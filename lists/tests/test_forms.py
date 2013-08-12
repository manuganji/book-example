from django.test import TestCase

from lists.forms import ItemForm

from lists.models import Item, List

class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_renders_list_as_hidden_input(self):
        form = ItemForm()
        self.assertIn('name="list" type="hidden"', form.as_p())

    def test_setting_initial_list(self):
        listey = List.objects.create()
        form = ItemForm()
        form.fields['list'].initial = listey
        self.fail(form.as_p())


    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            ["You can't have an empty list item"]
        )


    def test_form_validation_for_duplicate_items(self):
        listey = List.objects.create()
        form1 = ItemForm(data={'text': 'hiya', 'list': listey.id})
        item = form1.save()
        self.assertEqual(item.list, listey)
        self.assertEqual(item.text, 'hiya')

        form2 = ItemForm(data={'text': 'hiya', 'list': listey.id})
        self.assertFalse(form2.is_valid())
        self.fail(form2.errors)
        self.assertEqual(
            form2.errors['__all__'],
            ["You can't have an empty list item"]
        )

