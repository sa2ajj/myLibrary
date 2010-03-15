from django.db import models

class Book(models.Model):
    ''' ... '''

    uid = models.CharField(max_length=1024, null=False)
    uid_scheme = models.CharField(max_length=64, null=False)

    title = models.TextField(null=False)

    language = models.CharField(max_length=64, null=False)

    # MSS: probably, this needs to be replaced with FileField or something
    file = models.TextField(null=False)
    file_stamp = models.DateTimeField()

    annotation = models.TextField(null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = [ 'title' ]
        unique_together = (
            ('uid', 'uid_scheme'),
        )

class Author(models.Model):
    ''' ... '''

    name = models.CharField(max_length=256, null=False, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [ 'name' ]

class BookAuthor(models.Model):
    book = models.ForeignKey(Book)
    author = models.ForeignKey(Author)
    position = models.PositiveIntegerField(null=False)

    class Meta:
        unique_together = (
            ('book', 'author'),
        )

class Series(models.Model):
    name = models.CharField(max_length=256, null=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Series'
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

    def __unicode__(self):
        return self.name

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
