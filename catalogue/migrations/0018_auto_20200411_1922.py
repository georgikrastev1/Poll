# Generated by Django 2.1 on 2020-04-11 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0017_auto_20200411_1542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmark',
            name='bookmarked_case',
        ),
        migrations.RemoveField(
            model_name='bookmark',
            name='user',
        ),
        migrations.RemoveField(
            model_name='case',
            name='author',
        ),
        migrations.RemoveField(
            model_name='case',
            name='case_disease',
        ),
        migrations.RemoveField(
            model_name='contactsubmission',
            name='case',
        ),
        migrations.RemoveField(
            model_name='contactsubmission',
            name='user',
        ),
        migrations.RemoveField(
            model_name='media',
            name='case',
        ),
        migrations.DeleteModel(
            name='Bookmark',
        ),
        migrations.DeleteModel(
            name='Case',
        ),
        migrations.DeleteModel(
            name='ContactSubmission',
        ),
        migrations.DeleteModel(
            name='Disease',
        ),
        migrations.DeleteModel(
            name='Media',
        ),
    ]
