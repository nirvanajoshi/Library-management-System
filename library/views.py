from django.shortcuts import render ,get_object_or_404,
from .models import Book, Member, BorrowRecord

def dashboard(request):
    total_books = Book.objects.count()
    total_members = Member.objects.count()
    total_borrowed = BorrowRecord.objects.filter(return_date__isnull=True).count()
    return render(request, 'library/dashboard.html', {
        'total_books': total_books,
        'total_members': total_members,
        'total_borrowed': total_borrowed
    })
    
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def borrow_list(request):
    borrows = BorrowRecord.objects.filter(return_date__isnull=True)
    return render(request, 'library/borrow_list.html', {'borrows': borrows})
