# Generated by Django 3.2.9 on 2021-11-27 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmography', '0007_auto_20211127_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor_imdb_id', models.CharField(max_length=64)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('response', models.TextField(blank=True, default='')),
                ('status', models.CharField(choices=[('p', 'W kolejce'), ('r', 'W trakcie pobierania'), ('e', 'Błąd'), ('d', 'Pobrano')], default='p', max_length=1)),
            ],
        ),
    ]