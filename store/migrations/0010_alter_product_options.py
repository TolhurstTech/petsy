# Generated by Django 4.2.7 on 2023-12-13 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_review_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_on']},
        ),
    ]
