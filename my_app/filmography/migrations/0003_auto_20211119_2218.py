# Generated by Django 3.2.9 on 2021-11-19 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filmography', '0002_auto_20211119_2215'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActorUserRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('phrase', models.CharField(max_length=64)),
                ('response', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.RemoveField(
            model_name='userapirequest',
            name='user',
        ),
        migrations.AlterField(
            model_name='actor',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='actormovie',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='actoruser',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.DeleteModel(
            name='ActorFormModel',
        ),
        migrations.DeleteModel(
            name='UserAPIRequest',
        ),
        migrations.AddField(
            model_name='actoruserrequest',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='filmography.userprofile'),
        ),
    ]
