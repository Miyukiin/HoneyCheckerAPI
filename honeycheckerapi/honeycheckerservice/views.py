from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import HoneyCheckerTable
# Create your views here.


@api_view(['POST'])
def verify_honeyword(request:HttpRequest) -> dict:
    # Extract data from the request
    user_index:int = request.data.get('user_index')
    password_list:list = request.data.get('password_list')
    password_candidate:str = request.data.get('password_candidate')
    
    # Construct query to get the sugarword index of the user.
    try:
        query:object = HoneyCheckerTable.objects.get(user_random_index=user_index)
    except HoneyCheckerTable.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    except HoneyCheckerTable.MultipleObjectsReturned:
        return Response({'error': 'Multiple records found for user'}, status=500)
    
    # Logic for honeychecker verification
    sugarword = password_list[int(query.user_sugarword_index)]
    if password_candidate in password_list and sugarword != password_candidate:
        result = {
                    'status': 'success', 
                    'isCorrect': True, 
                    'isHoneyword': True, 
                    'isSugarword': False
                }
        
    elif password_candidate in password_list and sugarword == password_candidate:
        result = {
                    'status': 'success', 
                    'isCorrect': True, 
                    'isHoneyword': True, 
                    'isSugarword': True
                }
        
    elif password_candidate not in password_list and sugarword != password_candidate:
        result = {
                    'status': 'success', 
                    'isCorrect': False, 
                    'isHoneyword': False, 
                    'isSugarword': False
                }

    return Response(result)


@api_view(['POST'])
def create_honeychecker_entry(request:HttpRequest):
    user_index = request.data.get('user_index')  # Random index of the user
    sugarword_index = request.data.get('sugarword_index')  # Passed in the request data

    try:
        # Create the HoneyCheckerTable entry
        honeychecker_entry = HoneyCheckerTable.objects.create(
            user_random_index=user_index,
            user_sugarword_index=sugarword_index
        )
        honeychecker_entry.save()

        return Response({
            'status': 'success',
            'message': f'HoneyCheckerTable entry created for user random index {user_index}',
            'user_random_index': honeychecker_entry.user_random_index,
            'user_sugarword_index': honeychecker_entry.user_sugarword_index
        })

    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)
