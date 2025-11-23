from django.contrib import admin
from apps.ai.llm_service import AIAnalysisResult


@admin.register(AIAnalysisResult)
class AIAnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('competitor', 'product', 'criterion', 'analysis_type', 'confidence_score', 'analysis_at')
    list_filter = ('analysis_type', 'llm_model', 'analysis_at')
    search_fields = ('competitor', 'product', 'criterion', 'value')
    readonly_fields = ('analysis_at', 'parsed_at', 'raw_response')
    fieldsets = (
        ('Основная информация', {
            'fields': ('competitor', 'product', 'criterion', 'analysis_type')
        }),
        ('Результаты анализа', {
            'fields': ('value', 'confidence_score', 'source_url')
        }),
        ('Технические данные', {
            'fields': ('parsed_at', 'analysis_at', 'llm_model', 'llm_prompt_version', 'raw_response'),
            'classes': ('collapse',)
        }),
    )
