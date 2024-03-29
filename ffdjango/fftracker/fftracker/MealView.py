from .helperfuncs import execute_query
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework import status
from .models import MealPlans, Recipes

class MealSerializer(ModelSerializer):
	meal_name = serializers.CharField(max_length=200)
	snack_name = serializers.CharField(max_length=200)
	m_s = serializers.models.SmallIntegerField()
	m_latest = serializers.models.DateField(blank=True, null=True)
	s_latest = serializers.models.DateField(blank=True, null=True)
	class Meta():
		model = MealPlans
		fields = ('m_id', 'm_date', 'meal_name', 'snack_name', 'm_s', 'm_latest', 's_latest' )

class MealView(viewsets.ViewSet):
	def list(self, request):
		keys = ('m_id', 'm_date', 'snack_r_num', 'meal_r_num', 'num_servings', 'meal_name', 'snack_name')
		query = "SELECT mp.*, (SELECT r_name FROM recipes WHERE mp.meal_r_num = r_num) AS meal_name, (SELECT r_name FROM recipes WHERE mp.snack_r_num = r_num) AS snack_name FROM meal_plans mp"
		queryset = execute_query(query, keys, many=True)
		serializer = MealSerializer(queryset, many=True)
		return Response(serializer.data)
	def retrieve(self, request, pk):
		query = "SELECT mp.*, (SELECT r_name FROM recipes WHERE mp.meal_r_num = r_num) AS meal_name, (SELECT r_name FROM recipes WHERE mp.snack_r_num = r_num) AS snack_name FROM meal_plans mp WHERE mp.m_id=%s"%(pk)
		keys = ('m_id', 'm_date', 'snack_r_num', 'meal_r_num', 'num_servings', 'meal_name', 'snack_name')
		queryset = execute_query(query, keys)
		serializer = MealSerializer(queryset)
		return Response(serializer.data)
	def update(self, request):
		data = request.data
		serializer = MealSerializer(data)
		if serializer.is_valid():
			serializer.save()
			return Response(status=status.HTTP_200_OK)
		return Response(status=status.HTTP_200_BADREQUEST)
