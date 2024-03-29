from .helperfuncs import execute_query
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework import status
from django.db.models import Prefetch
from django.db import IntegrityError
from .models import Packaging, PackagingUsages, Supplier, PackagingTypes, PackagingTypeSizes
from .SupplierViews import SupplierSerializer
import os
import logging
logging.basicConfig(level = logging.WARNING)

class PackagingTypeSerializer(ModelSerializer):
    class Meta():
        model = Packaging
        fields = ('packaging_type',)


class PackagingUsageSerializer(ModelSerializer):
    class Meta():
        model = PackagingUsages
        depth = 1
        fields = ('used_date', 'used_qty')


class PackagingSizeSerializer(ModelSerializer):
    class Meta():
        model = PackagingTypeSizes
        depth = 1
        fields = ('pkg_size_id', 'pkg_size', 'pkg_holds')


class PackagingTypeSerializer(ModelSerializer):
    pkg_sizes = PackagingSizeSerializer(required=False, many=True)
    
    def create(self, validated_data):
        curr_type = PackagingTypes.objects.create(**validated_data)
        return curr_type
            
    def update(self, type_inst, validated_data):
        pkg_sizes = validated_data.pop('pkg_sizes')
        old_sizes = PackagingTypeSizes.objects.filter(pkg_type_fk = type_inst)
        old_sizes.delete()
        for size in pkg_sizes:
            size['pkg_type_fk'] = type_inst
            PackagingTypeSizes.objects.create(**size)
        return super().update(type_inst, validated_data)            
    
    class Meta():
        model = PackagingTypes
        fields = ('pkg_type_id', 'pkg_type', 'pkg_sizes')
        

class PackagingDefView(ModelViewSet):
    queryset = PackagingTypes.objects.all()
    serializer_class = PackagingTypeSerializer

    def create(self, request):
        ret = None
        try:
            ret = super().create(request)
        except IntegrityError:
            return Response({'errorText': 'There already exists an packaging definition with that name.'}, 400)
        return ret

    def update(self, request, *args, **kwargs):
        ret = None
        try:
            ret = super().update(request, *args, **kwargs)
        except IntegrityError:
            return Response({'errorText': 'Error in one of your inputs! Please try again.'}, 400)
        return ret
        

class PackagingInvSerializer(ModelSerializer):
    psupplier = SupplierSerializer(read_only=True)
    pref_psupplier = SupplierSerializer(read_only=True)
    psupplier_id = serializers.IntegerField(allow_null=True)
    pref_psupplier_id = serializers.IntegerField(allow_null=True)
    packaging_usage = PackagingUsageSerializer(required=False, allow_null=True, many=True)
    class Meta():
        model = Packaging
        fields = ('p_id', 'package_type', 'unit_qty', 'qty_holds', 'unit', 'returnable', 'in_date', 'in_qty', 'packaging_usage', 'qty_on_hand', 'unit_cost', 'flat_fee', 'psupplier_id', 'pref_psupplier_id', 'psupplier', 'pref_psupplier')

    def create(self, validated_data):
        # raise serializers.ValidationError("IM HERE")
        pkg_usage = validated_data.pop('packaging_usage')
        pkg_instance = Packaging.objects.create(**validated_data)
        used = 0
        if pkg_usage:
            # IngredientUsages.objects.all().filter(used_ing = instance).delete()
            for usage in pkg_usage:
                used += int(usage['used_qty'])
                if (PackagingUsages.objects.count() > 0):
                    latest_id = PackagingUsages.objects.latest('p_usage_id').p_usage_id + 1
                else:
                    latest_id = 0
                usage['p_usage_id'] = latest_id
                usage['used_pkg_id'] = validated_data.get('p_id')
                # raise serializers.ValidationError(usage)
                PackagingUsages.objects.create(**usage)
        in_qty = getattr(pkg_instance, 'in_qty')
        setattr(pkg_instance, 'qty_on_hand', in_qty)
        pkg_instance.save()
        return pkg_instance
        
    def update(self, pkg_instance, validated_data):
        # raise serializers.ValidationError("IM HERE")
        pkg_usage = validated_data.pop('packaging_usage')
        print(pkg_instance)
        # ing_instance = Ingredients.objects.create(**validated_data)
        used = 0
        # pkg_usages = PackagingUsages.objects.filter(used_ing = pkg_instance)
        # if pkg_usages:
        # 	for pkg in pkg_usages:
        # 		used += pkg.used_qty
        # used += pkg_usage['used_qty']
        # latest_id = PackagingUsages.object.latest('p_usage_id').p_usage_id + 1
        # pkg_usage['p_usage_id'] = latest_id
        # pkg_usage['used_pkg_id'] = pkg_instance
        # IngredientUsages.objects.create(**pkg_usage)
        PackagingUsages.objects.filter(used_pkg = pkg_instance).delete()
        if pkg_usage:
            # PackagingUsages.objects.filter(used_pkg = pkg_instance).delete()
            for usage in pkg_usage:
                used += int(usage['used_qty'])
                if (PackagingUsages.objects.count() > 0):
                    latest_id = PackagingUsages.objects.latest('p_usage_id').p_usage_id + 1
                else:
                    latest_id = 0
                usage['p_usage_id'] = latest_id
                usage['used_pkg_id'] = getattr(pkg_instance, 'p_id')
                # raise serializers.ValidationError(usage)
                PackagingUsages.objects.create(**usage)
        in_qty = validated_data['in_qty']
        validated_data['qty_on_hand'] =  in_qty - used
        return super().update(pkg_instance, validated_data)


# Create your views here.
class PackagingInvView(ModelViewSet):
    queryset = Packaging.objects.all().prefetch_related('packaging_usage')
    serializer_class = PackagingInvSerializer