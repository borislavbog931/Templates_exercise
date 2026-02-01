from django import forms
from reviews.models import Review


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'book' in self.initial:
            self.fields['book'].widget = forms.HiddenInput()
            self.fields['book'].required = True # Ensure book is still required even if hidden

    class Meta:
        model = Review
        fields = ['author', 'body', 'rating', 'book', 'is_spoiler']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4}),
        }


class ReviewEditForm(ReviewForm):
    pass


class ReviewDeleteForm(ReviewForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].disabled = True
