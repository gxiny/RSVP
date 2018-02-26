# Generated by Django 2.0.1 on 2018-02-11 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=200)),
                ('finalize', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('visibility', 'can see answers'),),
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=1000)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('address', models.CharField(max_length=100)),
                ('email_subject', models.CharField(max_length=20, null=True)),
                ('email_message', models.TextField(max_length=200, null=True)),
                ('owner_email', models.EmailField(max_length=254, null=True)),
                ('vendor_email', models.CharField(max_length=200, null=True)),
                ('guest_email', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, max_length=50)),
                ('question_type', models.CharField(choices=[('M', 'multiple choice'), ('S', 'single choice'), ('T', 'text question')], default='M', max_length=1)),
                ('vendor_editable', models.NullBooleanField(default=True)),
                ('vendor_permission', models.NullBooleanField(default=True)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question', to='myrsvp.Event')),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='choice',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myrsvp.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myrsvp.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
