from django.contrib import admin

from .models import Question, Choice

admin.site.register(Choice)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fields = ['date_published', 'question_text']
    inlines = [ChoiceInline]
    list_display = ('question_text', 'date_published',
                    'was_published_recently')
    list_filter = ['date_published']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
