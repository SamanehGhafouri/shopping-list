# Generated by Django 4.0.10 on 2023-07-21 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_store'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.store')),
            ],
        ),
    ]
