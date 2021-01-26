from django.test import TestCase
from django.contrib.auth.models import User
from django.forms import EmailField
from login.models import LoginInfo
from conventions.models import Convention, Favorite, Vote, Comment, Flag, Edit
from reputations.models import Reputation
from notifications.models import Notification
from django.core.urlresolvers import reverse

from tags.models import Tag

from datetime import date, datetime

class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="martha", 
                                             email="martha@mail.com", 
                                             password="random")

        self.user_two = User.objects.create_user(username="user_two", 
                                             email="martha@mail.com", 
                                             password="random")
        LoginInfo.objects.create(login=self.user_two, website='',location='')

        self.login_info = LoginInfo.objects.create(login=self.user,
                                                   website='',
                                                   location='')

        self.tag = Tag.objects.create(name="test tag",
                                      login=self.user)
        
        self.convention = Convention.objects.create(login=self.user,
                                                    title="test title",
                                                    description="test description",
                                                    tag=self.tag)

        self.favorite = Favorite.objects.create(convention=self.convention,
                                                login=self.user,
                                                favorite=True)

        self.vote = Vote.objects.create(up=True,login=self.user,convention=self.convention)

        self.reputation = Reputation.objects.create(login=self.user,points=101)

        self.notification = Notification.objects.create(convention=self.convention,
                                                        is_vote_up=True)
        self.notification.login.add(self.user)



    def test_frontpage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/.json')
        self.assertEqual(response.status_code, 200)

        self.convention.delete()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


