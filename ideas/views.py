from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Idea, Vote, Profile


# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('idea_list')  # Changed 'home' to 'idea_list'
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Update profile
@login_required
def update_profile(request):
    # Ensure profile exists, create if it doesn’t
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        bio = request.POST.get('bio', '').strip()
        profile_picture = request.FILES.get('profile_picture')

        if bio or profile_picture:  # Only save if there’s something to update
            profile.bio = bio
            if profile_picture:
                profile.profile_picture = profile_picture
            profile.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please provide a bio or profile picture.")

    return render(request, 'ideas/update_profile.html', {'profile': profile})


# User profile
@login_required
def user_profile(request):
    user_ideas = Idea.objects.filter(user=request.user)
    profile = request.user.profile  # Assumes profile exists
    return render(request, 'ideas/profile.html', {'user_ideas': user_ideas, 'profile': profile})


# Delete idea
@login_required
def delete_idea(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    if idea.user == request.user:
        idea.delete()
        messages.success(request, "Idea deleted successfully!")
        return redirect('profile')
    else:
        messages.error(request, "You can only delete your own ideas.")
        return redirect('idea_list')


# Signup view
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally log the user in after signup
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('idea_list')  # Redirect to idea_list instead of login
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


# Idea list
@login_required
def idea_list(request):
    ideas = Idea.objects.all().order_by('-votes')
    return render(request, 'ideas/idea_list.html', {'ideas': ideas})


# Submit a new idea
@login_required
def submit_idea(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if title and description:  # Ensure fields aren’t empty
            Idea.objects.create(user=request.user, title=title, description=description)
            messages.success(request, "Idea submitted successfully!")
            return redirect('idea_list')
        else:
            messages.error(request, "Title and description are required.")
    
    return render(request, 'ideas/submit_idea.html')


# Vote on an idea
@login_required
def vote_idea(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    existing_vote = Vote.objects.filter(user=request.user, idea=idea)

    if existing_vote.exists():
        return JsonResponse({"error": "You have already voted for this idea"}, status=400)

    Vote.objects.create(user=request.user, idea=idea)
    idea.votes += 1
    idea.save()
    return JsonResponse({"votes": idea.votes})


# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')

