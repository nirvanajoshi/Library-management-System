from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('books/', views.book_list, name='book_list'),
    path('members/', views.member_list, name='member_list'),
    path('borrows/', views.borrow_list, name='borrow_list'),
]