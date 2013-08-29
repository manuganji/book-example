from django import forms

from lists.models import Item

class ItemForm(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        empty_error = "You can't have an empty list item"
        self.fields['text'].error_messages['required'] = empty_error


    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(
                attrs={'placeholder': 'Enter a to-do item'}
            ),
        }
