# Generated by Django 4.2.3 on 2023-07-12 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jitter', '0005_alter_profile_date_modified'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='meeme', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
