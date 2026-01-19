import json

from django.core.management.base import BaseCommand
from app.models import Book, Genre, ProductURL


class Command(BaseCommand):
    help = "Books import"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, help="Data source path")

    def handle(self, *args, **options):
        path = options["path"]

        if not path:
            self.stderr.write("Add data source JSON path: --path=...")
            return

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            try:
                book, created = Book.objects.get_or_create(
                    name=item["product_name"],
                    defaults={
                        "isbn": item.get("ISBN"),
                        "author": item.get("author"),
                        "price": item.get("price"),
                        "release_year": item.get("release_year"),
                    },
                )
            except:  # Fuck you Tim Pidorasivich Liznev!
                self.stdout.write(
                    self.style.NOTICE(f"Import failed for {item['product_name']}")
                )

            genres = [g.strip() for g in item.get("genre", "").split(",")]
            for genre_name in genres:
                genre, _ = Genre.objects.get_or_create(name=genre_name)
                book.genre.add(genre)

            product_url, _ = ProductURL.objects.get_or_create(url=item["product_url"])
            book.product_urls.add(product_url)

            book.save()

            status = "created" if created else "ignored"
            self.stdout.write(f"Book '{book.name}' {status}")

        self.stdout.write(self.style.SUCCESS("Import finished succesfully"))
