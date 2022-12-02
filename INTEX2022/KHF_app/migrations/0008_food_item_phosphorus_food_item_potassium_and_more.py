# Generated by Django 4.1.2 on 2022-11-30 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KHF_app', '0007_alter_meal_meal_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='food_item',
            name='phosphorus',
            field=models.FloatField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='food_item',
            name='potassium',
            field=models.FloatField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='food_item',
            name='protein',
            field=models.FloatField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='food_item',
            name='sodium',
            field=models.FloatField(default=2),
            preserve_default=False,
        ),
    ]