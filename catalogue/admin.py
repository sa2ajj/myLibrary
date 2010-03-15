from django.contrib import admin

from myLibrary.catalogue.models import Book, Author, Series, Tag
from myLibrary.catalogue.models import BookAuthor, BookSeries, BookTag

class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1

class BookAdmin(admin.ModelAdmin):
    inlines = (BookAuthorInline,)

    fieldsets = (
        ('UID', {
            'fields': ('uid_scheme', 'uid'),
        }),
        ('Book Info', {
            'fields': ('title', 'language', 'annotation'),
        }),
        ('File', {
            'fields': ('mimetype', 'file', 'file_stamp')
        })
    )

class AuthorAdmin(admin.ModelAdmin):
    inlines = (BookAuthorInline,)

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Series)
admin.site.register(Tag)
