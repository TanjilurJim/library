# URLS Catalog 
from django.urls import path 
from . import views 
from .views import *

app_name='catalog'

urlpatterns = [
    path('',views.index,name='index'),
    path('create_book/',views.BookCreate.as_view(),name='create_book'),
    path('book/<int:pk>/',views.BookDetail.as_view(),name='book_detail'),
    path('book_list/',BookListView.as_view(),name='book_list'),
    # path('my_view/',views.my_view,name='my_view'),
    path('my_view/',views.CheckedOutBooksByUserView.as_view(),name='my_view'),
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('renew/<uuid:pk>/', views.renew_book, name='renew_book'),
    path('borrow/<int:pk>/', views.borrow_book, name='borrow_book'),


]
