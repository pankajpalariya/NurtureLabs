# Generated by Django 3.2.9 on 2021-11-14 02:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_rename_photourl_advisor_avisor_photo_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advisor',
            old_name='Avisor_Photo_Url',
            new_name='Advisor_Photo_Url',
        ),
    ]