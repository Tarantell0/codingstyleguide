from pagedown.widgets import PagedownWidget
from captcha.fields import CaptchaField
from django import forms
from django.utils.safestring import mark_safe


class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class AddConventionForm(forms.Form):
    
    #CHOICES = [('None', 'none'),
    #           (True, 'good practice'),
    #           (False, 'bad practice')]
 
    identifier_type = forms.CharField(label='Title for Naming', widget=forms.TextInput(attrs={'placeholder':'Write only one post per guideline. Be precise.'}))
    #Deprecated since 19. January,  because readability conflicts
    #declaration = forms.CharField(widget=PagedownWidget(), label='Declaration', required=False)
    rules_for_naming = forms.CharField(widget=PagedownWidget(attrs={'placeholder':'Here is the place for your guideline: standard, description, convention, technique, rule, etc.'}), label='Rules for Naming', required=False)
    language_tag = forms.CharField(label='Which language is your guideline?', widget=forms.TextInput(attrs={'placeholder':'Add only one programming language per guideline.'}), required=True)
    #Deprecated since 19. January, because a description could have bad or good code practices


class EditConventionForm(forms.Form):
    
    #title = forms.CharField(
    #declaration = forms.CharField(widget=PagedownWidget(), label='Declaration', required=False)
    title = forms.CharField(required=False)
    rules_for_naming = forms.CharField(widget=PagedownWidget(), label='Guideline', required=False)
    pass


class SignupForm(forms.Form):
    username = forms.CharField(error_messages={'required': 'This field is required.'})
    email = forms.EmailField(required=False, error_messages={'invalid': 'Enter a valid email.'})
    password = forms.CharField(widget=forms.PasswordInput, error_messages={'required': 'This field is required.'})
    password_verify = forms.CharField(widget=forms.PasswordInput, error_messages={'required': 'This field is required.'})
    captcha = CaptchaField(error_messages={'required': 'This field is required.'})


