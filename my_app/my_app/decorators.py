from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def role_required(*allowed_roles):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'role') and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return redirect('access_denied')  # Crée cette vue si besoin
        return _wrapped_view
    return decorator
