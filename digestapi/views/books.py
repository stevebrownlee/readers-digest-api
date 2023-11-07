from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from digestapi.models import Book, Category
from .categories import CategorySerializer


class BookWriteSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), required=True
    )

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "isbn_number",
            "cover_image",
            "categories",
        ]


class BookReadSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True)

    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context["request"].user == obj.user

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "isbn_number",
            "cover_image",
            "is_owner",
            "categories",
        ]


class BookViewSet(viewsets.ViewSet):
    serializer_class = BookReadSerializer

    def list(self, request):
        books = Book.objects.all()
        serializer = BookReadSerializer(books, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookReadSerializer(book, context={"request": request})
            return Response(serializer.data)

        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        title = request.data.get("title")
        author = request.data.get("author")
        isbn_number = request.data.get("isbn_number")
        cover_image = request.data.get("cover_image")

        book = Book.objects.create(
            user=request.user,
            title=title,
            author=author,
            cover_image=cover_image,
            isbn_number=isbn_number,
        )

        category_ids = request.data.get("categories", [])
        book.categories.set(category_ids)

        serializer = BookReadSerializer(book, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)

            if book.user == request.auth.user:
                book.title = request.data.get("title", None)
                book.author = request.data.get("author", None)
                book.isbn_number = request.data.get("isbn_number", None)
                book.cover_image = request.data.get("cover_image", None)
                category_ids = request.data.get("categories", [])

                serializer = BookWriteSerializer(data=request.data)
                if not serializer.is_valid():
                    return Response(
                        serializer.errors,
                        status.HTTP_400_BAD_REQUEST,
                    )

                book.save()

                book.categories.set(category_ids)

                serializer = BookReadSerializer(book, context={"request": request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(
                {"message": "You are not the owner of that book."},
                status.HTTP_403_FORBIDDEN,
            )

        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            self.check_object_permissions(request, book)
            book.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
