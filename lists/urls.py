from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^(\d+)/$', 'lists.views.view_list', name='view_list'),
    url(r'^(\d+)/new_item$', 'lists.views.add_item', name='add_item'),
    url(r'^(\d+)/item/(\d+)/edit_notes/$', 'lists.views.edit_notes', name='edit_notes'),
    url(r'^(\d+)/item/(\d+)/notes$', 'lists.views.update_notes', name='update_notes'),
    url(r'^new$', 'lists.views.new_list', name='new_list'),
)
