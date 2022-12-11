from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from .models import Households, HhAllergies, Packaging, Kits, Ingredients, Users, MealPlans, MealPacks, RecipeAllergies, RecipeDiets, RecipeIngredients, RecipeInstructions, Recipes

class AllergySerializer(ModelSerializer):
	class Meta():
		model = HhAllergies
		fields = ('__all__')
		depth = 1

class UserSerializer(ModelSerializer):
	class Meta():
		model = Users
		fields = ('__all__')

class HouseholdSerializer(ModelSerializer):
	class Meta():
		model = Households
		fields = ('__all__')

class IngredientInvSerializer(ModelSerializer):
	isupplier_name = serializers.CharField(max_length=200)
	pref_isupplier_name = serializers.CharField(max_length=200)
	class Meta():
		model = Ingredients
		fields = ('i_id', 'ingredient_name', 'pkg_type', 'storage_type', 'in_date', 'in_qty', 'unit', 'exp_date', 'unit_cost', 'flat_fee', 'isupplier_name', 'pref_isupplier_name')

class HouseholdAllergySerializer(ModelSerializer):
	hh_allergies = AllergySerializer(many=True)
	class Meta():
		model = Households
		fields = ('hh_name', 'num_adult', 'num_child', 'sms_flag', 'veg_flag', 'allergy_flag', 'gf_flag', 'ls_flag', 'paused_flag', 'phone', 'street', 'city', 'pcode', 'state', 'delivery_notes', 'hh_allergies')

class PackagingSerializer(ModelSerializer):
	class Meta():
		model = Packaging
		fields = ('__all__')

class MealKitSerializer(ModelSerializer):
	class Meta():
		model = Kits
		fields = ('__all__')

class MealPlansSerializer(ModelSerializer):
	class Meta():
		model = MealPlans
		fields = ('__all__')

class MealPacksSerializers(ModelSerializer):
	class Meta():
		model = MealPacks
		fields = ('__all__')


class RecipeAllergySerializers(ModelSerializer):
	class Meta():
		model = RecipeAllergies
		fields = ('__all__')

class RecipeDietsSerializers(ModelSerializer):
	class Meta():
		model = RecipeDiets
		fields = ('__all__')

class RecipeIngredientsSerializers(ModelSerializer):
	class Meta():
		model = RecipeIngredients
		fields = ('__all__')

class RecipeInstructionsSerializers(ModelSerializer):
	class Meta():
		model = RecipeInstructions
		fields = ('__all__')

class RecipesSerializers(ModelSerializer):
	class Meta():
		model = Recipes
		fields = ('__all__')