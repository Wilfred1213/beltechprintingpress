from django import forms
from .models import BlogComment, Testimonial, Contact, NewsLetter

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


class TestimonialForm(forms.ModelForm):
    # Overwrite the rating field to use RadioSelect, which works well with the custom star CSS
    rating = forms.IntegerField(
        label='Rate Your Experience (1 to 5 Stars)',
        widget=forms.RadioSelect(choices=[
            (1, '⭐'), 
            (2, '⭐⭐'), 
            (3, '⭐⭐⭐'), 
            (4, '⭐⭐⭐⭐'), 
            (5, '⭐⭐⭐⭐⭐')
        ]),
        initial=5,
    )

    class Meta:
        model = Testimonial
        fields = ['name', 'rating', 'message', 'main_image']
        
        # Add Bootstrap's default 'form-control' class to other fields
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Your Full Name'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Share your detailed experience here...'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}), # File inputs need form-control
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        # These MUST match the names in models.py exactly
        fields = ['full_name', 'email', 'phone_number', 'message']
        
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Your Name*', 
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your E-mail*', 
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Phone Number*', 
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Write Your Message*', 
                'class': 'form-control', 
                'rows': 4
            }),
        }

class NewsLetterForm(forms.ModelForm):

    class Meta:
        model = NewsLetter
        fields = ['email']
        widgets = {'email': forms.EmailInput(attrs={
                'placeholder': 'enter your E-mail*', 
                'class': 'form-control'
            }),}
        

class SendNewsletterForm(forms.Form):
    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your newsletter content here...'}))