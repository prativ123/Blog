# Generated by Django 4.2.1 on 2023-09-25 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0013_remove_customtaggeditem_content_object_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='blog_views',
            field=models.IntegerField(default=0),
        ),
    ]
