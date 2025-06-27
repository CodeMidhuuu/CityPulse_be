from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CivicIssue, UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number']

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, phone_number=phone_number)
        return user
    
class CivicIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CivicIssue
        fields = ['id', 'user', 'category', 'custom_category', 'subject', 'description',
                  'media', 'location', 'latitude', 'longitude', 'status', 'reported_at']
        read_only_fields = ['status', 'reported_at', 'user']

    def validate(self, data):
        location = data.get('location')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if not location and (latitude is None or longitude is None):
            raise serializers.ValidationError("Either location address or both latitude and longitude must be provided.")
        
        category = data.get('category')
        custom_category = data.get('custom_category')
        
        if category == 'other' and not custom_category:
            raise serializers.ValidationError({
                'custom_category': "This field is required when category is 'other'."
            })
        
        if category != 'other' and custom_category:
            raise serializers.ValidationError({
                'custom_category': "This field should only be used when category is 'other'."
            })

        return data

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    reports = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'phone_number', 'reports']

    def get_reports(self, profile):
        issues = profile.user.issues.all().order_by('-reported_at')
        return CivicIssueSerializer(issues, many=True).data