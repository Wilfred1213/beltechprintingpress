from django import forms
from .models import BlogComment

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['name', 'email', 'website', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name*', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your E-mail*', 'class': 'form-control'}),
            'website': forms.URLInput(attrs={'placeholder': 'Website*', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Write Your Comment*', 'class': 'form-control', 'rows': 4}),
        }

class BlogSearchForm(forms.Form):
    q = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Keywords here....',
            'class': 'sidebar__search-input-2' # This matches your CSS
        })
    )