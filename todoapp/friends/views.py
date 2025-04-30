from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm
# Create your views here.
@login_required
def profile_view(request,username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'friends/view_friendsprofile.html', {'profile': profile, 'user': user})
@login_required
def view_your_profile(request):
    profile = get_object_or_404(Profile,user=request.user)
    return render(request,'friends/profile.html',{'profile': profile, 'user': request.user})

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user) 
    print(profile.bio)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('friends:my_profile')
    else:
        form = ProfileForm(instance=profile)
        
    return render(request, 'friends/view_profile.html', {'form': form, 'profile': profile})    

@login_required
def list_friends(request):
    users  = User.objects.exclude(id=request.user.id)
    return render(request, 'friends/friends_list.html', {'users': users})