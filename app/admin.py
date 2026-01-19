from django.contrib import admin
from app.models import Book, ProductURL, Genre


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_filter = ("genre",)
    search_fields = ("isbn", "name", "author")


admin.site.register(ProductURL)
admin.site.register(Genre)
