# Generated by Django 3.0.3 on 2020-04-09 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_postdesc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postdesc',
            name='status',
            field=models.CharField(max_length=10),
        ),
    ]