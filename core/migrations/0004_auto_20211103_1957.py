# Generated by Django 3.2.9 on 2021-11-03 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Password',
            field=models.BinaryField(max_length=64),
        ),
        migrations.AlterField(
            model_name='user',
            name='Salt',
            field=models.BinaryField(max_length=32),
        ),
    ]
