from django.http import HttpResponse
from django.shortcuts import redirect


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not allowed to see this page')
                
        return wrapper
    return decorator

def dict_get_key(func):
    def wrapper():
        func()
        for key in img_dict:
            img_dict.get(key)
    return wrapper()