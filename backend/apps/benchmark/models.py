from django.db import models


class Bank(models.Model):
    """Модель банка для сравнения"""
    id = models.SlugField(primary_key=True, max_length=50)
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Банк'
        verbose_name_plural = 'Банки'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель банковского продукта/услуги"""
    id = models.SlugField(primary_key=True, max_length=100)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Criterion(models.Model):
    """Модель критерия сравнения"""
    id = models.SlugField(primary_key=True, max_length=100)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Критерий'
        verbose_name_plural = 'Критерии'

    def __str__(self):
        return self.name


class Source(models.Model):
    """Источник данных (сайт агрегатора, банка и т.д.)"""
    name = models.CharField(max_length=200, unique=True)
    url = models.URLField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'

    def __str__(self):
        return self.name


class Snapshot(models.Model):
    """Снимок данных по дате (версионирование)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='snapshots')
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    parsing_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'В ожидании'),
            ('in_progress', 'В процессе'),
            ('completed', 'Завершено'),
            ('failed', 'Ошибка'),
        ],
        default='pending'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Снимок'
        verbose_name_plural = 'Снимки'
        indexes = [
            models.Index(fields=['product', '-created_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'{self.product.name} - {self.created_at.strftime("%Y-%m-%d %H:%M")}'


class FeatureValue(models.Model):
    """Значение критерия для банка в конкретном снимке"""
    snapshot = models.ForeignKey(Snapshot, on_delete=models.CASCADE, related_name='features')
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    value = models.BooleanField(help_text='Наличие критерия')
    confidence = models.FloatField(null=True, blank=True, help_text='Уверенность парсера 0.0-1.0')
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True)
    source_url = models.URLField(blank=True, null=True, help_text='Ссылка на конкретную страницу')
    raw_data = models.JSONField(null=True, blank=True, help_text='Сырые данные с парсера')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['bank', 'criterion']
        verbose_name = 'Значение критерия'
        verbose_name_plural = 'Значения критериев'
        unique_together = ('snapshot', 'bank', 'criterion')
        indexes = [
            models.Index(fields=['snapshot', 'bank']),
            models.Index(fields=['source']),
        ]

    def __str__(self):
        return f'{self.bank.name} - {self.criterion.name}: {self.value}'


class ParseLog(models.Model):
    """Лог парсинга для отладки и мониторинга"""
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='logs')
    snapshot = models.ForeignKey(Snapshot, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('success', 'Успешно'),
            ('warning', 'Предупреждение'),
            ('error', 'Ошибка'),
        ],
        default='success'
    )
    message = models.TextField()
    error_trace = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Лог парсинга'
        verbose_name_plural = 'Логи парсинга'
        indexes = [
            models.Index(fields=['source', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f'{self.source.name} - {self.status}'
