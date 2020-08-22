# Generated by Django 2.0.1 on 2020-08-10 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ieltsapp', '0043_auto_20200807_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batch_db',
            name='category',
        ),
        migrations.AddField(
            model_name='batch_db',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='ieltsapp.Main_Course_Category_Db'),
        ),
    ]
