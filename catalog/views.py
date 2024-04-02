from django.shortcuts import render
from django.http import HttpResponse
from .models import Book,Author,BookInstance,Genre,Language
from django.views.generic import  *
from django.contrib.auth.decorators import login_required # function based er jonno decorator
from django.contrib.auth.mixins import LoginRequiredMixin #for class based views
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

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


class BookCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    fields = '__all__'
    template_name = 'catalog/create_book.html'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        # Raise a PermissionDenied exception if the user does not pass the test
        raise PermissionDenied
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
    
    
    

@login_required
def renew_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if book_instance.borrower == request.user:
        # Set the due back to 1 weeks from today
        book_instance.due_back = timezone.now() + timedelta(weeks=1)
        book_instance.save()
        # Redirect to 'my_view' to see the updated book list
        return redirect('catalog:my_view')
    else:
        return HttpResponseForbidden("You can't renew this book.")
    

def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # First, try to fetch a book instance
    book_instance = book.bookinstance_set.filter(status='a').first()
    if book_instance:
        book_instance.borrower = request.user
        book_instance.status = 'o'  # Update status to 'On Loan'
        book_instance.due_back = timezone.now() + timedelta(weeks=2)  # Set a due back date
        book_instance.save()
        return redirect('catalog:my_view')
    else:
        return HttpResponse("No available instances for this book.")

