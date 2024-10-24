from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect

# create is manager check decorator
def manager_required(view_func):
    # use built in django auth decorator to check if user is manager 
    @user_passes_test(lambda user: user.is_manager)
    # define wrapper function
    def wrapper(request, *args, **kwargs):
        # check if the user is a manager 
        if request.user.is_manager:
            # return to the view function
            return view_func(request, *args, **kwargs)
        else: 
            # if not return to home with error message
            messages.error(request, 'You Are Not authorized to access this page.')
            return redirect('core:home')
    # return the whole wrapper function
    return wrapper
