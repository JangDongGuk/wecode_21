import json
from django.views import View
from django.http  import JsonResponse
from .models import Owner, Dog
class OwnerView(View):
    def get(self, request):
        owners = Owner.objects.all()
        
        result = []
        for owner in owners:
            dogs = owner.dog_set.all()
            dogs_list = []
            for dog in dogs:
                dog_info = {
                    'name': dog.name,
                    'age' : dog.age
                }
                dogs_list.append(dog_info)
                
            owner_info = {
                'email': owner.email,
                'name' : owner.name,
                'age'  : owner.age,
                'dogs' : dogs_list
            }
            result.append(owner_info)
            
        return JsonResponse({'result': result}, status=200)
    
    def post(self, request): 
        try:
            data = json.loads(request.body)
        
            Owner.objects.create(name=data['name'], age=data['age'], email=data['email'])
        
            return JsonResponse({'message': 'SUCCESS'}, status=200)
       
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status=400)

class DogView(View):
    def get(self, request):
        dogs = Dog.objects.all()
        
        result = []
        for dog in dogs:
            dog_info = {
                'owner': dog.owner.name,
                'name' : dog.name,
                'age'  : dog.age
            }
            result.append(dog_info)
            
        return JsonResponse({'result': result}, status=200)
    
    
    
    
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            owner = Owner.objects.get(email=data['owner'])
            
            Dog.objects.create(name=data['name'], age=data['age'], owner=owner)
            
            
            #dog = Dog.objects.get(id=1)
            
            #dog.owner.name
            
            #Owner.objects.get(id= dog.owner_id).name
            
            return JsonResponse({'message': 'SUCCESS'}, status=201)
         
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)
        
        except Owner.DoesNotExist:
            return JsonResponse({'message':'USER DOES NOT EXIST'}, status=400)
             