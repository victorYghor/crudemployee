# Generated by Django 5.1.3 on 2024-11-29 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_alter_employee_managers_employee_date_joined_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='employee',
            unique_together={('username', 'last_name', 'email')},
        ),
        migrations.AlterField(
            model_name='employee',
            name='username',
            field=models.CharField(max_length=255),
        ),
        migrations.RemoveField(
            model_name='employee',
            name='name',
        ),
    ]
