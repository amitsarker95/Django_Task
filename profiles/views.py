from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Profile, Relationship
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home_view(request):
    user = request.user
    context = {
        'user' : user,

    }
    return render(request, 'home/home.html', context)
    # return HttpResponse("This is Home")
@login_required
def profile_view(request):
    
    profiles = Profile.objects.get(user=request.user)
    print('user',profiles)
    context = {
        'profiles' : profiles,
    }

    return render(request, 'profile/myprofile.html', context)
@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invatations_received(profile)

    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True
    
    context = {
        'qs' : results,
        'is_empty' : is_empty,
    }

    return render(request, 'profile/my_invites.html', context)



@login_required
def invite_profile_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)
    context = {
        'qs' : qs,
    }

    return render(request, 'profile/to_invite_list.html', context)

@login_required
def accept_request(request):
    if request.method == "POST":
        pk = request.POST['profile_pk']
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)

        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == "send":
            rel.status = "accepted"
            rel.save()
    try:
       return redirect('profile:my-invites-view')
    except:
        return redirect('my-invites-view')
        
def reject_request(request):
    pass


@login_required
def profile_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)
    context = {
        'qs' : qs,
    }

    return render(request, 'profile/profile_list.html', context)


class ProfileListView(ListView):
    model = Profile
    template_name = 'profile/profile_list.html'
    # context_object_name = 'qs'
    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)

        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hello"] = "Hello user"
        user = User.objects.get(username__iexact= self.request.user)
        profile = Profile.objects.get(user=user)
        # context['profile'] = profile
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_sender = []
        rel_receiver = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)

        for item in rel_s:
            rel_sender.append(item.sender.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False

        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context
    
@login_required
def send_invatation(request):
    if request.method == "POST":
        pk = request.POST['profile_pk']
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    redirect('profile:my-invites-view')

@login_required
def remove_friend(request):
    if request.method == "POST":
        pk = request.POST['profile_pk']
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get((Q(sender=sender) & Q(receiver=receiver) | Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    redirect('profile:my-invites-view')


    