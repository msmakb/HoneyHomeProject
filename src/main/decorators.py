from django.shortcuts import redirect


def isAuthenticatedUser(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group == 'Admin':
                    return redirect('Dashboard')
                g = str(group).split(' ')
                group = ''
                for i in g:
                    group += i
            return redirect(group +'Dashboard')
        else:
            return view_func(request, *args, **kwargs)
            
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('Unauthorized')
        return wrapper_func
    return decorator
