# Generated by Django 2.1.7 on 2019-03-24 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sec', '0003_auto_20190324_2353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher_user',
            name='total_lectures',
        ),
        migrations.AlterField(
            model_name='teacher_user',
            name='count',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='teacher_user',
            name='teacher_code',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
