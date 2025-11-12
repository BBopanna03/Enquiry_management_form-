from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import AccessControl
from rest_framework import generics

class Command(BaseCommand):
       help = 'Create fixed users with roles'

       def handle(self, *args, **kwargs):
           users = [
               {"email": "counsellors@gmail.com", "username": "counsellors", "password": "counsellors", "role": "counsellor"},
               {"email": "accounts@gmail.com", "username": "accounts", "password": "accounts", "role": "accounts"},
               {"email": "hr@gmail.com", "username": "hr", "password": "hr", "role": "hr"},
               {"email": "admin@gmail.com", "username": "admin", "password": "admin", "role": "admin"},
           ]

           for u in users:
               user, created = User.objects.get_or_create(username=u["username"], defaults={"email": u["email"]})
               user.email = u["email"]
               user.set_password(u["password"])
               user.save()
               AccessControl.objects.update_or_create(user=user, defaults={"role": u["role"]})

           self.stdout.write(self.style.SUCCESS('Users and roles set up!'))