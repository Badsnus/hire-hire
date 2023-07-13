from django import forms
from django.contrib import admin, messages
from django.contrib.admin.utils import model_ngettext
from django.db import models, router, transaction
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext

from add_question.mixins import DefaultFilterMixin
from add_question.models import AddQuestion
from add_question.services import get_count_questions_text
from interview.models import Question


@admin.register(AddQuestion)
class AddQuestionAdmin(DefaultFilterMixin, admin.ModelAdmin):
    """Админ панель предложенных вопросов."""

    list_per_page = 8

    APPROVE = '_approve'
    REJECT = '_reject'

    @admin.display(description='Одобряем?')
    def approve_button(self, obj):
        return mark_safe(
            '<div class="submit-row">'
            f'<button type="submit" value={self.APPROVE} name="status">'
            'ОДОБРИТЬ</button></div>',
        )

    @admin.display(description='Отклонить?')
    def reject_button(self, obj):
        return mark_safe(
            '<div class="submit-row">'
            f'<button type="submit" value={self.REJECT} name="status">'
            'ОТКЛОНИТЬ</button></div>',
        )

    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(attrs={'rows': 3, 'cols': 45}),
        },
    }

    list_display = (
        AddQuestion.id.field.name,
        AddQuestion.status.field.name,
        AddQuestion.text.field.name,
        AddQuestion.answer.field.name,
        AddQuestion.pub_date.field.name,
        AddQuestion.language.field.name,
    )
    list_editable = (
        AddQuestion.text.field.name,
        AddQuestion.answer.field.name,
        AddQuestion.language.field.name,
    )
    search_fields = (
        AddQuestion.language.field.name,
        AddQuestion.text.field.name,
        AddQuestion.answer.field.name,
    )
    list_filter = (
        AddQuestion.language.field.name,
        AddQuestion.status.field.name,
    )
    readonly_fields = (
        AddQuestion.id.field.name,
        AddQuestion.status.field.name,
        AddQuestion.ip_address.field.name,
        AddQuestion.user_cookie_id.field.name,
        AddQuestion.author.field.name,
        AddQuestion.pub_date.field.name,
        approve_button.__name__,
        reject_button.__name__,
    )

    default_filters = (('status__exact', AddQuestion.StatusChoice.PROPOSED),)
    empty_value_display = '-пусто-'

    actions = ('approve', 'reject')

    @admin.action(description='Одобрить выбранные вопросы.')
    def approve(self, request, queryset):
        questions = [
            Question(language=obj.language, text=obj.text, answer=obj.answer)
            for obj in queryset
        ]
        Question.objects.bulk_create(questions)
        queryset.update(status=AddQuestion.StatusChoice.APPROVED)
        self.message_user(
            request,
            f'Одобрен{get_count_questions_text(len(questions))}.',
        )

    @admin.action(description='Отклонить выбранные вопросы.')
    def reject(self, request, queryset):
        queryset.update(status=AddQuestion.StatusChoice.REJECTED)
        self.message_user(
            request,
            f'Отклонен{get_count_questions_text(len(queryset))}.',
        )

    def response_change(self, request, obj):
        """В change_view обработка нажатия кнопок 'Одобрить' и 'Отклонить'."""

        if request.POST.get('status') == self.APPROVE:
            Question.objects.create(
                language=obj.language,
                text=obj.text,
                answer=obj.answer,
            )
            obj.status = AddQuestion.StatusChoice.APPROVED
            obj.save()
            self.message_user(request, 'Вопрос одобрен.')
        elif request.POST.get('status') == self.REJECT:
            obj.status = AddQuestion.StatusChoice.REJECTED
            obj.save()
            self.message_user(request, 'Вопрос отклонён.')
        return super().response_change(request, obj)

    def response_action(self, request, queryset):
        """
        When we use an our custom action and we have list_editable fields this
        part saves all the changes that have been made in list_editable fields.
        That part of code is exactly part that we need from changelist_view
        method.
        """

        print(self.get_changelist_instance(request).__dict__)

        formset = self.get_changelist_formset(request)
        modified_objects = self._get_list_editable_queryset(
            request,
            formset.get_default_prefix(),
        )
        formset = formset(
            request.POST,
            request.FILES,
            queryset=modified_objects,
        )
        if formset.is_valid():
            changecount = 0
            with transaction.atomic(using=router.db_for_write(self.model)):
                for form in formset.forms:
                    if form.has_changed():
                        obj = self.save_form(request, form, change=True)
                        self.save_model(request, obj, form, change=True)
                        self.save_related(
                            request,
                            form,
                            formsets=[],
                            change=True,
                        )
                        change_msg = self.construct_change_message(
                            request,
                            form,
                            None,
                        )
                        self.log_change(request, obj, change_msg)
                        changecount += 1
            if changecount:
                msg = ngettext(
                    '%(count)s %(name)s was changed successfully.',
                    '%(count)s %(name)s were changed successfully.',
                    changecount,
                ) % {
                    'count': changecount,
                    'name': model_ngettext(self.opts, changecount),
                }
                self.message_user(request, msg, messages.SUCCESS)

        return super().response_action(request, queryset)
