from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.shortcuts import HttpResponse
from django.template import loader
from app.models import Book
from django.db.models import Q


class BooksListView(ListView):
    model = Book
    paginate_by = 10
    template_name = "books_list.html"
    context_object_name = "books_list"

    def get_queryset(self):
        search = self.request.GET.get("search")
        if search is not None:
            return Book.objects.filter(
                Q(name__icontains=search)
                | Q(author__icontains=search)
                | Q(isbn__icontains=search)
            ).order_by("id")
        return Book.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["search"] = self.request.GET.get("search", "")
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = "book_details.html"
