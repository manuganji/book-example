from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import Client, TestCase

from lists.models import List, Item
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content, expected_html)



class NewListItemPOSTTest(TestCase):

    def test_url(self):
        # TODO
        pass

    def test_can_use_POST_to_create_new_list_item(self):
        client = Client()
        response = client.post('/lists/new', {u'item_text': u'A new list item'})
        self.assertRedirects(response, '/')
        new_list = List.objects.all()[0]
        first_list_item = new_list.item_set.all()[0]
        self.assertEqual(first_list_item.text, 'A new list item')


class ListsAndItemsTest(TestCase):

    def test_creating__saving_and_retrieving_a_list_with_items(self):

        new_list = List()
        new_list.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = new_list
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = new_list
        second_item.save()


