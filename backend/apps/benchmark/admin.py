from django.contrib import admin
from .models import Bank, Product, Criterion, Source, Snapshot, FeatureValue, ParseLog


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'website', 'created_at')
    search_fields = ('id', 'name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('id', 'name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('id', 'name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'created_at')
    search_fields = ('name', 'url')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Snapshot)
class SnapshotAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'created_at', 'parsing_status', 'is_active')
    list_filter = ('parsing_status', 'is_active', 'created_at')
    search_fields = ('product__name',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(FeatureValue)
class FeatureValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'bank', 'criterion', 'value', 'confidence', 'source', 'created_at')
    list_filter = ('value', 'confidence', 'bank', 'source', 'created_at')
    search_fields = ('bank__name', 'criterion__name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(ParseLog)
class ParseLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'status', 'created_at')
    list_filter = ('status', 'source', 'created_at')
    search_fields = ('source__name', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
