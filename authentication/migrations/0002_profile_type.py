# Generated by Django 4.2.7 on 2023-12-26 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='type',
            field=models.CharField(choices=[('personal', 'personal'), ('joint', 'joint'), ('organization', 'organization'), ('visa', 'visa'), ('retirement', 'retirement')], default='personal', max_length=20),
        ),
    ]
