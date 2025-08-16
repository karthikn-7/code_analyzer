from rest_framework import serializers
from rest_framework_mongoengine import serializers as docsr
from .models import CodingQuestion,CodingResult
from django.contrib.auth.models import User

class ResultSerializer(docsr.DocumentSerializer):
    class Meta:
        model = CodingResult
        fields = ["user_id","question_id","submitted_code"]
        
   
    def validate_user_id(self,val):
        user = User.objects.filter(pk=val)
        if(user):
            return val
        raise serializers.ValidationError("User doesn't exists") 
    
class CreateQuestionSerializer(docsr.DocumentSerializer):
    class Meta:
        model = CodingQuestion
        fields = ["user_id"]
        
    def validate_user_id(self,val):
        user = User.objects.filter(pk=val)
        if(user):
            return val
        raise serializers.ValidationError("User doesn't exists")