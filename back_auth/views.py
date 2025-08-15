from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *
from .serializer import RegisterSerializer

class RegisterAPI(APIView):
    def post(self,request):
        
        try:
            user_details = request.data
            serializer = RegisterSerializer(data = user_details)
            if(serializer.is_valid()):
                serializer.save()
                return Response({"message":"user registered succesfully","user":serializer.data})
            return Response({"error":serializer.errors})
        except Exception as e:
            return Response({"error":e},status=HTTP_500_INTERNAL_SERVER_ERROR)
        
        
