from .helperfuncs import execute_query
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework import status
from .models import MealPlans, RecipePackaging, PackagingUsages, Packaging
from django.db.models import Prefetch
from collections import defaultdict
import os

# def get_latest_items(queryset, fieldName):
# 		new_queryset = []
# 		i = 0
# 		while i < len(queryset):
# 			print(len(queryset))
#             # find similar items
# 			similar_items = [n for n in queryset if getattr(n, fieldName) == getattr(queryset[i], fieldName)]
# 			print('%a, %a'%(getattr(queryset[i],fieldName), len(similar_items)))
#             # if this is not a duplicate
# 			if len(similar_items) <= 1:
#                 # put it in the queryset
# 				new_queryset.append(queryset[i])
#             # if this is a duplicate
# 			elif len(similar_items) > 1:
# 				print('in this section')
#                 # if this is the most recent (date) item
# 				latest_similar_item = similar_items[0]
# 				for n in similar_items:
# 					if n.m_date > latest_similar_item.m_date:
#                         # put it in the queryset
# 						latest_similar_item = n
# 				queryset = [x for x in queryset if getattr(x, fieldName) != getattr(latest_similar_item, fieldName)]
# 				new_queryset.append(latest_similar_item)
# 			i += 1
# 		return new_queryset

class PackagingUsageSerializer(ModelSerializer):
	used_qty = serializers.IntegerField()
	class Meta():
		model = PackagingUsages
		fields = ('used_date', 'used_qty', 'used_pkg')

class RecipePackagingSerializer(ModelSerializer):
	pkg_type = serializers.CharField(read_only=True)

	class Meta():
		model = RecipePackaging
		fields = ('pkg_type', 'rp_pkg')

class PackPurchasingSerializer(ModelSerializer):
	class Meta():
		model = Packaging
		fields = ('package_type', 'qty_on_hand', 'qty_needed')

class MealPlansSerializer(ModelSerializer):
	meal_name = serializers.CharField(source='meal_r_num.r_name')
	snack_name = serializers.CharField(source='snack_r_num.r_name')
	meal_servings = serializers.CharField()
	snack_servings = serializers.CharField()
	m_date = serializers.DateField()
	class Meta():
		model = MealPlans
		fields = ('m_id', 'm_date', 'meal_name', 'snack_name', 'snack_r_num', 'meal_r_num', 'meal_servings', 'snack_servings')

class PPLSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	meal_plans = MealPlansSerializer()
	packaging_usage = PackagingUsageSerializer()
	recipe_packaging = RecipePackagingSerializer()
	m_date = serializers.CharField()
	ms_name = serializers.CharField()
	unit = serializers.CharField()
	pkg_type = serializers.CharField()
	qty_on_hand = serializers.IntegerField()
	qty_needed = serializers.IntegerField()
	total_required = serializers.IntegerField()	

	
# class PPLView(viewsets.ViewSet):
	# def list(self, request):
	# 	startDate = request.query_params.get('startDate')
	# 	endDate = request.query_params.get('endDate')
	# 	if (startDate and endDate):
	# 		queryset = MealPlans.objects.filter(m_date__range=[startDate, endDate]).order_by('m_date')
	# 	else:
	# 		queryset = MealPlans.objects.all().order_by('m_date')
	# 	# meal_queryset = get_latest_items(queryset, 'meal_r_num')
	# 	serializer = PPLSerializer(queryset, many=True)


	# 	startDate = request.query_params.get('startDate')
	# 	endDate = request.query_params.get('endDate')
	# 	if (startDate and endDate):
	# 		queryset = PackagingUsages.objects.filter(used_date__range=[startDate, endDate]).order_by('used_date')
	# 	else:
	# 		queryset = PackagingUsages.objects.order_by('used_date')
	# 	# packaging_queryset = get_latest_items(queryset, 'used_qty')
	# 	serializer = PPLSerializer(queryset, many=True)


	# 	startDate = request.query_params.get('startDate')
	# 	endDate = request.query_params.get('endDate')
	# 	if (startDate and endDate):
	# 		queryset = RecipePackaging.objects.filter(pkg_type__range=[startDate, endDate]).order_by('pkg_type')
	# 	else:
	# 		queryset = RecipePackaging.objects.order_by('pkg_type')
	# 	serializer = PPLSerializer(queryset, many=True)
	# 	return Response(serializer.data)
    
	# def retrieve(self, request, pk):
	# 	query = "SELECT mp.*, (SELECT r_name FROM recipes WHERE mp.meal_r_num = r_num) AS meal_name, (SELECT r_name FROM recipes WHERE mp.snack_r_num = r_num) AS snack_name FROM meal_plans mp WHERE mp.m_id=%s"%(pk)
	# 	keys = ('m_id', 'm_date', 'snack_r_num', 'meal_r_num', 'meal_name', 'snack_name', 'num_servings')
	# 	queryset = execute_query(query, keys)
	# 	serializer = PPLSerializer(queryset)
	# 	return Response(serializer.data)
	# def update(self, request, pk):
	# 	update_obj = Packaging.objects.get(pk)
	# 	serializer = PPLSerializer(update_obj, data=request.data)
	# 	if serializer.is_valid():
	# 		obj = serializer.save()
	# 		obj.save()
	# 		return Response(status=status.HTTP_200_OK)
	# 	return Response(status=status.HTTP_200_BADREQUEST)
	
# queryset = Packaging.objects.prefetch_related(Prefetch('packaging_usage', queryset=PackagingUsages.objects.all())).all().all()
		# print(queryset[0].__dict__['_prefetched_objects_cache']['packaging_usage'].__dict__)


