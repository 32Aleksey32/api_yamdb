# Generated by Django 2.2.16 on 2022-07-26 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(max_length=50, null=True, verbose_name='Код подтверждения'),
        ),
    ]