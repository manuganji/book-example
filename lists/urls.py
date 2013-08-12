from django.conf.urls import patterns, url
from lists import views as list_views

urlpatterns = patterns('',
    url(r'^(.+)/$', 'lists.views.view_list', name='view_list'),
    #url(r'^(?P<list_id>.+)/$', list_views.ListViewAndAddItemView.as_view(), name='view_list'),
    url(r'^new$', 'lists.views.new_list', name='new_list'),
)