#from datetime import date, timedelta
class PPLView(viewsets.ViewSet):
	def list(self, request):
		id = 0
		m_date = 0
		ms_name = ''
		m_r_num = 0
		s_r_num = 0
		name = ''
		meal_servings = 0
		snack_servings = 0
		meal_name = ''
		snack_name = ''
		pkg_type = ''
		qty_on_hand = 0
		qty_needed = 0
		to_purchase = 0
		unit = ''
		total_required = 0
		amt = 0

		queryset = []
		# ||TRAINING|| this area is the most important bit to understand why the issue is happening 
		startDate = request.query_params.get('startDate')
		endDate = request.query_params.get('endDate')
		MealsQueryset = MealPlans.objects.filter(m_date__range=(startDate, endDate)).order_by('-m_date')
		PkgQueryset = Packaging.objects.all()
		recipeset = RecipePackaging.objects.all()
		pkg_type_totals = defaultdict(lambda: {"total_qty_on_hand": 0, "qty_needed": 0, "total_cost": 0})
		for meals in MealsQueryset:
    	# calculate servings needed for meal and snack
			# meal_servings = meal_plan.meal.rp_pkg.servings_per_recipe * meal_plan.meal_servings
			m_r_num = meals.meal_r_num
			s_r_num = meals.snack_r_num
			meal_servings = meals.meal_servings
			meal_name = meals.meal_r_num.r_name
			snack_name = meals.snack_r_num.r_name
			m_date = meals.m_date
			snack_servings = meals.snack_servings
			mealRecipePkg = RecipePackaging.objects.filter(rp_recipe_num=m_r_num)
			snackRecipePkg = RecipePackaging.objects.filter(rp_recipe_num=s_r_num)
			qty_needed += meal_servings
    		# process meal packaging
			for meal in mealRecipePkg:
				name = meal_name
				PkgQueryset = Packaging.objects.get(p_id=meal.rp_pkg)
				amt = meal.amt
				unit = meal.unit
				total_required = amt * qty_needed
				meal.rp_pkg = MealPlans.meal_r_num.rp_pkg
				packaging.package_type = RecipePackaging.pkg_type * qty_on_hand
			for recipe in recipeset:
					if m_r_num == recipe.r_num:
						ms_name = recipe.r_name
			for packaging in PkgQueryset:
				if unit == packaging.unit:
					qty_needed = qty_on_hand - meal_servings
					qty_on_hand = packaging.qty_on_hand
					pkg_type = meals.pkg_type
					if (int(total_required or 0) - int(qty_needed or 0)) > 0:
						to_purchase = int(total_required or 0) - int(qty_on_hand or 0)
					else:
						to_purchase = 0
					if (int(total_required or 0) - int(qty_needed or 0)) > 0:
						to_purchase = int(total_required or 0) - int(qty_on_hand or 0)
					else:
						to_purchase = 0
					queryset.append({'id': count,
									'm_date:': m_date, 
		      						'name': name,
									'ms_name': ms_name,
		    						'meal_name': meal_name, 
									'snack_name': snack_name, 
									'pkg_type': pkg_type, 
									'qty_on_hand': qty_on_hand, 
									'qty_needed': qty_needed,
									'total_required': total_required, 
									'to_purchase': to_purchase})
					count += 1

			cost = qty_needed * packaging.unit_cost
			pkg_type_totals[meal.rp_pkg.pkg_type]["total_qty_on_hand"] += qty_on_hand
			pkg_type_totals[meal.rp_pkg.pkg_type]["qty_needed"] += qty_needed
			pkg_type_totals[meal.rp_pkg.pkg_type]["total_cost"] += cost
	
		#process snack packaging
		for snack in snackRecipePkg:
				name = snack_name
				amt = snack.amt
				unit = snack.unit
				total_required = amt * snack_servings
				snack_rp_pkg = MealPlans.snack_r_num.rp_pkg
				packaging._package_type = RecipePackaging.pkg_type * qty_on_hand
		for recipe in recipeset:
			if s_r_num == recipe.r_num:
				ms_name = recipe.r_name
		for packaging in PkgQueryset:
				if unit == packaging.unit:
					qty_needed = qty_on_hand - snack_servings
					qty_on_hand = packaging.qty_on_hand
					pkg_type = snack.pkg_type
		if qty_on_hand >= snack_servings:
			qty_needed = qty_on_hand - snack_servings
			if (int(total_required or 0) - int(qty_needed or 0)) > 0:
				to_purchase = int(total_required or 0) - int(qty_on_hand or 0)
			else:
				to_purchase = 0
			if(int(total_required or 0) - int(qty_needed or 0)) > 0:
				to_purchase = int(total_required or 0) - int(qty_on_hand or 0)
			else:
				to_purchase = 0
				
			queryset.append({'id': count,
							'm_date:': m_date, 
		    				'name': name,
		    				'meal_name': meal_name, 
							'snack_name': snack_name, 
							'pkg_type': pkg_type, 
							'qty_on_hand': qty_on_hand, 
							'qty_needed': qty_needed,
							'total_required': total_required, 
							'to_purchase': to_purchase})
			count += 1

			cost = qty_needed * packaging.unit_cost
			pkg_type_totals[snack.rp_pkg.pkg_type]["qty_on_hand"] += qty_on_hand
			pkg_type_totals[snack.rp_pkg.pkg_type]["qty_needed"] += qty_needed
			pkg_type_totals[snack.rp_pkg.pkg_type]["total_cost"] += cost

		serializer = PPLSerializer(queryset, many=True)
		print (serializer)
		return Response(serializer.data)
