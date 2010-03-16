from django.contrib import admin

from myLibrary.catalogue.models import BookFormat, Book, Author, Series, Tag
from myLibrary.catalogue.models import BookAuthor, BookSeries, BookTag

class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1

class BookSeriesInline(admin.TabularInline):
    model = BookSeries
    extra = 1

class BookTagInline(admin.TabularInline):
    model = BookTag
    extra = 1

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

    inlines = (BookAuthorInline, BookSeriesInline, BookTagInline)

    fieldsets = (
        ('UID', {
            'fields': ('uid_scheme', 'uid'),
        }),
        ('Book Info', {
            'fields': ('title', 'language', 'annotation'),
        }),
        ('File', {
            'fields': ('file', 'file_stamp', 'mimetype', 'format')
        })
    )

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    inlines = (BookAuthorInline,)

class SeriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    inlines = (BookSeriesInline,)

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(BookFormat)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Tag, TagAdmin)
