# Generated by Django 3.0.3 on 2020-04-08 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='imgLink',
            field=models.TextField(default='ABC'),
            preserve_default=False,
        ),
    ]
