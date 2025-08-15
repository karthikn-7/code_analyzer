from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CodingQuestion, CodingResult

from langchain.schema import SystemMessage, HumanMessage

from langchain_groq import ChatGroq
from .serializer import MessageSerializer, QuestionSerializer, ResultSerializer
from dotenv import load_dotenv
import os
load_dotenv()

class ReportApi(APIView):
    
    def post(self,request):
        chat = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-8b-8192", 
            temperature=0.7
        )
        
        system_message = SystemMessage(content="""You are code analyzer bot, You just send
                                       response of user code analyze and send it as format: Overall Quality:(excellent|good|fair|poor)
                                        ,Strengths:(key_strengths),Areas for improvement:(key_issues). Dont send nothing more than this and
                                        if any other message not regarding to code comes to you send response as i couldn't help with
                                       this.""")
        
        serializer = MessageSerializer(data =request.data)
        if serializer.is_valid():
            messages = [system_message,HumanMessage(content=serializer.data["message"])]
            response = chat(messages)
            return Response({"user_message":serializer.data["message"],"llm_response":response.content})
        return Response({"error":serializer.errors})
    
    
class QuestionListCreateAPI(APIView):
    def post(self,request):
        try:
            
            serializer = QuestionSerializer(data =request.data)
            if (serializer.is_valid()):
                serializer.save()
                return Response({"message":"Question saved succesfully","question":serializer.data})
            
            return Response({"message":serializer.errors})
            
        except Exception as e:
            return Response({"error":e})
        
    
    def get(self,request):
        try:
            questions = CodingQuestion.objects.all()
            print(questions)
            serializer = QuestionSerializer(questions,many=True)
            if serializer.data:
                return Response({"questions":serializer.data})
            return Response({"message":serializer.errors})
            
        except Exception as e:
            return Response({"error":str(e)})
        
        
class ResultAPI(APIView):
    def post(self,request):
        
        try:
            serializer = ResultSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':"Result submitted","result":serializer.data})
            return Response({"error":serializer.errors})
            
            
        except Exception as e:
            return Response({"error":str(e)})