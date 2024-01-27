from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    book_objects = Book.objects.all()
    books = list({'name': b.name, 'author': b.author, 'pub_date': b.pub_date} for b in book_objects)

    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(books, 10)
    page = paginator.get_page(page_number)

    context = {
        'books': page.object_list,
        'page': page
    }
    return render(request, template, context)

def home(request):
    return redirect('books')


def date_of_publication(request, pub_date):
    template = 'books/books_list.html'
    # book_objects = Book.objects.filter(pub_date=pub_date)
    # books = list({'name': b.name, 'author': b.author, 'pub_date': b.pub_date} for b in book_objects)
    #
    # page_number = int(request.GET.get('page', 1))
    # paginator = Paginator(books, 1)
    # page = paginator.get_page(page_number)
    #
    # context = {
    #     'books': page.object_list,
    #     'page': page
    # }
    books = Book.objects.all().filter(pub_date=pub_date)
    all_books = Book.objects.all().order_by('pub_date')
    all_pub_dates = list(set([f'{x.pub_date}' for x in all_books]))
    if all_pub_dates.index(pub_date) != 0 and all_pub_dates.index(pub_date) != int(len(all_pub_dates) - 1):
        prev_page = str(all_pub_dates[int(all_pub_dates.index(pub_date) - 1)])
        next_page = str(all_pub_dates[int(all_pub_dates.index(pub_date) + 1)])
    elif all_pub_dates.index(pub_date) == 0:
        prev_page = str(all_pub_dates[int(len(all_pub_dates) - 1)])
        next_page = str(all_pub_dates[int(all_pub_dates.index(pub_date) + 1)])
    elif all_pub_dates.index(pub_date) == int(len(all_pub_dates) - 1):
        prev_page = str(all_pub_dates[int(all_pub_dates.index(pub_date) - 1)])
        next_page = str(all_pub_dates[0])
    paginator = Paginator(all_pub_dates, 1)
    page = paginator.page(int(all_pub_dates.index(pub_date) + 1))
    context = {'books': books,
               'page': page,
               'prev_page': prev_page,
               'next_page': next_page}

    return render(request, template, context)
