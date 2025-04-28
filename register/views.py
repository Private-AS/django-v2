from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout

# Create an account
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/polls")
    else:
        form = RegistrationForm()
    return render(request, 'register/register.html', {"form": form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Log the user out before deleting the account
        user.delete()  # Delete the user account
        return redirect('home')  # Redirect to the home page
    return HttpResponse("Invalid request method.", status=405)