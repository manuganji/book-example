from django.test import TestCase

from lists.models import Item, List
from lists.forms import ItemForm


class ItemFormTest(TestCase):

    def test_form_init_with_list(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        form = ItemForm(list2)
        self.assertIn(
            '<input id="id_list" name="list" type="hidden" value="{0}" />'.format(
                list2.id
            ),
            form.as_p()
        )

        self.assertEqual(form.fields['list'].initial, list2)


    def test_form_data_and_saving(self):
        list1 = List.objects.create()
        form = ItemForm(list1, data={'list': list1.id, 'text': 'wibble'})
        item =  form.save()
        self.assertEqual(item.list, list1)
        self.assertEqual(item.text, 'wibble')


    def test_ignores_list_id_hacked_in(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        form = ItemForm(list1, data={'list': list2.id, 'text': 'wibble'})
        item =  form.save()
        self.assertEqual(item.list, list1)
        self.assertEqual(item.text, 'wibble')


    def test_error_message_for_blank_items(self):
        list1 = List.objects.create()
        form = ItemForm(list1, data={'list': list1.id, 'text': ''})
        self.assertEqual(
            form.errors['text'],
            ["You can't have a blank item"]
        )


    def test_error_message_for_duplicate_items(self):
        list1 = List.objects.create()
        Item.objects.create(list=list1, text='textey')
        form = ItemForm(list1, data={'list': list1.id, 'text': 'textey'})
        self.assertEqual(
            form.errors['text'],
            ["You've already got this item in your list"]
        )
        self.assertNotIn('__all__', form.errors)

