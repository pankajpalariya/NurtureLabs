# Generated by Django 3.2.9 on 2021-11-14 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_rename_avisor_photo_url_advisor_advisor_photo_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advisor',
            name='Advisor_Photo_Url',
            field=models.CharField(max_length=499),
        ),
    ]
