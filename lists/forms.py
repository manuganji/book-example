from django import forms

from lists.models import List, Item

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
            'list': forms.fields.HiddenInput()
        }


    def save(self, *args, **kwargs):
        item = super().save(commit=False)
        item.list = List.objects.create()
        item.save()
        return item



class ExistingListItemForm(ItemForm):

    def __init__(self, parent_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data['list'] = parent_list.id


    def validate_unique(self):
        super().validate_unique()
        if '__all__' in self.errors:
            self._update_errors({'text':["You've already got this in your list"]})


    class Meta(ItemForm.Meta):
        fields = ('list', 'text')

    def save(self, *args, **kwargs):
        return super(forms.models.ModelForm, self).save(*args, **kwargs)

