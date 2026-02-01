from datetime import date

from django import forms

from books.models import Book, Tag

# class BookFormBasic(forms.Form): #standard form that doesnt use the model
#     title = forms.CharField(max_length=100,
#                             widget=forms.TextInput(attrs={'placeholder': 'e.g. Done'}))
#     price = forms.DecimalField(max_digits=6, decimal_places=2, min_value=0, label = "Price (USD)")
#     isbn = forms.CharField(max_length=12, min_length=10)
#     genre = forms.ChoiceField(choices=Book.GenreChoices.choices,
#                               widget=forms.RadioSelect)
#     publishing_date = forms.DateField(
#         initial=date.today,
#     )
#     description = forms.CharField(
#         widget=forms.Textarea,
#     )
#     image_url = forms.URLField()
#     publisher = forms.CharField(max_length=100)

from datetime import date

from django import forms

from books.models import Book


# class BookFormBasic(forms.Form): #standard form that doesnt use the model
#     title = forms.CharField(max_length=100,
#                             widget=forms.TextInput(attrs={'placeholder': 'e.g. Done'}))
#     price = forms.DecimalField(max_digits=6, decimal_places=2, min_value=0, label = "Price (USD)")
#     isbn = forms.CharField(max_length=12, min_length=10)
#     genre = forms.ChoiceField(choices=Book.GenreChoices.choices,
#                               widget=forms.RadioSelect)
#     publishing_date = forms.DateField(
#         initial=date.today,
#     )
#     description = forms.CharField(
#         widget=forms.Textarea,
#     )
#     image_url = forms.URLField()
#     publisher = forms.CharField(max_length=100)

class BookFormBasic(forms.ModelForm):
    tags =forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    fields_order =[]
    class Meta:
        exclude = ['slug']
        model = Book

    def save(self, commit=True):
        book = super().save(commit=commit)
        book.tags.clear()
        selected_tags = self.cleaned_data.get('tags')
        if selected_tags:
            book.tags.add(*selected_tags)
        return book

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all()


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs['class'] = 'form-control'


class BookCreateForm(BookFormBasic):
    class Meta:
        exclude = ['slug']
        model = Book


class BookEditForm(BookFormBasic):
    class Meta:
        exclude = ['slug']
        model = Book


class BookDeleteForm(BookFormBasic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].disabled = True


class BookSearchForm(forms.Form):
    query = forms.CharField(max_length=100,label = "", required=False,)

