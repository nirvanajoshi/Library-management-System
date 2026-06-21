from django import forms
from .models import BorrowRecord, Book, Member

class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['book', 'member']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'member': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show books that have available copies
        self.fields['book'].queryset = Book.objects.filter(available_copies__gt=0)