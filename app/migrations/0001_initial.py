# Generated by Django 3.2.4 on 2022-07-22 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=12)),
                ('winner', models.BooleanField(default=False)),
                ('try_again', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UniqueCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, default='Automatic Generated', editable=False, max_length=8, null=True, unique=True)),
                ('used', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('prize', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.prize')),
            ],
        ),
        migrations.CreateModel(
            name='Draw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('code', models.CharField(max_length=8)),
                ('sent', models.BooleanField(default=False)),
                ('rotation', models.IntegerField(default=0)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('retry_used', models.BooleanField(default=False)),
                ('prize', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.prize')),
            ],
        ),
    ]
