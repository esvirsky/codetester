# Generated by Django 2.2.6 on 2019-10-25 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0014_auto_20191024_0337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answersubmission',
            name='code',
            field=models.TextField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='answersubmission',
            name='response',
            field=models.TextField(max_length=2000),
        ),
    ]
