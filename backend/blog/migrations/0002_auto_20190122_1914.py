# Generated by Django 2.1.5 on 2019-01-22 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptions',
            name='have_read',
            field=models.ManyToManyField(blank=True, to='blog.Post', verbose_name='Прочитаные посты'),
        ),
    ]
