from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'website', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name*', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your E-mail*', 'class': 'form-control'}),
            'website': forms.URLInput(attrs={'placeholder': 'Website*', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Write Your Comment*', 'class': 'form-control', 'rows': 4}),
        }