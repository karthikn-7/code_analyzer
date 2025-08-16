from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CodingQuestion, CodingResult

from langchain.schema import SystemMessage, HumanMessage

from langchain_groq import ChatGroq
from .serializer import  ResultSerializer, CreateQuestionSerializer
from dotenv import load_dotenv
import os
load_dotenv()

chat = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192", 
    temperature=0.7
)

        
class ResultAPI(APIView):
    def post(self,request):
        
        try:
            serializer = ResultSerializer(data = request.data)
            if serializer.is_valid():
                qid = request.data["question_id"]
                question = CodingQuestion.objects.with_id(qid)
                code = request.data["submitted_code"]
                
                system_message = SystemMessage(content=rf"""You are code analyzer bot, You just send
                                       response of user code analyze and send it as format: Overall Quality:(excellent|good|fair|poor)
                                        ,Strengths:(key_strengths),Areas for improvement:(key_issues). Dont send nothing more than this and
                                        if any other message not regarding to code comes to you send response as i couldn't help with
                                       this. Important don't send answers.""")
                
                # serializer.save()
                messages = [system_message,HumanMessage(content=rf"Prompt: The question is {question.question}, user code {code}")]
                response = chat(messages)
                print(response.content)
                serializer.validated_data["report"] = response.content
                serializer.save()
                return Response({'message':"Result submitted","result":response.content})
            return Response({"error":serializer.errors})
            
            
        except Exception as e:
            return Response({"error":str(e)})
        

class createQuestion(APIView):
    def post(self,request):
        
        try:
            serializer = CreateQuestionSerializer(data = request.data)
            if serializer.is_valid():
                system_message = SystemMessage(content=rf"""You are a coding question creating bot. You need to create one question for user
                                               based on their previous coding reports analyze user strength and weekness based on that create question.
                                               . If there's no prior reports create and base question. Important Just only the question, input, expected output nothing more than that. 
                                               No reply from you just create like question.
                                               Take reference format like this: 
                                               You are given a string `s` containing only digits 0-9. You need to group consecutive digits together and return the result as a list of strings.

                                                Example:
                                                ```
                                                Input: s = "12345"
                                                Output: ["123", "45"]
                                                ```
                                                Write a function to solve this problem.""")
                
                querys = CodingResult.objects(user_id=request.data["user_id"])
                reports = []
                for query in querys:
                    print(query)
                    print(query.report)
                    reports.append(query.report)
                    
                print(reports)
                 
                messages = [system_message,HumanMessage(content=rf"""Privious reports: {reports}""")]
                question = chat(messages)
                serializer.validated_data["question"] = question.content
                serializer.save()
                return Response({"message":"Question created succesfully","question":question.content})
            return Response({"error":serializer.errors})
        
        except Exception as e:
            return Response({"error":str(e)})