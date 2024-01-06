from django.shortcuts import render, get_object_or_404, redirect

from .models import RentalBoyfriendAndGirlfriend, Review
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def rental_detail(request, rental_id):
    boyfriend = get_object_or_404(RentalBoyfriendAndGirlfriend, id=rental_id)
    reviews = Review.objects.filter(boyfriend_girlfriend=boyfriend).order_by('-created_at')
    return render(request, 'rentals/rental_detail.html', {'boyfriend': boyfriend, 'reviews': reviews})
@login_required(login_url='login')
def index(request):
    boyfriends = RentalBoyfriendAndGirlfriend.objects.all()
    return render(request, 'rentals/index.html', {'boyfriends': boyfriends})
def contact(request):
    return render(request, 'rentals/contact.html')
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'rentals/login.html', {'form': form})

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Signup successful. You are now logged in.')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'rentals/signup.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('index')
def submit_review(request, rental_id):
    if request.method == 'POST':
        boyfriend = get_object_or_404(RentalBoyfriendAndGirlfriend, id=rental_id)
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        # Check if the user has already submitted a review for this boyfriend
        existing_review = Review.objects.filter(user=request.user, boyfriend_girlfriend=boyfriend)
        if existing_review.exists():
            messages.warning(request, 'You have already submitted a review for this boyfriend.')
        else:
            # Create a new review
            Review.objects.create(user=request.user, boyfriend_girlfriend=boyfriend, comment=comment, rating=rating)
            messages.success(request, 'Review submitted successfully.')

    return redirect('rental_detail', rental_id=rental_id)