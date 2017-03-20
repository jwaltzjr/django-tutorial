from django.contrib import admin

# Register your models here.

from . import models

class ChoiceInline(admin.TabularInline):
    model = models.Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    # fields = ['pub_date','question_text']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date Info', {'fields': ['pub_date']})
    ]
    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    search_fields = ['question_text']



admin.site.register(models.Question, QuestionAdmin)