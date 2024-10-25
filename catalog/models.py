from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User

# Create your models here.
class Genre(models.Model):

    name = models.CharField(max_length=150)

    def get_absolute_url(self):
        return reverse("genre_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name 


class Language(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name 




class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=600, null=True)
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    genre = models.ManyToManyField(Genre)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        genres = ", ".join([genre.name for genre in self.genre.all()])
        return f"{self.title} written by {self.author}. It is a/an {genres} type of book"

    def get_absolute_url(self):
        return reverse("catalog:book_detail", kwargs={"pk": self.pk})

    def available_instances(self):
        """Return the number of available copies of this book."""
        return self.bookinstance_set.filter(status='a').count()

    


class Author(models.Model):
    first_name = models.CharField(max_length=200, db_index=True)
    last_name = models.CharField(max_length=200, db_index=True)
    date_of_birth = models.DateField(null=True,blank=True)

    class Meta:
        ordering = ['last_name','first_name']

    def get_absolute_url(self):
        return reverse("catalog:author_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.last_name} , {self.first_name}"
        
import uuid 

class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    book = models.ForeignKey('Book',on_delete=models.RESTRICT,null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True,blank=True)
    borrower = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    LOAN_STATUS = (
        ('m','Maintenance'),
        ('o','On Loan'),
        ('a','Available'),
        ('r','Reserved')
    )

    status = models.CharField(max_length=1,choices=LOAN_STATUS,blank=True,default='m') 

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} Title: ({self.book.title})'