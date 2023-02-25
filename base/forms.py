
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Room , User

# from django.contrib.auth.models import User
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model= User
        fields = ['name','username','email','password1']
        # exclude = ['Password']




class RoomForm(ModelForm):
    class Meta:
        model= Room
        fields = '__all__'
        exclude = ['host','participants']  # exclude is to get rid of unwanted column by specifying name of column




class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','password']


class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username','email','bio']