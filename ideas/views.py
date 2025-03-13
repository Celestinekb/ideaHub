from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Idea, Vote
from django.contrib.auth.forms import UserCreationForm
from .models import Idea
from .models import Profile



@login_required
def update_profile(request):
    profile = request.user.profile  # Fetch the latest profile

    if request.method == 'POST':
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')

        if bio:
            profile.bio = bio
        if profile_picture:
            profile.profile_picture = profile_picture

        profile.save()
        return redirect('profile')  # Redirect to profile page to see changes

    return render(request, 'ideas/update_profile.html', {'profile': profile})



@login_required
def user_profile(request):
    user_ideas = Idea.objects.filter(user=request.user)
    return render(request, 'ideas/profile.html', {'user_ideas': user_ideas})

@login_required
def delete_idea(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)

    if idea.user == request.user:  # Only allow the owner to delete
        idea.delete()
        return redirect('profile')
    else:
        return redirect('idea_list')  # Prevent unauthorized deletion


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def idea_list(request):
    if request.user.is_authenticated:
        # Display all ideas ranked by votes for logged-in users
        ideas = Idea.objects.all().order_by('-votes')
        return render(request, 'ideas/idea_list.html', {'ideas': ideas})
    else:
        # Show a "Please log in" message for non-authenticated users
        return render(request, 'ideas/idea_list.html', {'message': 'Please log in to view the ideas.'})

# Submit a new idea
@login_required
def submit_idea(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        if title and description:
            Idea.objects.create(user=request.user, title=title, description=description)
        return redirect('idea_list')

    return render(request, 'ideas/submit_idea.html')


# Voting functionality
from django.http import JsonResponse

@login_required
def vote_idea(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    existing_vote = Vote.objects.filter(user=request.user, idea=idea)

    if existing_vote.exists():
        return JsonResponse({"error": "You have already voted for this idea"}, status=400)

    Vote.objects.create(user=request.user, idea=idea)
    idea.votes += 1
    idea.save()

    return JsonResponse({"votes": idea.votes})  # Send back updated votes


