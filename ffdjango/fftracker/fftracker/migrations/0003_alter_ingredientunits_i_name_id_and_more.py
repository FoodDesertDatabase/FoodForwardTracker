# Generated by Django 4.1.3 on 2023-07-28 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fftracker', '0002_ingredientunits_recipe_unit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredients',
            name='amt',
            field=models.DecimalField(decimal_places=3, max_digits=6),
        ),
    ]