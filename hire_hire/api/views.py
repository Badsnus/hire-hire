from rest_framework import viewsets
from rest_framework import mixins

from interview.models import Category, Interview, Language, Question

from api.serializers import (
    CategoryListSerializer,
    CategoryRetrieveSerializer,
    InterviewCreateSerializer,
    InterviewSerializer,
    LanguageSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return CategoryRetrieveSerializer


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()


class InterviewViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):

    # обязательно дописать пермишны

    def get_queryset(self):
        if self.action == 'retrieve':
            return Interview.objects.get_interview_by_user(
                user=self.request.user,
                interview_pk=self.kwargs.get('pk'),
            )
        return Interview.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return InterviewCreateSerializer
        return InterviewSerializer

    def perform_create(self, serializer):
        print(serializer.validated_data)
        serializer.save()

