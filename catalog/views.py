from django.shortcuts import render
from django.http import HttpResponse
from .models import Book,Author,BookInstance,Genre,Language
from django.views.generic import  *
from django.contrib.auth.decorators import login_required,user_passes_test
 # function based er jonno decorator
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin #for class based views
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta



def is_librarian_or_admin(user):
    return user.is_superuser or user.groups.filter(name='Librarian').exists()

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


class BookCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):  # book_form.html
    model = Book 
    fields = '__all__'

    # Implementing the test_func method to restrict access
    def test_func(self):
        # Allow access only to superusers or users in the 'Librarian' group
        return self.request.user.is_superuser or self.request.user.groups.filter(name='Librarian').exists()


class BookDetail(DetailView):

    model = Book

class BookListView(ListView):
    model = Book
    queryset = Book.objects.all()
    context_object_name = 'book_list'
    paginate_by = 5  # Show 5 books per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # For each book, annotate with the first available instance ID (or None)
        for book in context['book_list']:
            first_available_instance = book.bookinstance_set.filter(status='a').first()
            if first_available_instance:
                book.first_available_instance_id = first_available_instance.id
            else:
                book.first_available_instance_id = None

        return context



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
        return BookInstance.objects.filter(borrower=self.request.user).order_by('due_back')
    
    
    



@login_required
def borrow_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk, status='a')  # 'a' for available
    if request.method == 'POST':
        book_instance.status = 'o'  # 'o' for on loan
        book_instance.due_back = timezone.now() + timedelta(days=7)
        book_instance.borrower = request.user
        book_instance.save()
        return redirect('catalog:book_detail', pk=book_instance.book.pk)
    else:
        # This GET method will just redirect to book detail or could show a confirmation page
        return redirect('catalog:book_detail', pk=book_instance.book.pk)



@login_required
def renew_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk, borrower=request.user, status='o')  # Ensure only borrowed books by this user
    if request.method == 'POST':
        book_instance.due_back = timezone.now() + timedelta(days=7)  # Extend due date by 7 days
        book_instance.save()
        return redirect('catalog:my_view')  # Redirect back to the list of borrowed books
    else:
        return redirect('catalog:my_view')  # Redirect if not a POST request
