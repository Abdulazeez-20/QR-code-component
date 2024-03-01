# Generated by Django 5.0.2 on 2024-02-27 15:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lemonAPI', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='menuitem',
            name='drinks',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='lemonAPI.drinks'),
        ),
    ]
