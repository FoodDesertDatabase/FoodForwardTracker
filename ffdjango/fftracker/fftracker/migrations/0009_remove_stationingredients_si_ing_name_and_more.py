# Generated by Django 4.1.3 on 2023-08-13 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fftracker', '0008_remove_ingredientunits_i_name_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stationingredients',
            name='si_ing_name',
        ),
        migrations.AddField(
            model_name='stationingredients',
            name='si_recipe_ing',
            field=models.ForeignKey(db_column='si_recipe_ing', default=None, on_delete=django.db.models.deletion.CASCADE, to='fftracker.recipeingredients'),
            preserve_default=False,
        ),
    ]
