from django.core.urlresolvers import resolve
from django.test import Client, TestCase
from django.utils.html import escape

from lists.forms import ItemForm, EMPTY_LIST_ERROR
from lists.models import Item, List
from lists.views import home_page


class HomePageTest(TestCase):
    maxDiff = None

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_renders_home_template_with_form(self):
        response = Client().get('/')
        self.assertTemplateUsed(response, 'home.html')
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        client = Client()
        response = client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )

        self.assertEqual(Item.objects.all().count(), 1)
        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new list item')
        self.assertEqual(List.objects.all().count(), 1)
        new_list = List.objects.all()[0]
        self.assertEqual(new_item.list, new_list)

        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))


    def test_validation_errors_sent_back_to_home_page_template(self):
        response = Client().post('/lists/new', data={'text': ''})
        self.assertEqual(Item.objects.all().count(), 0)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, escape(EMPTY_LIST_ERROR))
        self.assertIsInstance(response.context['form'], ItemForm)



class ListViewTest(TestCase):

    def test_list_view_displays_all_items(self):
        list = List.objects.create()
        Item.objects.create(text='itemey 1', list=list)
        Item.objects.create(text='itemey 2', list=list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        client = Client()
        response = client.get('/lists/%d/' % (list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(response.context['list'], list)


    def test_saving_a_POST_request_to_an_existing_list(self):
        list = List.objects.create()
        other_list = List.objects.create()
        client = Client()
        response = client.post(
            '/lists/%d/' % (list.id,),
            data={'text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.all().count(), 1)
        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, list)
        self.assertRedirects(response, '/lists/%d/' % (list.id,))


    def test_empty_item_validation_errors_end_up_on_lists_page(self):
        list = List.objects.create()

        response = Client().post(
            '/lists/%d/' % (list.id,),
            data={'text': ''}
        )
        self.assertEqual(Item.objects.all().count(), 0)
        self.assertTemplateUsed(response, 'list.html')
        expected_error =  escape("You can't have an empty list item")
        self.assertContains(response, expected_error)


    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        client = Client()
        response = client.post(
            '/lists/%d/' % (list1.id,),
            data={'text': 'textey'}
        )

        self.assertEqual(Item.objects.all().count(), 1)
        self.assertTemplateUsed(response, 'list.html')
        expected_error =  escape("You've already got this in your list")
        self.assertContains(response, expected_error)

