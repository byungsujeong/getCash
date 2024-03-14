# Generated by Django 5.0.3 on 2024-03-14 11:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성일시')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='수정일시')),
                ('earned', models.IntegerField(verbose_name='획득캐시')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question', verbose_name='문제')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]