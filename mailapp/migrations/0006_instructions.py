# Generated by Django 3.0.8 on 2020-07-07 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailapp', '0005_auto_20200702_0359'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instructions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'instruction',
            },
        ),
    ]
