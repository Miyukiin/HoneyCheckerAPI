from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpRequest, JsonResponse
from .models import HoneyCheckerTable
import requests 
# Create your views here.


@api_view(['POST'])
def verify_honeyword(request:HttpRequest) -> dict:
    # Extract data from the request
    user_index:int = request.data.get('user_index')
    password_list:list = request.data.get('password_list')
    password_candidate:str = request.data.get('password_candidate')
    salt:str = request.data.get('salt')
    
    # Construct query to get the sugarword index of the user.
    try:
        query:object = HoneyCheckerTable.objects.get(user_random_index=user_index)
    except HoneyCheckerTable.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except HoneyCheckerTable.MultipleObjectsReturned:
        return JsonResponse({'error': 'Multiple records found for user'}, status=500)
    # Hash password_candidate

    try:
        # Hash Honey Passwords
        honeypassword_hasher_api_url = 'http://127.0.0.1:8002/honeypassword/hash_honeypasswords/'
        data = {"honeyword_list": [password_candidate], "salt": salt}
        
        try:
            response = requests.post(honeypassword_hasher_api_url, json=data)  # Call API with honeywordlist as honeywords
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to send data to the honeypassword hasher API: {str(e)}")
        
        response_text = response.json()
        honeyhash_list = response_text['honeyword_hashes'] 
        print(honeyhash_list)
        password_hash_candidate = honeyhash_list[0]
        
    except ValueError as e:
            raise Exception(f"Failed to parse JSON from the API response: {str(e)}")
    except KeyError as e:
        raise Exception(f"Missing expected key in the API response: {str(e)}")
    
    # Logic for honeychecker verification
    sugarword = password_list[int(query.user_sugarword_index)]
    if password_hash_candidate in password_list and sugarword != password_hash_candidate:
        result = {
                    'status': 'success', 
                    'isCorrect': True, 
                    'isHoneyword': True, 
                    'isSugarword': False
                }
        
    elif password_hash_candidate in password_list and sugarword == password_hash_candidate:
        result = {
                    'status': 'success', 
                    'isCorrect': True, 
                    'isHoneyword': True, 
                    'isSugarword': True
                }
        
    elif password_hash_candidate not in password_list and sugarword != password_hash_candidate:
        result = {
                    'status': 'success', 
                    'isCorrect': False, 
                    'isHoneyword': False, 
                    'isSugarword': False
                }

    return JsonResponse(result)


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

        return JsonResponse({
            'status': 'success',
            'message': f'HoneyCheckerTable entry created for user random index {user_index}',
            'user_random_index': honeychecker_entry.user_random_index,
            'user_sugarword_index': honeychecker_entry.user_sugarword_index
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
