from rest_framework import serializers
from rest_framework_mongoengine import serializers as docsr
from .models import CodingQuestion,CodingResult
from django.contrib.auth.models import User

class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(required=False, allow_null=True)

    def validate(self, attrs):
        msg = attrs.get("message")
        print(msg)
        if not msg:
            raise serializers.ValidationError("message must be included")
        return attrs


class QuestionSerializer(docsr.DocumentSerializer):
    class Meta:
        model = CodingQuestion
        fields ="__all__"
    
    
    def validate_user_id(self, val):
        
        user = User.objects.filter(pk=val)
        if(user):
            # print(user)
            return val
        raise serializers.ValidationError("User doesn't exists")
    
    def validate_question(self,val):
        if not val:
            raise serializers.ValidationError("Question cannot be empty")
        

        print(val)
        question = CodingQuestion.objects.filter(question=val).count()>0
        print(question)
        if(question):
            print(question)
            raise serializers.ValidationError("Question already exist")
        return val
    
class ResultSerializer(docsr.DocumentSerializer):
    class Meta:
        model = CodingResult
        fields = "__all__"
        
        