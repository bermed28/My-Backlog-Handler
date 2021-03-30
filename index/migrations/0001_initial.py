# Generated by Django 3.1.7 on 2021-03-30 16:42

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Developer_Model',
            fields=[
                ('dev_id', models.IntegerField(primary_key=True, serialize=False)),
                ('dev_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Game_Model',
            fields=[
                ('game_id', models.IntegerField(primary_key=True, serialize=False)),
                ('game_title', models.CharField(max_length=128)),
                ('genres', django.contrib.postgres.fields.jsonb.JSONField()),
                ('developers', django.contrib.postgres.fields.jsonb.JSONField()),
                ('platforms', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Genre_Model',
            fields=[
                ('genre_id', models.IntegerField(primary_key=True, serialize=False)),
                ('genre_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Image_Model',
            fields=[
                ('img_id', models.IntegerField(primary_key=True, serialize=False)),
                ('img_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Library_Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_played', models.DateField()),
                ('is_finished', models.BooleanField(default=False)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.game_model')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_name', models.CharField(max_length=128)),
                ('user_name', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Library_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games', models.ManyToManyField(through='index.Library_Membership', to='index.Game_Model')),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='library_membership',
            name='library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.library_model'),
        ),
        migrations.AddField(
            model_name='game_model',
            name='img_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.image_model'),
        ),
    ]
