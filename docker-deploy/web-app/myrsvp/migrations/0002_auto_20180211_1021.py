# Generated by Django 2.0.1 on 2018-02-11 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrsvp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[(0, 'multiple choice'), (1, 'text question')], default=0, max_length=1),
        ),
    ]
