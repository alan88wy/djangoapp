from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    
    '''
    Can also do this:
    
    name = forms.CharField(label='Name', max_length=200)
    ....
    
    '''
    class Meta:
        model = Room
        fields = '__all__'  # includes all fields from Room
        
