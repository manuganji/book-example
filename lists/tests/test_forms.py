from django.test import TestCase

from lists.models import List, Item
from lists.forms import ItemForm, ExistingListItemForm


class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())


    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            ["You can't have an empty list item"]
        )


    def test_saving_a_new_list(self):
        form = ItemForm(data={'text': 'new item'})
        item = form.save()
        self.assertEqual(List.objects.all().count(), 1)
        self.assertEqual(Item.objects.all().count(), 1)
        self.assertEqual(item.text, 'new item')
        self.assertEqual(item.list, List.objects.all()[0])



class ExistingListItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        listey = List.objects.create()
        form = ExistingListItemForm(parent_list=listey)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())


    def test_form_renders_list_input_as_hidden(self):
        listey = List.objects.create()
        form = ExistingListItemForm(parent_list=listey)
        self.assertIn('name="list" type="hidden"', form.as_p())


    def test_form_validation_for_blank_items(self):
        listey = List.objects.create()
        form = ExistingListItemForm(parent_list=listey, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            ["You can't have an empty list item"]
        )


    def test_form_validation_for_duplicate_items(self):
        listey = List.objects.create()
        Item.objects.create(list=listey, text='hi')
        form = ExistingListItemForm(parent_list=listey, data={'text': 'hi'})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            ["You've already got this in your list"]
        )


    def test_saving_a_new_item(self):
        listey = List.objects.create()
        form = ExistingListItemForm(parent_list=listey, data={'text': 'new item'})
        item = form.save()
        self.assertEqual(List.objects.all().count(), 1)
        self.assertEqual(item.text, 'new item')
        self.assertEqual(item.list, List.objects.all()[0])

