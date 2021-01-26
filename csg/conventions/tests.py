# coding=utf-8

from django.test import TestCase
#from django.test.client import Client
from django.contrib.auth.models import User
from conventions.models import Convention, Vote, Comment, Edit
from login.models import LoginInfo
from tags.models import Tag
from django.forms import CharField, EmailField
from notifications.models import Notification

import re

#resp.status_code
#resp.context
#resp.templates
#resp[<header name>]

class PostTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="martha", 
                                             email="martha@mail.com", 
                                             password="random")

        self.tag = Tag.objects.create(name='temp_tag',
                                      login=self.user)

        self.convention = Convention.objects.create(title='temp_title',
                                                   description='temp_description',
                                                   login=self.user,
                                                   tag=self.tag)

        self.vote = Vote.objects.create(up=True,
                                        down=False,
                                        convention=self.convention,
                                        login=self.user)


        self.notification = Notification.objects.create(is_remove_up=True,
                                                        is_remove_down=False,
                                                        supporter=self.user,
                                                        convention=self.convention,
                                                        extra_info=self.convention.description[:200])

        self.comment = Comment.objects.create(login=self.user, 
                                              convention=self.convention, 
                                              comment="co")


        self.edit = Edit.objects.create(title="new title",
                                        description="new desc",
                                        login=self.user,
                                        tag=self.tag,
                                        convention=self.convention,
                                        latest=True)


        self.login_info = LoginInfo.objects.create(website='http://www.muugs.com',
                                                   location='Bad Staffelstein, Bamberg',
                                                   birthday='1986-01-01',
                                                   login=self.user)


    
    def test_response_no_auth(self):
        response = self.client.get('/post/guideline/')
        self.assertEqual(response.status_code, 302) # redirection status_code

    
    def test_perma_convention(self):
        url = '/guideline/%d/' % self.convention.id
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.convention.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_edit_convention(self):
        url = '/guideline/%d/edit/' % self.convention.id

        self.client.logout()
        response= self.client.get(url)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(url,follow=True)
        self.assertRedirects(response, '/login/?next=%s' % url)

        login = self.client.login(username="martha", password="random")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    
    def test_similar_convention(self):
        sim_con = Convention.objects.create(title=self.convention.title,
                                            tag=self.tag,
                                            description='not imp',
                                            login=self.user)

        url = '/guideline/%d/similar/' % self.convention.id
        response = self.client.get(url)
        print response.context['perms']
        self.assertEqual(response.status_code, 200)
        
        url = '/guideline/%d/similar/' % sim_con.id
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # no similars
        sim_con.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        self.convention.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    
    def test_search_machine(self):
        url = '/search/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_hot_conventions(self):
        url = '/hot/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.convention.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_unovoted(self):
        url = '/unvoted/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.convention.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_users(self):
        url = '/users/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_flag(self):
        url = '/flag/'
        response = self.client.get(url)
        self.assertRedirects(response, '/')

        #test with post

    def test_about(self):
        url = '/about/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
