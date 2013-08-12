from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from lists.models import Item, List
from lists.forms import ItemForm

def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list = List.objects.get(id=list_id)
    form = ItemForm(parent_list=list)
    if request.method == 'POST':
        form = ItemForm(parent_list=list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/lists/%d/' % (list.id,))

    return render(request, 'list.html', {'list': list, "form": form})


from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

class ListViewAndAddItemView(DetailView, CreateView):
    model = List
    context_object_name = 'list'
    template_name = 'list.html'
    form_class = ItemForm

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

