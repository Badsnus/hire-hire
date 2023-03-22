from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, InterviewViewset, LanguageViewSet

router = DefaultRouter()

router.register(r'category', CategoryViewSet)
router.register(r'language', LanguageViewSet)
router.register(r'interview', InterviewViewset, basename='interview')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
]