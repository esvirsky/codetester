# Generated by Django 2.2.6 on 2020-01-08 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0016_question_wrap_solution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='wrap_solution',
        ),
    ]