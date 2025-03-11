from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from .models import Profile, Expense ,Book , Author

# Create your views here.
def demo_one_to_one(request):
    profiles = Profile.objects.select_related('user').all();
    # profiles = Profile.objects.select_related('user').all().filter(location="New York").all();

    #  list comprehension

    profile_data = [
        {
            # "id":profile.user.id,
            "id":profile.user.id,
            "username":profile.user.username,
            "email":profile.user.email,
            "bio":profile.bio,
            "birth_date":profile.birth_date,
            "location":profile.location
        } for profile in profiles
    ]

    return JsonResponse(profile_data,safe=False)


# user/id/ deye call kore url hit

def user(request,pk):
    profile = Profile.objects.select_related("user").get(user_id=pk)

        #  list comprehension

    profile_data = [
        {
            # "id":profile.user.id,
            "id":profile.user.id,
            "username":profile.user.username,
            "email":profile.user.email,
            "bio":profile.bio,
            "birth_date":profile.birth_date,
            "location":profile.location
        } 
    ]

    return JsonResponse(profile_data,safe=False)

def demo_one_to_many(request):
    # expenses = Expense.objects.select_related("category").filter(category="1").all()
    expenses = (
        Expense.objects.select_related("category").filter(category__name="Food").all()
    )
    expense_data = [
        {
            "amount": str(e.amount),
            "category": e.category.name,
            "description": e.description,
        }
        for e in expenses
    ]

    return JsonResponse(expense_data, safe=False)

def demo_many_to_many(request):
    books = Book.objects.prefetch_related("authors").all()
    book_data = [
        {
            "book_id": b.id,
            "title": b.title,
            "authors": [a.name for a in b.authors.all()],
            "isbn": b.isbn,
        }
        for b in books
    ]

    return JsonResponse(book_data, safe=False)
def get_book_details(request, book_title):
    try:
        # Get books whose titles contain the search term (case-insensitive)
        books = Book.objects.prefetch_related('authors').filter(title__contains=book_title)
        
        if not books.exists():
            return JsonResponse({'error': 'No books found'}, status=404)
        
        # Prepare details for all matching books
        books_details = {
            'books': [{
                'title': book.title,
                'year': book.year,
                'isbn': book.isbn,
                'authors': [{
                    'name': author.name,
                    'bio': author.bio
                } for author in book.authors.all()]
            } for book in books]
        }
        
        return JsonResponse(books_details)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def get_author_details(request, author_name):
    try:
        # Get authors whose names contain the search term (case-insensitive)
        authors = Author.objects.prefetch_related('book_set').filter(name__icontains=author_name)
        
        if not authors.exists():
            return JsonResponse({'error': 'No authors found'}, status=404)
        
        # Prepare details for all matching authors
        authors_details = {
            'authors': [{
                'name': author.name,
                'bio': author.bio,
                'books': [{
                    'title': book.title,
                    'year': book.year,
                    'isbn': book.isbn
                } for book in author.book_set.all()]
            } for author in authors]
        }
        
        return JsonResponse(authors_details)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
def get_book_by_id(request, book_id):
    try:
        # Get book with related authors
        book = Book.objects.prefetch_related('authors').get(id=book_id)
        
        # Prepare book details
        book_details = {
            'id': book.id,
            'title': book.title,
            'year': book.year,
            'isbn': book.isbn,
            'authors': [{
                'name': author.name,
                'bio': author.bio
            } for author in book.authors.all()]
        }
        
        return JsonResponse(book_details)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
