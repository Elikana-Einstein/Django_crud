from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile,FriendRequest
from .forms import ProfileForm,friendRequestForm
from django.db.models import Q
# Create your views here.
@login_required
def profile_view(request,username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'friends/view_friendsprofile.html', {'profile': profile, 'user': user})
@login_required
def view_your_profile(request):
    profile = get_object_or_404(Profile,user=request.user)
    friend_requests = FriendRequest.objects.filter(Q(sender=request.user) | Q(receiver=request.user))

    # Get profiles of all involved users
    profiles = [
    req.sender.profile for req in friend_requests if req.sender != request.user
    ] + [
    req.receiver.profile for req in friend_requests if req.receiver != request.user
    ]

    # Remove duplicate profiles if needed
    unique_profiles = list(set(profiles))
   
    return render(request,'friends/profile.html',{'profile': profile,'profiles':unique_profiles ,'user': request.user})

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user) 

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
    current_user = request.user
    users = User.objects.exclude(id=current_user.id)  # Exclude the current user from the list
    user_data = []
    for user in users:
        try:
            # Check if request exists (sent or received)
            sent_request = FriendRequest.objects.filter(sender=current_user, receiver=user).first()
            received_request = FriendRequest.objects.filter(sender=user, receiver=current_user).first()

        except FriendRequest.DoesNotExist:
            friend_request = None

        user_data.append({
            'user': user,
            'sent_request': sent_request,
            'received_request': received_request
        })


    
    return render(request, 'friends/friends_list.html', {'users': user_data})

@login_required
def add_friend(request,user_name):
    if request.method == 'POST':
        user = get_object_or_404(User, username=user_name)
        # Check if the user is already a friend
        if FriendRequest.objects.filter(sender=request.user, receiver=user).exists() or FriendRequest.objects.filter(sender=user, receiver=request.user).exists():
            return redirect('friends:list_friends')
        friendship =FriendRequest(sender=request.user, receiver=user,status='pending')
        friendship.save()
    
    else:
        return redirect('friends:list_friends')
    
    return redirect('friends:list_friends')

@login_required
def accept_friend_request(request, user_name):
    if request.method == 'POST':
        user = get_object_or_404(User, username=user_name)
        friend_request = get_object_or_404(FriendRequest, sender=user, receiver=request.user)
        friend_request.status = 'accepted'
        friend_request.save()
    return redirect('friends:list_friends')
@login_required
def reject_friend_request(request, user_name):
    if request.method == 'POST':
        user = get_object_or_404(User, username=user_name)
        friend_request = get_object_or_404(FriendRequest, sender=user, receiver=request.user)
        friend_request.delete()
    return redirect('friends:list_friends')