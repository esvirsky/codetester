# Generated by Django 2.2.6 on 2019-10-11 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0006_answersubmission_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='assignee',
        ),
        migrations.CreateModel(
            name='AssessmentTake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('assignee', models.CharField(max_length=255)),
                ('done', models.BooleanField(default=False)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_takes', to='assessment.Assessment')),
            ],
            options={
                'db_table': 'assessment_takes',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='assessment_take',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='assessment.AssessmentTake'),
            preserve_default=False,
        ),
    ]
