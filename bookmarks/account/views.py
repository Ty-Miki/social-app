from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact
from actions.models import Action
from actions.utils import create_action

# Create your views here.

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    # Display all actions by default.
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        # If user is follwing others, retrieve only their actions.
        actions = actions.filter(user_id__in= following_ids)
    
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    return render(request,
                  "account/dashboard.html",
                  {"section": "dashboard",
                   "actions": actions})

def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)

            # Add an action for account creation.
            create_action(user= new_user,
                          verb= "has created an account")
            
            return render(request,
                          "account/register_done.html",
                          {"new_user": new_user})

    else:
        user_form = UserRegistrationForm()

    return render(request,
                  "account/register.html",
                  {"user_form": user_form})

@login_required
def edit(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,
                             "Profile updated successfully")
        
        else:
            messages.error(request,
                           "Error updating your profile")
    
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                  "account/edit.html",
                  {"user_form": user_form, "profile_form": profile_form})

@login_required
def user_list(request: HttpRequest) -> HttpResponse:
    users = User.objects.filter(is_active=True)

    return render(request,
                  "account/user/list.html",
                  {"section": "people", "users": users})

@login_required
def user_detail(request: HttpRequest, username) -> HttpResponse:
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    
    return render(request,
                  "account/user/detail.html",
                  {"section":"people", "user": user})

@require_POST
@login_required
def user_follow(request: HttpRequest) -> HttpResponse:
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, 
                                              user_to=user)
                
                # Create an action for user follow.
                create_action(user=request.user,
                              verb="is following",
                              target= user)
                
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({"status": "ok"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error"})
    return JsonResponse({"status": "error"})
