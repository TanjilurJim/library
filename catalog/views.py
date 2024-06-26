from django.shortcuts import render
from django.http import HttpResponse
from .models import Book,Author,BookInstance,Genre,Language
from django.views.generic import  *
from django.contrib.auth.decorators import login_required # function based er jonno decorator
from django.contrib.auth.mixins import LoginRequiredMixin #for class based views
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


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


class BookCreate(LoginRequiredMixin, CreateView): #book_form.html
    model = Book 
    fields = '__all__'

class BookDetail(DetailView):

    model = Book

class BookListView(ListView):
    model = Book
    queryset = Book.objects.all()
    context_object_name = 'book_list'

@login_required
def my_view(request):
    return render(request,'catalog/my_view.html')
    

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'catalog/signup.html'

class CheckedOutBooksByUserView(LoginRequiredMixin,ListView):


    #list all BookInstances BUT I will filter based off currently logged in user session

    model = BookInstance
    template_name = 'catalog/my_view.html'
    paginate_by = 5 #5 book instances per page


    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).all()
    
    
    