#    def test_signup(self):
#        """
#        IMPORTANT: To test this view, it is necessary to delete the captcha form from forms.py
#        """
#        from mostachocase import views
#        url = '/join/'
#
#        self.client.login(username="martha", password="random")
#        response = self.client.get(url)
#        self.assertEqual(response.status_code,302)
#        self.assertRedirects(response, '/')
#        self.client.logout()
#
#        response = self.client.post(url,{'username':'cecilia','password':'random','password_verify':'random'})
#        self.assertEqual(response.status_code, 302)
#        self.assertRedirects(response, '/')
#        self.client.logout()
#
#        response = self.client.post(url,{})
#        self.assertTrue(response.context['have_error']) # Error should be This field is required.
#        self.assertEqual(response.status_code, 200)
#        self.assertEqual(response.context['form']['username'].errors,[u'This field is required.'])
#        self.assertEqual(response.context['form']['password'].errors,[u'This field is required.'])
#        self.assertEqual(response.context['form']['password_verify'].errors,[u'This field is required.'])
#
#        response = self.client.post(url,{'username':'123','password':'random','password_verify':'random'})
#        self.assertEqual(response.context['error_username'],'Invalid username, use at least 4 and not more than 12 characters.')
#        response = self.client.post(url,{'username':'123456789abcd','password':'random','password_verify':'random'})
#        self.assertEqual(response.context['error_username'],'Invalid username, use at least 4 and not more than 12 characters.')
#       
#        response = self.client.post(url,{'username':'123','password':'1234','password_verify':'1234'})
#        self.assertEqual(response.context['error_password'],'Invalid password, use at least 5 and not more than 20 characters.')
#        response = self.client.post(url,{'username':'123','password':'123456789abcdefghijkl','password_verify':'123456789abcdefghijkl'})
#        self.assertEqual(response.context['error_password'],'Invalid password, use at least 5 and not more than 20 characters.')
#
#        response = self.client.post(url,{'username':'123','password':'12345','password_verify':'abcde'})
#        self.assertEqual(response.context['error_password_verify'],"Your password doesn't match.")
#
#        response = self.client.post(url,{'username':'martha','password':'12345','password_verify':'12345'})
#        self.assertEqual(response.context['error_username'],"Username already taken.")
#        
#        response = self.client.post(url,{'username':'martha','email':'123','password':'12345','password_verify':'12345'})
#        self.assertEqual(response.context['form']['email'].errors, [u'Enter a valid email.'])
#
#        response = self.client.post(url,{'username':'1234','email':'1@2.com','password':'12345','password_verify':'12345'})
#        self.assertEqual(response.status_code, 302)
#        self.assertRedirects(response, '/')
#        self.client.logout()
#        
#        response = self.client.post(url,{'username':'123456789abc','password':'123456789abcdefghijk','password_verify':'123456789abcdefghijk'})
#        new_user = User.objects.get(username='123456789abc')
#        self.assertTrue(new_user)
#        new_user_lg_info = LoginInfo.objects.get(login=new_user)
#        self.assertTrue(new_user_lg_info)
#        reputation = Reputation.objects.get(login=new_user)
#        self.assertTrue(reputation)
#        self.assertEqual(reputation.points, views.PTS_WELCOME)
#
#        session = self.client.session
#        self.assertTrue(session['show_welcome_banner'])
#        self.assertEqual(response.status_code, 302)
#        self.assertRedirects(response, '/')
#        self.client.logout()


    def test_login_view(self):
        response = self.client.post('/login/?next=',{'username':'martha','password':'random'})
        self.assertRedirects(response, '/')
        self.client.logout()

        response = self.client.post('/login/?next=/hot',{'username':'martha','password':'random'})
        self.assertRedirects(response, '/hot')
        self.client.logout()

        response = self.client.post('/login/?next=/join/',{'username':'martha','password':'random'})
        self.assertRedirects(response, '/')
        self.client.logout()

        response = self.client.post('/login/?next=/somethingnonsense',{'username':'martha','password':'random'})
        self.assertEqual(response.status_code, 302)
        self.client.logout()

        url = '/login/'
        self.client.login(username="martha",password="random")
        response = self.client.get(url)
        self.assertRedirects(response, '/')

        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {'username':'martha','password':'random'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

       
        self.client.logout()
        self.user.is_active = False
        self.user.save()
        response = self.client.post(url, {'username':'martha','password':'random'})
        self.assertEqual(response.context['error_username'], "This user doesn't exist anymore.")
        self.assertEqual(response.status_code, 200)

        self.user.delete()
        response = self.client.post(url, {'username':'martha','password':'random'})
        self.assertEqual(response.context['error_message'], "Username or password incorrect.")
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.logout()       
        response = self.client.get('/logout/',follow=True)
        self.assertRedirects(response, '/')

        login = self.client.login(username="martha", password="random")
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_front_user(self):

        u = User.objects.create(username="cecilia",password="random")
        LoginInfo.objects.create(login=u,website='',location='')
        c2=Convention.objects.create(login=u,title="ti2",description="t2",tag=self.tag)
        c3=Convention.objects.create(login=self.user,title="ti3",description="t4",tag=self.tag)
        Vote.objects.create(up=True,login=self.user,convention=self.convention)
        Vote.objects.create(up=True,login=self.user,convention=self.convention)
        Vote.objects.create(up=True,login=self.user,convention=c3)
        Vote.objects.create(up=True,login=self.user,convention=c3)
        Vote.objects.create(up=True,login=self.user,convention=c2)
        Vote.objects.create(down=True,login=self.user,convention=self.convention)
        Vote.objects.create(down=True,login=self.user,convention=c3)
        Vote.objects.create(down=True,login=self.user,convention=c2)
        Vote.objects.create(down=True,login=self.user,convention=c2)
        Vote.objects.create(down=True,login=self.user,convention=c2)
        Vote.objects.create(down=True,login=self.user,convention=self.convention)

        self.assertEqual(Vote.objects.total_votes(c3),1)
        self.assertEqual(Vote.objects.total_votes(c2),-2)
        self.assertEqual(Vote.objects.total_votes(self.convention),1)

        url = '/user/%d/' % self.user.pk
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        
        self.client.login(username="martha",password="random")
        response = self.client.get(url)
        self.assertEqual(response.context['is_same_user'],True)
        
        [self.assertEqual(c.login.pk, self.user.pk) for c,v in response.context['conventions']]
        [self.assertEqual(f.login.pk, self.user.pk) for f,v in response.context['favorites']]
        self.assertEqual(response.context['reputation'],Reputation.objects.total(self.user))

        [self.assertEqual(v,Vote.objects.total_votes(c)) for c,v in response.context['conventions']]
        #[self.assertEqual(v,Vote.objects.total_votes(f)) for f,v in response.context['favorites']]
       
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.context['is_same_user'],False)
        
        response = self.client.get('/user/%d/' % u.pk)
        [self.assertEqual(c.login.pk, u.pk) for c,v in response.context['conventions']]

        self.user.is_active = False
        self.user.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        self.login_info.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_user_frontpage(self):
        url = '/user/%s/' % self.login_info.login.id
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

        # if user is not authenticated
        self.user.is_active = False
        self.user.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

        conventions = Convention.objects.filter(login=self.user)
        self.assertEqual(conventions[0].login, self.user)
        is_list = True if conventions else False
        self.assertEqual(is_list,True)

        favorites = Favorite.objects.filter(login=self.user)
        self.assertEqual(favorites[0].login, self.user)
        is_list = True if favorites else False
        self.assertEqual(is_list,True)

        # with not existing user
        self.user.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)
        
        # user deleted, empty conventions list
        conventions = Convention.objects.filter(login=self.user)
        is_list = True if conventions else False
        self.assertEqual(is_list,False)

         # user deleted, empty favorite list
        favorites = Favorite.objects.filter(login=self.user)
        is_list = True if favorites else False
        self.assertEqual(is_list,False)


    def test_edit_user(self):
        url = '/user/edit/%d/' % self.user.pk

        response = self.client.get(url)
        self.assertEqual(response.status_code,404)
        
        self.client.login(username="martha",password="random")
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        
        response = self.client.post(url,{'edit':'Change'})
        self.assertEqual(response.status_code,302)
        u_log = LoginInfo.objects.get(login=self.user)
        self.assertEqual(u_log.website,'')
        response = self.client.post(url,{'edit':'Change','website':'csg.com'})
        u_log = LoginInfo.objects.get(login=self.user)
        self.assertEqual(u_log.website,'http://csg.com')
        response = self.client.post(url,{'edit':'Change','website':''})
        u_log = LoginInfo.objects.get(login=self.user)
        self.assertEqual(u_log.website,'')
        response = self.client.post(url,{'edit':'Change','website':'http://csg.com'})
        u_log = LoginInfo.objects.get(login=self.user)
        self.assertEqual(u_log.website,'http://csg.com')
        response = self.client.post(url,{'edit':'Change','birthday':'1986-12-12'})
        u_log = LoginInfo.objects.get(login=self.user)
        self.assertEqual(u_log.birthday,date(1986,12,12))
        response = self.client.post(url,{'edit':'Change','birthday':'XXXXXX'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error_birthday'],'Ex. yyyy-mm-dd')
        response = self.client.post(url,{'edit':'Change','location':'nonsense'})
        self.assertEqual(response.status_code,302)
        u_log = LoginInfo.objects.get(login=self.user)
        self.assertEqual(u_log.location, 'nonsense')
        response = self.client.post(url,{'edit':'Change','location':''})
        u_log = LoginInfo.objects.get(login=self.user)
        self.assertEqual(u_log.location, '')
        response = self.client.post(url,{'edit':'Change','website':'myweb.com','birthday':'1986-01-13','location':'Ahuicales'})
        u_log = LoginInfo.objects.get(login=self.user)
        self.assertEqual(u_log.location, 'Ahuicales')
        self.assertEqual(u_log.birthday, date(1986,01,13))
        self.assertEqual(u_log.website, 'http://myweb.com')

        response = self.client.post(url, {'edit_mail':'Save'})
        self.assertEqual(response.status_code, 302)
        u_log = User.objects.get(username=self.user.username)
        self.assertEqual(u_log.email,'')
        response = self.client.post(url, {'edit_mail':'Save', 'email':'a@a.com'})
        u_log = User.objects.get(username=self.user.username)
        self.assertEqual(u_log.email,'a@a.com')
        response = self.client.post(url, {'edit_mail':'Save', 'email':'XXXXX'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error_mail'], 'Insert a valid email.')
        u_log = User.objects.get(username=self.user.username)
        self.assertEqual(u_log.email,'a@a.com')

        new_pass = "marthita"
        response = self.client.post(url, {'edit_log':'Change Password'})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['error_current_pw'],'All password inputs are required.')
        response = self.client.post(url, {'edit_log':'Change Password', 'new_pw':'something'})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['error_current_pw'],'All password inputs are required.')
        response = self.client.post(url,{'edit_log':'Change Password','current_pw':'random','new_pw':new_pass,'confirm_pw':new_pass})
        self.assertEqual(response.status_code,302)
        u_log = User.objects.get(username=self.user.username)
        self.client.logout()
        login = self.client.login(username=self.user.username, password='marthita')
        self.assertTrue(login)
        response = self.client.post(url,{'edit_log':'Change Password','current_pw':new_pass,'new_pw':'1234','confirm_pw':'1234'})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['error_pw'],'Password must at least 5 chars long.')
        response = self.client.post(url,{'edit_log':'Change Password','current_pw':new_pass,'new_pw':'12345','confirm_pw':'123467'})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['error_pw'],"Password doesn't match.")

        response = self.client.post(url,{'edit_log':'Change Password','current_pw':'otherthan','new_pw':'12345','confirm_pw':'123467'})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['error_pw'],"Password doesn't match.")

        response = self.client.post(url, {'delete':'Delete Account'}, follow=True)
        self.assertRedirects(response, reverse('frontpage'))
        u_log = User.objects.get(username=self.user.username)
        self.assertEqual(u_log.is_active, False)
        
        self.client.login(username="user_two",password="random")
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

        self.login_info.delete()
        self.assertEqual(response.status_code,404)
        
        self.client.logout()
        url = '/user/edit/%d/' % self.user_two.pk
        login = self.client.login(username="user_two",password="random")
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)


    def test_logininfo_age(self):
        self.login_info.birthday = date(1986,01,13)
        self.login_info.save()
        self.assertEqual(self.login_info.age(), 28)
        #self.login_info.birthday = date(1988,02,29) 
        #self.login_info.save()
 

    def test_notifications_user(self):
        n2=Notification.objects.create(convention=self.convention,is_comment=True)
        n2.login.add(self.user)
        n3=Notification.objects.create(convention=self.convention,is_vote_up=True)
        n3.login.add(self.user)
        n4=Notification.objects.create(convention=self.convention,is_remove_up=True)
        n4.login.add(self.user)
        n5=Notification.objects.create(convention=self.convention,is_vote_down=True)
        n5.login.add(self.user)
        n6=Notification.objects.create(convention=self.convention,is_remove_down=True)
        n6.login.add(self.user)
        n7=Notification.objects.create(convention=self.convention,is_edit=True)
        n7.login.add(self.user)

        login = self.client.login(username="martha",password="random")

        url = '/user/notifications/%d/' % self.user.id
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.context['notifications']),7)

        url = '/user/notifications/%d/' % self.user.id
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)
        
        self.client.login(username="user_two",password="random")
        self.assertEqual(response.status_code,404)
        self.client.logout()

        self.client.login(username="martha",password="random")
        url = '/user/notifications/10/' 
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

        # fail if the user is not the same as the logged
        login = self.client.login(username="user_two",password="random")
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

        self.client.logout()
        url = '/user/notifications/%d/' % self.user.id
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)


    def test_post_convention(self):
        url = '/post/guideline/'
        
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=%s' % url)

        login = self.client.login(username="martha", password="random")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(url, {'identifier_type':'12345',
                                          'rules_for_naming':'r0',
                                          'language_tag':self.tag.name})
        new=Convention.objects.get(title='12345')
        self.assertTrue(new)
        self.assertEqual(response.status_code,302)
        red_url = '/guideline/%d'%new.id
        self.assertRedirects(response, red_url)
       

        response = self.client.post(url)
        self.assertEqual(response.context['form']['identifier_type'].errors, [u'This field is required.'])
        self.assertEqual(response.context['form']['language_tag'].errors, [u'This field is required.'])
        
        response = self.client.post(url, {'identifier_type':'1234',
                                          'rules_for_naming':'r01234',
                                          'language_tag':self.tag.name})
        self.assertEqual(response.context['error_min_char'],'This title is too short.')
        
        response = self.client.post(url, {'identifier_type':'12345',
                                          'language_tag':'none'})
        self.assertTrue(response.context['wrn_lang'])


    def test_front_conventions_tagged(self):
        c2=Convention.objects.create(title="a",tag=self.tag,login=self.user)
        c2.creation_date=date(2014,02,20)
        c3=Convention.objects.create(title="b",tag=self.tag,login=self.user_two,creation_date=datetime(1987,12,12,01,01))
        c3.creation_date=date(2014,02,19)
        c4=Convention.objects.create(title="d",tag=self.tag,login=self.user,creation_date=datetime(1988,12,12,01,01))
        c4.creation_date=date(2014,02,18)
        c5=Convention.objects.create(title="c",tag=self.tag,login=self.user_two,creation_date=datetime(1989,12,12,01,01))
        c5.creation_date=date(2014,02,17)
        
        v2=Vote.objects.create(up=True,convention=c4,login=self.user)
        v3=Vote.objects.create(up=True,convention=c4,login=self.user)
        v4=Vote.objects.create(up=True,convention=c4,login=self.user)
        v5=Vote.objects.create(up=True,convention=c3,login=self.user)
        v5=Vote.objects.create(up=True,convention=c2,login=self.user)
        v5=Vote.objects.create(up=True,convention=c2,login=self.user)
        Favorite.objects.create(login=self.user,convention=c4,favorite=True)
        
        r2=Reputation.objects.create(points=106,login=self.user)

        
        #c2.save()
        #c3.save()
        #c4.save()
        #c5.save()

        url = '/guidelines/language/%d/' % self.tag.id
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        
        #zip( convention, reputation, votes )
        response = self.client.get("%s%s" % (url,'?sort=date&page=1'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['language'],'test tag')
        self.assertEqual(response.context['sort'], 'date')
        #self.assertEqual(response.context['conventions'][0][0],self.convention) 
        #self.assertEqual(response.context['conventions'][2][0],c3) 
        #self.assertEqual(response.context['conventions'][4][0],c5) 

        response = self.client.get("%s%s" % (url,'?sort=title'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['language'],'test tag')
        self.assertEqual(response.context['sort'], 'title')
        #self.assertEqual(response.context['conventions'][0][0],c2) 
        #self.assertEqual(response.context['conventions'][1][0],c3) 
        #self.assertEqual(response.context['conventions'][2][0],c5)

        response = self.client.get("%s%s" % (url,'?sort=up_votes'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['language'],'test tag')
        self.assertEqual(response.context['sort'], 'up_votes')
        #self.assertEqual(response.context['conventions'][0][0],c4) 
        #self.assertEqual(response.context['conventions'][1][0],c2) 
        #self.assertEqual(response.context['conventions'][2][0],self.convention)

        response = self.client.get("%s%s" % (url,'?sort=down_votes'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['language'],'test tag')
        #self.assertEqual(response.context['sort'], 'down_votes')
        #self.assertEqual(response.context['conventions'][0][0],c5) 
        #self.assertEqual(response.context['conventions'][1][0],self.convention) 
        #self.assertEqual(response.context['conventions'][2][0],c3)

        response = self.client.get("%s%s" % (url,'?sort=hot'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['language'],'test tag')
        self.assertEqual(response.context['sort'], 'hot')

        self.client.login(username="martha",password="random")
        response = self.client.get("%s%s" % (url,'?sort=favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['language'],'test tag')
        self.assertEqual(response.context['sort'], 'favorites')
        self.assertEqual(response.context['conventions'][0][0],self.convention) 
        self.assertEqual(response.context['conventions'][1][0],c4) 
        
        self.assertEqual(response.context['conventions'][0][1],207)

        self.tag.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)


    def test_perma_convention(self):

        c1=Comment.objects.create(login=self.user,convention=self.convention,comment="c1")
        
        url = '/guideline/%d/' % self.convention.id
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['comments'][0].convention,self.convention)
        self.assertEqual(response.context['convention'],self.convention)
        self.assertEqual(response.context['reputation'],101)
        self.assertEqual(response.context['total_votes'],1)
        self.assertEqual(response.context['is_flag'],False)
        
        self.client.login(username="martha",password="random")
        f1=Flag.objects.create(login=self.user,convention=self.convention,flag=True)
        url = '/guideline/%d/' % self.convention.id
        self.assertEqual(response.context['is_flag'],False)

        self.convention.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)


    def test_edit_convention(self):

       c2 = Convention.objects.create(title=self.convention.title,
                                      login=self.user,
                                      tag=self.tag)
       
       url = '/guideline/%d/edit/' % self.convention.pk
       response = self.client.get(url)
       self.assertEqual(response.status_code,302)
       self.assertRedirects(response, '/login/?next=%s'%url)
       
       self.client.login(username="martha",password="random")
       response = self.client.get(url)
       self.assertEqual(response.status_code,200)
       self.assertEqual(response.context['is_title_editable'],False)

       response = self.client.post(url)
       self.assertEqual(response.status_code,302)
       self.assertRedirects(response,'/guideline/%d'%self.convention.pk)
       self.assertFalse(Edit.objects.all().filter(convention=self.convention))

       response = self.client.post(url, {'rules_for_naming':'newd'})
       self.assertEqual(response.context['error_min_char'],"This guideline description is to short. Please add more information.")
       #self.assertEqual(response.status_code,302)
       #self.assertRedirects(response,'/guideline/%d'%self.convention.pk)
       #e=Edit.objects.all().filter(convention=self.convention,login=self.user)[0]
       #self.assertEqual(e.description,'newd')
       #self.assertEqual(e.title,self.convention.title)
       #self.assertEqual(e.description,'newd')
       #e.delete()

       #response = self.client.post(url, {'title':'12345'})
       #self.assertEqual(response.context['is_title_editable'],False)
       #self.assertEqual(response.status_code,200)
       #self.assertFalse(Edit.objects.all())
       #self.assertEqual(response.context['error_min_char'],"This guideline description is to short. Please add more information.")
       #response = self.client.post(url, {'title':'12345', 'description':'somethingnew'})
       #self.assertEqual(response.context['is_title_editable'],False)
       #self.assertEqual(response.status_code,200)
       #self.assertEqual(response.context['error_min_char'],"Sorry! Similar guideline existing, editing this title isn't permitted.")

       c2.delete()
       response = self.client.post(url, {'title':'1234'})
       self.assertEqual(response.status_code,200)
       self.assertEqual(response.context['error_min_char'],"This guideline description is to short. Please add more information.")

       
       response = self.client.post(url)
       self.assertEqual(response.status_code,302)
       self.assertRedirects(response,'/guideline/%d'%self.convention.pk)
       self.assertFalse(Edit.objects.all())

       response = self.client.post(url,{'title':self.convention.title,'rules_for_naming':self.convention.description})
       self.assertEqual(response.status_code,302)
       self.assertRedirects(response,'/guideline/%d'%self.convention.pk)
       self.assertFalse(Edit.objects.all())


       response = self.client.post(url,{'title':'12345','rules_for_naming':self.convention.description})
       self.assertEqual(response.status_code,302)
       self.assertRedirects(response,'/guideline/%d'%self.convention.pk)
       self.assertTrue(Edit.objects.all())
       self.assertEqual(Edit.objects.all()[0].title,'12345')
       self.assertEqual(Edit.objects.all()[0].description,self.convention.description)
       Edit.objects.all().delete()

       response = self.client.post(url,{'title':self.convention.title,'rules_for_naming':'12345a'})
       self.assertEqual(response.status_code,302)
       self.assertRedirects(response,'/guideline/%d'%self.convention.pk)
       self.assertTrue(Edit.objects.all())
       self.assertEqual(Edit.objects.all()[0].title,self.convention.title)
       self.assertEqual(Edit.objects.all()[0].description,'12345a')
       Edit.objects.all().delete()

       response = self.client.post(url,{'title':self.convention.title,'rules_for_naming':'a'})
       self.assertEqual(response.status_code,200)
       self.assertEqual(response.context['error_min_char'],"This guideline description is to short. Please add more information.")


       Notification.objects.all().delete()
       self.client.login(username="martha",password="random")
       response = self.client.post(url, {'rules_for_naming':'12345'})
       self.assertEqual(response.status_code,302)
       self.assertRedirects(response,'/guideline/%d'%self.convention.pk)
       self.assertTrue(Edit.objects.all())
       self.assertEqual(Edit.objects.all()[0].title,self.convention.title)
       self.assertEqual(Edit.objects.all()[0].description, '12345')
       #self.assertTrue(Notification.objects.all().filter(convention=self.convention)[0].is_seen)
       Edit.objects.all().delete()

       #Notification.objects.all().delete()
       #self.client.login(username="martha",password="random")
       #response = self.client.post(url, {'title':'12345'})
       #self.assertEqual(response.status_code,302)
       #self.assertRedirects(response,'/guideline/%d'%self.convention.pk)
       #self.assertTrue(Edit.objects.all())
       #self.assertEqual(Edit.objects.all()[0].title,'12345')
       #self.assertFalse(Edit.objects.all()[0].description)
       #self.assertTrue(Notification.objects.all().filter(convention=self.convention)[0].is_seen)


    def test_revision_convention(self):


        url = '/guideline/900/revision/' 
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

        url = '/guideline/%d/revision/' % self.convention.id
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)


        e1=Edit.objects.create(title='t1',
                               login=self.user,
                               description="",
                               convention=self.convention,
                               tag=self.tag,
                               creation_date=date(2014,02,21))
        e1.save()


        url = '/guideline/%d/revision/' % self.convention.id
        response = self.client.get(url)
        self.assertEqual(response.context['edit'],e1)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['latest_title'],'t1')
        self.assertEqual(response.context['subversion'][0][3],2)
        
        e2=Edit.objects.create(title='t2',
                               login=self.user,
                               convention=self.convention,
                               description="d2",
                               tag=self.tag,
                               creation_date=date(2014,02,22))
        e2.save()
        url = '/guideline/%d/revision/' % self.convention.id
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        edits =  Edit.objects.all().filter(convention=self.convention)
        self.assertEqual(response.context['latest_title'],'t2')
        self.assertEqual(response.context['subversion'][0][3],3)


        e3=Edit.objects.create(login=self.user,
                               title="t3",
                               convention=self.convention,
                               description="",
                               tag=self.tag)
        e3.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        edits =  Edit.objects.all().filter(convention=self.convention)
        self.assertEqual(response.context['subversion'][0][3],4)


    def test_similar_convention(self):
        
        url = '/guideline/%d/similar/' % self.convention.id
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['no_similars_msg'],'This guideline has no similars.')

        c1 = Convention.objects.create(title=self.convention.title,tag=self.tag,login=self.user)
        
        v1 = Vote.objects.create(convention=self.convention,up=True,login=self.user)
        
        v2_1 = Vote.objects.create(convention=c1,up=True,login=self.user)
        v2_2 = Vote.objects.create(convention=c1,up=True,login=self.user)
        v2_3 = Vote.objects.create(convention=c1,up=True,login=self.user)
        
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.context['conventions']),2)
        self.assertEqual(response.context['conventions'][0][0],c1)
        self.assertEqual(response.context['conventions'][0][2],3)
        self.assertEqual(response.context['conventions'][1][2],2)

        Vote.objects.create(convention=self.convention,up=True,login=self.user)
        Vote.objects.create(convention=self.convention,up=True,login=self.user)
        Vote.objects.create(convention=c1,down=True,login=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.context['conventions']),2)
        self.assertEqual(response.context['conventions'][0][0],self.convention)
        self.assertEqual(response.context['conventions'][0][2],4)
        self.assertEqual(response.context['conventions'][1][2],2)


    def test_toggle_vote(self):

        url = '/toggle_vote/'
