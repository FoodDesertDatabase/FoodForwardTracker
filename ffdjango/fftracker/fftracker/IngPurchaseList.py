from .helperfuncs import execute_query
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework import status
from django.db.models import Prefetch
from .models import Ingredients, IngredientUsages
import os

class IngredientUsageSerializer(ModelSerializer):
	class Meta():
		model = IngredientUsages
		fields = ('used_date', 'used_qty')

class IngredientInvSerializer(ModelSerializer):
	isupplier = serializers.CharField(max_length=200)
	pref_isupplier = serializers.CharField(max_length=200)
	ingredient_usage = IngredientUsageSerializer()
	class Meta():
		model = Ingredients
		fields = ('i_id', 'ingredient_name', 'pkg_type', 'storage_type', 'in_date', 'in_qty', 'ingredient_usage', 'unit', 'exp_date', 'unit_cost', 'flat_fee', 'isupplier', 'pref_isupplier')

# Create your views here.
class IngredientInvView(viewsets.ViewSet):
	def list(self, request):
		#keys = ('i_id', 'ingredient_name', 'pkg_type', 'storage_type', 'in_date', 'in_qty', 'unit', 'exp_date', 'qty_on_hand', 'unit_cost', 'flat_fee', 'isupplier_id', 'pref_supplier_id', 'isupplier_name', 'pref_isupplier_name')
		#query = "SELECT i.*, (SELECT s_name FROM supplier WHERE i.isupplier_id = s_id) AS isupplier_name, (SELECT s_name FROM supplier WHERE i.pref_isupplier_id = s_id) AS pref_supplier_name FROM ingredients i"
		#queryset = execute_query(query, keys, many=True)
		queryset = Ingredients.objects.prefetch_related(Prefetch('ingredient_usage', queryset=IngredientUsages.objects.all())).all().all()
		print(queryset[0].__dict__['_prefetched_objects_cache']['ingredient_usage'].__dict__)
		serializer = IngredientInvSerializer(queryset, many=True)
		return Response(serializer.data)
	def retrieve(self, request, pk):
		query = "SELECT i.*, (SELECT s_name FROM supplier WHERE i.isupplier_id = s_id) AS isupplier_name, (SELECT s_name FROM supplier WHERE i.pref_isupplier_id = s_id) AS pref_supplier_name FROM ingredients i WHERE i.i_id=%s"%(pk)
		keys = ('i_id', 'ingredient_name', 'pkg_type', 'storage_type', 'in_date', 'in_qty', 'unit', 'exp_date', 'qty_on_hand', 'unit_cost', 'flat_fee', 'isupplier_id', 'pref_supplier_id', 'isupplier_name', 'pref_isupplier_name')
		queryset = execute_query(query, keys)
		serializer = IngredientInvSerializer(queryset)
		return Response(serializer.data)
	def update(self, request, pk):
		update_obj = Ingredients.Objects.get(pk)
		serializer = IngredientInvSerializer(update_obj, data=request.data)
		if serializer.is_valid():
			obj = serializer.save()
			obj.save()
			return Response(status=status.HTTP_200_OK)
		return Response(status=status.HTTP_200_BADREQUEST)
	def create(self, request):
		data = request.data
		serializer = IngredientInvSerializer(data=data)
		if serializer.is_valid():
			obj = serializer.save()
			obj.save()
			return Response(obj, status=200)
		return Response(status=400)
	def destroy(self, request, pk):
		ingredient = Ingredients.Objects.get(pk)
		ingredient.delete()
		return Response(status=204)