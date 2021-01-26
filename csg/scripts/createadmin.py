#!/usr/bin/env python

from django.contrib.auth.models import User
if User.objects.count() == 0:
    admin = User.objects.create(username='loop')
    admin.set_password('TD82megaR1L')
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()
