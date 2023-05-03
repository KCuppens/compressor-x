"""Faq admin."""
from django.contrib import admin
from django.db import models, transaction

from adminsortable2.admin import SortableAdminMixin, SortableTabularInline
from martor.widgets import AdminMartorWidget

from apps.translations.admin import TranslatableAdmin, TranslationInline
from apps.translations.tasks import translate_object

from .models import Question, Topic


class QuestionAdminInline(SortableTabularInline):
    """Question admin inline."""

    model = Question
    extra = 1
    verbose_name = "Question"
    verbose_name_plural = "Questions"
    fields = ("position", "question", "answer", "state")


class TopicAdmin(SortableAdminMixin, TranslatableAdmin, admin.ModelAdmin):
    """Topic admin."""

    actions = ["make_published", "make_draft"]
    search_fields = ("name", "description")
    list_display = ("position", "name", "state")
    list_display_links = ("name",)
    list_editable = ("state",)
    fields = (
        "position",
        "state",
        "name",
        "description",
        "meta_title",
        "meta_description",
        "meta_keywords",
    )

    formfield_overrides = {
        models.TextField: {"widget": AdminMartorWidget},
    }
    inlines = [QuestionAdminInline, TranslationInline]

    def save_model(self, request, obj, form, change):
        """Save the model and auto translate."""
        obj.user = request.user
        transaction.on_commit(lambda: translate_object.delay("faq.Topic", obj.id))
        for question in obj.question_set.all():
            transaction.on_commit(
                lambda: translate_object.delay("faq.Question", question.id)  # noqa B023
            )
        super().save_model(request, obj, form, change)


admin.site.register(Topic, TopicAdmin)
