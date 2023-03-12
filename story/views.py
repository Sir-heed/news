from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from .tasks import get_latest_news

from .models import Item
from .forms import ItemForm, ItemFilterForm, SearchForm

# Create your views here.
top_stories_url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
news = 'https://hacker-news.firebaseio.com/v0/item/{}.json'


def index(request):
    if Item.objects.count() == 0:
        get_latest_news.delay()
    context = {}
    latest_news = Item.objects.order_by('-id')
    filter_form = ItemFilterForm(request.POST or None)
    search_form = SearchForm(request.POST or None)
    if filter_form.is_valid():
        item_type = filter_form.cleaned_data['item_type']
        latest_news = latest_news.filter(item_type=item_type)
    if search_form.is_valid():
        search = search_form.cleaned_data['search']
        latest_news = latest_news.filter(text__contains=search)
    template = loader.get_template('story/index.html')
    paginator = Paginator(latest_news, 5) # Show 25 news per page.
    page_number = request.GET.get('page')
    latest_news = paginator.get_page(page_number)
    context = {
        'latest_news': latest_news,
        'filter_form': filter_form,
        'search_form': search_form,
        # 'page_obj': page_obj
    }
    return HttpResponse(template.render(context, request))


def detail(request, pk):
    try:
        item = Item.objects.get(id=pk)
        parent = item.parent
        kids = item.kids
        kid_qs = None
        if parent:
            try:
                parent = Item.objects.get(item_id=parent)
            except Item.DoesNotExist:
                parent = None
        if kids:
            kid_qs = Item.objects.filter(item_id__in=kids)
        return render(request, 'story/detail.html', {'item': item, 'parent': parent, 'kid_qs': kid_qs})
    except Item.DoesNotExist:
        raise Http404('Item does not exist')


def create_item(request):
    context = {}
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("story:index")
    context['form']= form
    return render(request, "story/create_item.html", context)


def edit_item(request, pk):
    context = {}
    try:
        item = Item.objects.get(id=pk)
    except Item.DoesNotExist:
        raise Http404('Item does not exist')
    if item.editable == False:
        raise Http404('Item cannot be edit')
    form = ItemForm(request.POST or None, instance = item)
    if form.is_valid():
        form.save()
        return redirect("story:index")
    context["form"] = form
    return render(request, "story/edit_item.html", context)


def delete_item(request, pk):
    try:
        item = Item.objects.get(id=pk)
    except Item.DoesNotExist:
        raise Http404('Item does not exist')
    if item.editable == False:
        raise Http404('Item cannot be delete')
    item.delete()
    return redirect("story:index")