##The doppel comment is in case of getting data as request.POST.get('') and not
##request.POST['']
#        Raises an MultiValueDicKeyError       
#        response = self.client.post(url)
#        self.assertEqual(response.status_code, 302)
#        self.assertRaises(MultiValueDictKeyError)
#        
#        response = self.client.post(url, {'convention_id':self.convention.id,'down_vote':'true','up_vote':'false'})
#        self.assertEqual(response.status_code, 302)
#        self.assertRedirects(response, '/')
#        self.client.logout()
#        
#        Raises an MultiValueDicKeyError       
#        response = self.client.post(url, {'convention_id':self.convention.id})
#        self.assertEqual(response.status_code, 302)
#        self.assertRedirects(response, '/')
#
#        Raises an MultiValueDicKeyError       
#        response = self.client.post(url, {'up_vote':True})
#        self.assertEqual(response.status_code, 302)
#        self.assertRedirects(response, '/')
#    
#        Raises an MultiValueDicKeyError       
#        response = self.client.post(url, {'down_vote':True})
#        self.assertEqual(response.status_code, 302)
#        self.assertRedirects(response, '/')

        response = self.client.post(url, {'convention_id':self.convention.id,'down_vote':'true','up_vote':'false'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        
        self.client.login(username="martha",password="random")

        # accessing as same user and same convention writter
        self.notification.delete()
        response = self.client.post(url, {'convention_id':self.convention.id,'down_vote':'true','up_vote':'false'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        self.client.logout()

        self.client.login(username=self.user_two.username,password='random')
        response = self.client.post(url, {'convention_id':self.convention.id,'down_vote':'false','up_vote':'true'})
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response, '/guideline/%d' % self.convention.id)
        
        Reputation.objects.create(login=self.user_two,points=10)
        self.client.login(username=self.user_two.username,password='random')
        response = self.client.post(url, {'convention_id':self.convention.id,'down_vote':'false','up_vote':'true'})
        self.assertEqual(response.status_code,200)
        self.assertTrue(Vote.objects.get(convention=self.convention,up=True,down=False,login=self.user_two))
        self.assertTrue(Notification.objects.get(is_vote_up=True,convention=self.convention,login=self.user))
        self.assertTrue(Reputation.objects.get(points=5,convention=self.convention,login=self.user))

        response = self.client.post(url, {'convention_id':self.convention.id,'down_vote':'false','up_vote':'true'})
        self.assertEqual(response.status_code,200)
        self.assertFalse(Vote.objects.all().filter(convention=self.convention,up=True,down=False,login=self.user_two))
        self.assertTrue(Notification.objects.all().filter(is_remove_up=True,convention=self.convention,login=self.user))
        self.assertFalse(Reputation.objects.all().filter(points=5,convention=self.convention,login=self.user))

        Reputation.objects.create(login=self.user_two,points=30)
        self.client.login(username=self.user_two.username,password='random')
        response = self.client.post(url, {'convention_id':self.convention.id,'down_vote':'true','up_vote':'down'})
        self.assertEqual(response.status_code,200)
        self.assertTrue(Vote.objects.get(convention=self.convention,up=False,down=True,login=self.user_two))
        self.assertTrue(Notification.objects.get(is_vote_down=True,convention=self.convention,login=self.user))
        self.assertTrue(Reputation.objects.get(points=-2,convention=self.convention,login=self.user))

        response = self.client.post(url, {'convention_id':self.convention.id,'down_vote':'true','up_vote':'down'})
        self.assertEqual(response.status_code,200)
        self.assertFalse(Vote.objects.all().filter(convention=self.convention,up=False,down=True,login=self.user_two))
        self.assertTrue(Notification.objects.all().filter(is_remove_down=True,convention=self.convention,login=self.user))
        self.assertFalse(Reputation.objects.all().filter(points=-2,convention=self.convention,login=self.user))
        
        self.client.login(username=self.user_two.username,password='random')
        response = self.client.post(url, {'convention_id':self.convention.id,'down_vote':'false','up_vote':'true'})
        self.assertEqual(response.status_code,200)
        self.assertTrue(Vote.objects.get(convention=self.convention,up=True,down=False,login=self.user_two))
        self.assertTrue(Notification.objects.get(is_vote_up=True,convention=self.convention,login=self.user))
        self.assertTrue(Reputation.objects.get(points=5,convention=self.convention,login=self.user))
        
        self.client.login(username=self.user_two.username,password='random')
        response = self.client.post(url, {'convention_id':self.convention.id,'down_vote':'true','up_vote':'down'})
        self.assertEqual(response.status_code,200)
        self.assertTrue(Vote.objects.get(convention=self.convention,up=False,down=True,login=self.user_two))
        self.assertTrue(Notification.objects.get(is_vote_down=True,convention=self.convention,login=self.user))
        self.assertTrue(Reputation.objects.get(points=-2,convention=self.convention,login=self.user))

        response = self.client.get('/toggle_vote/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/')


    def test_toggle_favorite(self):
        url = '/toggle_favorite/'
        # if existing more than two favorites
        self.client.login(username="martha",password="random")
        Favorite.objects.create(convention=self.convention,login=self.user,favorite=True)

        response= self.client.post(url,{'convention_id':self.convention.id,'favorite':"true"})
        self.assertFalse(Favorite.objects.all().filter(convention=self.convention,login=self.user))
        self.client.logout()
        
        self.favorite.delete()
        response= self.client.post(url,{'convention_id':self.convention.id,'favorite':"true"})
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,'/')

        self.client.login(username="martha",password="random")
        response= self.client.post(url,{'convention_id':self.convention.id,'favorite':"true"})
        self.assertTrue(Favorite.objects.get(convention=self.convention,favorite=True,login=self.user))

        self.client.login(username="martha",password="random")
        response= self.client.post(url,{'convention_id':self.convention.id,'favorite':"true"})
        self.assertFalse(Favorite.objects.all().filter(convention=self.convention,login=self.user))
        
        response = self.client.get('/toggle_favorite/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/')

    def test_toggle_comment(self):
        self.notification.delete()
        url = '/toggle_comment/'
        response = self.client.post(url, {'convention_id':self.convention.pk,'comment':'c1'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/login/?next=/guideline/%d/'% self.convention.pk)

        self.client.login(username="martha",password="random")
        response = self.client.post(url, {'convention_id':self.convention.pk})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/guideline/%d' % self.convention.pk)

        response = self.client.post(url, {'convention_id':333})
        self.assertEqual(response.status_code, 404)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/')

        response = self.client.post(url, {'convention_id':self.convention.pk,'comment':'c1'})
        self.assertTrue(Comment.objects.get(convention=self.convention,login=self.user,comment='c1'))
        self.assertFalse(Notification.objects.all().filter(convention=self.convention))
        
        u1 = User.objects.create_user(username="u1",password="random")
        u2 = User.objects.create_user(username="u2",password="random")
        u3 = User.objects.create_user(username="u3",password="random")
        c1 = Comment.objects.create(login=u1,convention=self.convention,comment="c10")
        c2 = Comment.objects.create(login=u2,convention=self.convention,comment="c11")
        c3 = Comment.objects.create(login=u3,convention=self.convention,comment="c12")

        response = self.client.post(url, {'convention_id':self.convention.pk,'comment':'c2'})
        self.assertTrue(Comment.objects.get(convention=self.convention,login=self.user,comment='c2'))
        notifications=Notification.objects.all().filter(convention=self.convention)
        self.assertTrue(notifications)
        self.assertEqual(len(notifications[0].login.all()),3)
        self.assertEqual(notifications[0].login.all()[0],u1)
        self.assertEqual(notifications[0].login.all()[1],u2)
        self.assertEqual(notifications[0].login.all()[2],u3)
        self.client.logout()

        self.client.login(username="u1",password="random")
        response = self.client.post(url, {'convention_id':self.convention.pk,'comment':'c3'})
        self.assertTrue(Comment.objects.get(convention=self.convention,login=u1,comment='c3'))
        notifications_2=Notification.objects.all().filter(convention=self.convention)
        self.assertTrue(notifications_2)
        self.assertEqual(len(notifications_2[1].login.all()),3)
        self.assertEqual(notifications_2[1].login.all()[0],self.user)
        self.assertEqual(notifications_2[1].login.all()[1],u2)
        self.assertEqual(notifications_2[1].login.all()[2],u3)
        self.client.logout()


    def test_toggle_delete_comment(self):
        self.notification.delete()
        url = '/toggle_delete_comment/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/')

        u1 = User.objects.create_user(username="u1",password="random") 
        u2 = User.objects.create_user(username="u2",password="random") 
        c1 = Comment.objects.create(comment="c1",convention=self.convention,login=u1)
        c2 = Comment.objects.create(comment="c2",convention=self.convention,login=u1)
        n1 = Notification.objects.create(is_comment=True,convention=self.convention,supporter=u1)
        n1.login.add(self.user)
        n2 = Notification.objects.create(is_comment=True,convention=self.convention,supporter=u1)
        n2.login.add(self.user)

        response = self.client.post(url,{'comment_id':c1.pk})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/login/?next=/guideline/%d/' % self.convention.pk)

        login = self.client.login(username=self.user.username, password="random")
        response = self.client.post(url,{'comment_id':c1.pk})
        self.assertFalse(Comment.objects.all().filter(id=c1.pk))

        
    def test_toggle_rm_welcome(self):
        url = '/toggle_rm_welcome/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.client.login(username="martha", password="random")
        session = self.client.session
        response = self.client.post(url)
        self.assertFalse(session['show_welcome_banner'])


    def test_search(self):
        url = '/search/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


    def test_hot_conventions(self):
        url = '/hot/'
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        
        self.convention.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_unvoted(self):
        self.vote.delete()
        url = '/unvoted/'
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(Vote.objects.total_votes(convention=self.convention),0)
        
        self.convention.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_favorites(self):
        self.favorite.delete()
        url = '/favorites/'
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

        self.client.login(username="martha", password="random")
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertFalse(Favorite.objects.filter(login=self.user))

        Favorite.objects.create(convention=self.convention,login=self.user,favorite=True)
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTrue(Favorite.objects.filter(login=self.user))


    def test_flag(self):
        url = '/flag/'
        response = self.client.get(url)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response, '/')

        reponse = self.client.post(url,{'convention_id':66666})
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response, '/')
        
        self.client.logout()
        reponse = self.client.post(url,{'convention_id':self.convention.pk})
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response, '/')


    def test_users(self):
        u1 = User.objects.create_user(username="u1",password="random")
        li = LoginInfo.objects.create(website="www.",login=u1,location="Matamor")
        self.login_info.delete()
        url = '/users/'
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_about(self):
        url = '/about/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)



