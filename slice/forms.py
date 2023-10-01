from django import forms

class Cuisine(forms.Form):
    CUISINE_CHOICES = [
        ('seafood', 'Seafood'),
        ('mexican', 'Mexican'),
        ('chinese', 'Chinese'),
        ('italian', 'Italian'),
        ('indian', 'Indian'),
        ('japanese', 'Japanese'),
        ('french', 'French'),
        ('thai', 'Thai'),
        ('mediterranean', 'Mediterranean'),
        ('american', 'American'),
    ]
    
    choices = forms.MultipleChoiceField(choices=CUISINE_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-list'}),
)