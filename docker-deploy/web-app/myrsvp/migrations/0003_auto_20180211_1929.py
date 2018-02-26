# Generated by Django 2.0.1 on 2018-02-11 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrsvp', '0002_auto_20180211_1021'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'permissions': (('regist', 'can regist for event'),)},
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.IntegerField(choices=[(0, 'multiple choice'), (1, 'text question')], default=0),
        ),
    ]