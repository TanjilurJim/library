from django.shortcuts import render
from django.http import HttpResponse
from .models import Book,Author,BookInstance,Genre,Language
from django.views.generic import  *

# Create your views here.
def index(request):

    num_books= Book.objects.all().count() 
    num_instances = BookInstance.objects.all().count() 

    num_instances_avail = BookInstance.objects.filter(status__exact='a').count()

    context = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_avail':num_instances_avail
    }

    return render(request,'catalog/index.html',context=context)


class BookCreate(CreateView): #book_form.html
    model = Book 
    fields = '__all__'

class BookDetail(DetailView):

    model = Book

class BookListView(ListView):
    model = Book
    queryset = Book.objects.all()
    context_object_name = 'book_list'
    
