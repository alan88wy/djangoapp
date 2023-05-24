from django.forms import ModelForm
from .models import Room


class RoomForm(ModelForm):
    
    '''
    Can also define each form's field separately instead of using Meta class.
    Can also add label tag to each field :
    
    name = forms.CharField(label='Name', max_length=200)
    ....
    
    '''
    class Meta:
        model = Room
        fields = '__all__'  # includes all fields from Room
        
'''
    Can also create label with a dictionary for the fields when using __all__
    
    For example:
    
    labels = {
        "name" : "Your Name",
    }
    
    You can then use the label in your html
'''
