from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from lists.forms import ExistingListItemForm, ItemForm
from lists.models import Item, List

def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list = List.objects.get(id=list_id)

    if request.method == 'POST':
        form = ExistingListItemForm(data={
            'text': request.POST['text'],
            'list': list.id
        })
        if form.is_valid():
            form.save()
            return redirect('/lists/%d/' % (list.id,))
    else:
        form = ExistingListItemForm()

    return render(request, 'list.html', {'list': list, "form": form})


def new_list(request):
    form = ItemForm(request.POST)
    if form.is_valid():
        list = List.objects.create()
        Item.objects.create(text=form.cleaned_data['text'], list=list)
        return redirect('/lists/%d/' % (list.id,))
    return render(request, 'home.html', {'form': form})