#    def test_script(self):
#        from login.models import LoginInfo #, Login
#        from django.contrib.auth.models import User
#        from reputations.models import Reputation
#        from conventions.models import Convention
#        from tags.models import Tag
#
#        NUM_USRS = 1000
#        PWD = "asdf"
#        LANG = 100
#        from random import randint
#
#        u = 1 # 1 and not 0 because user 1 is my admin
#        for u in range(1,NUM_USRS):
#            id = "user%d" % (u + 1)
#            u = User.objects.create_user(username=id,password=PWD,email="email@mail.com")
#            LoginInfo.objects.create(login=u, website="", location=id)
#            Reputation.objects.create(login=u, points=11)
#
#        t = 0
#        for t in range(LANG):
#            tg = "tag%d" % (t+1)
#            u = User.objects.get(id=randint(2,NUM_USRS))
#            Tag.objects.create(name=tg,login=u)
#
#
#        p = 0
#        for p in range(NUM_USRS + 1):
#            i = 0
#            for i in range(p):
#                u = User.objects.get(id=p)
#                t = Tag.objects.get(id=randint(1,LANG))
#                post = "title %d_%d" % (p, i + 1)
#                description = "description %d_%d" % (p, i + 1)
#                Convention.objects.create(title=post,description=description,tag=t,login=u)
#            p + 1
#


