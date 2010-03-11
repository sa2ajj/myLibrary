from django.db import models

class Book(models.Model):
    ''' ... '''

    title = models.TextField(null=False)

    language = models.CharField(max_length=64, null=False)

    # MSS: probably, this needs to be replaced with FileField or something
    file = models.TextField(null=False)

    class Meta:
        ordering = [ 'title' ]

class Author(models.Model):
    ''' ... '''

    name = models.CharField(max_length=256, null=False, unique=True)

    class Meta:
        ordering = [ 'name' ]

class BookAuthor(models.Model):
    book = models.ForeignKey(Book)
    author = models.ForeignKey(Author)

    class Meta:
        unique_together = (
            ('book', 'author'),
        )

class Series(models.Model):
    name = models.CharField(max_length=256, null=False)

    class Meta:
        db_table = 'catalogue_series'
        ordering = [ 'name' ]

class BookSeries(models.Model):
    book = models.ForeignKey(Book)
    series = models.ForeignKey(Series)
    number = models.IntegerField()

    class Meta:
        unique_together = (
            ('book', 'series', 'number'),
        )

class Tag(models.Model):
    name = models.CharField(max_length=128, null=False, unique=True)
    parent = models.ForeignKey('self', null=True)

    class Meta:
        ordering = [ 'name' ]

class BookTag(models.Model):
    book = models.ForeignKey(Book)
    tag = models.ForeignKey(Tag)

    class Meta:
        unique_together = (
            ('book', 'tag'),
        )

# vim:ts=4:sw=4:et
