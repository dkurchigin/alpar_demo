# Generated by Django 2.2.5 on 2019-10-02 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParsingTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.TextField(verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Задача для парсинга',
                'verbose_name_plural': 'Задачи для парсинга',
            },
        ),
    ]
