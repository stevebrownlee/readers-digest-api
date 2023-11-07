from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from digestapi.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'rating', 'comment', 'date_posted', 'is_owner']

    def get_is_owner(self, obj):
        # Check if the request has a user and if the user is the owner
        return self.context['request'].user == obj.user


class ReviewViewSet(viewsets.ViewSet):

    def list(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        review = Review(
            book_id=request.data['book'],
            user=request.auth.user,
            rating=request.data['rating'],
            comment=request.data['comment']
        )
        review.save()

        try:
            serializer = ReviewSerializer(review, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)

        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            if review.user.id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)

            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
