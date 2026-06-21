from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Book, Member, BorrowRecord
from .forms import BorrowForm

@login_required
def dashboard(request):
    total_books = Book.objects.count()
    total_members = Member.objects.count()
    total_borrowed = BorrowRecord.objects.filter(return_date__isnull=True).count()
    return render(request, 'library/dashboard.html', {
        'total_books': total_books,
        'total_members': total_members,
        'total_borrowed': total_borrowed
    })

@login_required
def book_list(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(title__icontains=query) if query else Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books, 'query': query})

@login_required
def member_list(request):
    members = Member.objects.all()
    return render(request, 'library/member_list.html', {'members': members})

@login_required
def borrow_list(request):
    records = BorrowRecord.objects.filter(return_date__isnull=True).select_related('book', 'member')
    return render(request, 'library/borrow_list.html', {'records': records})

@login_required
def borrow_book(request):
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow = form.save(commit=False)
            book = borrow.book
            if book.available_copies > 0:
                book.available_copies -= 1
                book.save()
                borrow.save()
                messages.success(request, f'"{book.title}" borrowed successfully!')
                return redirect('borrow_list')
            else:
                messages.error(request, 'No copies available for this book.')
    else:
        form = BorrowForm()
    return render(request, 'library/borrow_book.html', {'form': form})

@login_required
def return_book(request, record_id):
    record = get_object_or_404(BorrowRecord, id=record_id)
    if request.method == 'POST':
        record.return_date = timezone.now()
        record.save()
        record.book.available_copies += 1
        record.book.save()
        messages.success(request, f'"{record.book.title}" returned successfully!')
        return redirect('borrow_list')
    return render(request, 'library/return_book.html', {'record': record})

@login_required
def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['category']
        copies = int(request.POST['total_copies'])
        Book.objects.create(title=title, author=author, isbn=isbn,
                            category=category, total_copies=copies, available_copies=copies)
        messages.success(request, f'Book "{title}" added successfully!')
        return redirect('book_list')
    return render(request, 'library/add_book.html')

@login_required
def add_member(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        Member.objects.create(name=name, email=email, phone=phone)
        messages.success(request, f'Member "{name}" added successfully!')
        return redirect('member_list')
    return render(request, 'library/add_member.html')