from rest_framework import serializers

class MonthlyDataSerializer(serializers.Serializer):
    month = serializers.CharField()
    count = serializers.IntegerField()
    
class MonthlyAvgSerializer(serializers.Serializer):
    month = serializers.CharField()
    monthly_data_avg = serializers.IntegerField()
    monthly_data_deleted_avg = serializers.IntegerField()
    combined_avg = serializers.IntegerField()
    
class DailyDataSerializer(serializers.Serializer):
    day = serializers.CharField()
    month = serializers.CharField()
    count = serializers.IntegerField()