from lists.models import Item
from django.forms.models import ModelForm
from django.forms.fields import HiddenInput

class ItemForm(ModelForm):

    def __init__(self, parent_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['list'].initial = parent_list
        self.fields['text'].error_messages['required'] = "You can't have a blank item"
        self.data['list'] = parent_list.id

    def validate_unique(self):
        super().validate_unique()
        if '__all__' in self.errors:
            self._update_errors({'text': ["You've already got this item in your list"]})
            del self.errors['__all__']

    class Meta:
        model = Item
        fields =  ('list', 'text')
        widgets = {'list': HiddenInput}

