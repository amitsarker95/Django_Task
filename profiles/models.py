from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from .utils import get_random_code
from django.db.models import Q

class ProfileManager(models.Manager):
    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = set([])
        for rel in qs:
            if rel.status == "accepted":
                accepted.add(rel.receiver)
                accepted.add(rel.sender)

        print(accepted)
        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        return available
    
    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(models.Model):
    fast_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='images/', blank=True, null=True)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def get_friends(self):
        return self.friends.all()

    def get_total_friends(self):
        return self.friends.all().count()

    def __str__(self):
        return f"{self.user.username}--{self.created.strftime('%d-%m-%Y')}"

    def save(self, *args, **kwargs):
        ex = False
        if self.fast_name and self.last_name:
            to_slug = slugify(str(self.fast_name)+ " " + str(self.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


STATUS_CHOICES =(
        ('send', 'send'),
        ('accepted', 'accepted'),
    )


class RelationshipManager(models.Manager):
    def invatations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs
    # Relationship.objects.invatations_received(myprofile)

class Relationship(models.Model):
    
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="receiver")
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self) -> str:
        return f"{self.sender}--{self.receiver}--{self.status}"


