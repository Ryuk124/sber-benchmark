# Generated migration for AIAnalysisResult model

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AIAnalysisResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competitor', models.CharField(db_index=True, max_length=200)),
                ('product', models.CharField(max_length=200)),
                ('criterion', models.CharField(max_length=200)),
                ('analysis_type', models.CharField(choices=[('facts', 'Extraction of Facts'), ('comparison', 'Comparison Analysis'), ('recommendation', 'Recommendation')], default='facts', max_length=20)),
                ('value', models.TextField(blank=True, null=True)),
                ('source_url', models.URLField(blank=True, null=True)),
                ('parsed_at', models.DateTimeField()),
                ('analysis_at', models.DateTimeField(auto_now_add=True)),
                ('llm_model', models.CharField(default='Qwen-14B', max_length=100)),
                ('llm_prompt_version', models.CharField(default='v1', max_length=50)),
                ('confidence_score', models.FloatField(blank=True, null=True)),
                ('raw_response', models.JSONField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-analysis_at'],
            },
        ),
        migrations.AddIndex(
            model_name='aianalysisresult',
            index=models.Index(fields=['competitor', 'product'], name='ai_analysis_result_competitor_product_idx'),
        ),
        migrations.AddIndex(
            model_name='aianalysisresult',
            index=models.Index(fields=['parsed_at'], name='ai_analysis_result_parsed_at_idx'),
        ),
    ]
