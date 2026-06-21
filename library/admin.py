from django.contrib import admin
from .models import Book, Member, BorrowRecord

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'total_copies', 'available_copies', 'added_on']
    search_fields = ['title', 'author', 'isbn']
    list_filter = ['category']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'joined_on']
    search_fields = ['name', 'email']

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['member', 'book', 'borrow_date', 'return_date']
    list_filter = ['borrow_date', 'return_date']
    search_fields = ['member__name', 'book__title']