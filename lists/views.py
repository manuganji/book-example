from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from lists.models import Item, List
from lists.forms import ItemForm

def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            Item.objects.create(text=request.POST['text'], list=list)
            return redirect('/lists/%d/' % (list.id,))
        except ValidationError as e:
            if 'blank' in str(e):
                error = "You can't have an empty list item"
            elif 'already exists' in str(e):
                error = "You've already got this in your list"

    return render(request, 'list.html', {'list': list, "error": error})

from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

class ListViewAndAddItemView(DetailView, CreateView):
    model = List
    context_object_name = 'list'
    pk_url_kwarg = 'list_id'
    template_name = 'list.html'
    form_class = ItemForm

    def get_success_url(self):
        return reverse('view_list', args=(self.get_object().id,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'parent_list': self.get_object()})
        return kwargs


def new_list(request):
    list = List.objects.create()
    try:
        Item.objects.create(text=request.POST['item_text'], list=list)
    except ValidationError:
        error_text = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error_text})

    return redirect('/lists/%d/' % (list.id,))

