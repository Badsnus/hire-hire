import uuid

from rest_framework import mixins, viewsets

from add_question.models import AddQuestion
from api_add_question.serializers import AddQuestionSerializer


class AddQuestionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = AddQuestion.objects.all()
    serializer_class = AddQuestionSerializer

    def dispatch(self, request, *args, **kwargs):
        self.user_cookie = request.COOKIES.get('user_cookie')
        if not self.user_cookie:
            self.user_cookie = uuid.uuid4().hex
            response = super().dispatch(request, *args, **kwargs)
            response.set_cookie('user_cookie', self.user_cookie)
        else:
            response = super().dispatch(request, *args, **kwargs)
        return response

    def perform_create(self, serializer):
        ip_address = self.request.META.get('REMOTE_ADDR')
        author = (
            self.request.user if self.request.user.is_authenticated else None
        )
        user_cookie = self.user_cookie if not author else None
        serializer.save(
            ip_address=ip_address,
            author=author,
            user_cookie=user_cookie,
        )
