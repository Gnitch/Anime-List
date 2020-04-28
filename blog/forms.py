from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django import forms
from .models import Post

choices_status = (
    ('1','Watched'),
    ('2','Watching'),
)

class PostForm(forms.ModelForm):

    class Meta :
        model = Post
        fields = ('title','imgLink','status')
        widgets = {
            'title': forms.TextInput(attrs={'id':'title','placeholder':'Enter Title'}),
            'imgLink':forms.Textarea(attrs={'id':'imgLink','placeholder':'Google Search for an Image of the Anime and paste the url'}),
            'status': forms.TextInput(attrs={'id':'status','placeholder':'Enter Status ("watching" or "watched" or "not watched")'}),
        }

        labels = {
            'title' : (''),
            'imgLink' : (''),
            'status' : (''),
        }

class UserSignUpForm(UserCreationForm):
 
    class Meta :
        model = User
        fields = ('username', 'email', 'password1', 'password2')       
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter Email'}),
        }
        labels = {
            'username' : (''),
            'email' : (''),
            'password1' : None,
            'password2' : None,
        }    
        help_texts = {
            'username': None,
            'email': None,
        } 
    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-Enter Password'})   
        self.fields['password2'].help_text = None
        self.fields['email'].max_length = None
        self.fields['email'].required=True

class UserAuthenticationForm(AuthenticationForm):

    class Meta :
        model = User
        fields = ('username','password')       
    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}) 
        self.fields['username'].help_text = None
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}) 
        self.fields['password'].help_text = None
        self.fields['password'].label = False







