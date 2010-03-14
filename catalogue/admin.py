from django.contrib import admin

from myLibrary.catalogue.models import Book, Author, Series, Tag

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Series)
admin.site.register(Tag)
