from django.db import models

class BookFormat(models.Model):
    """
    Book format
    """
    name = models.CharField(max_length=128, null=False, unique=True)

    def __unicode__(self):
        return self.name

class Author(models.Model):
    """
    Author record
    """

    name = models.CharField(max_length=256, null=False, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Tag(models.Model):
    """
    Tag record
    """

    name = models.CharField(max_length=128, null=False)
    parent = models.ForeignKey('self', null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = (
            ('name', 'parent'),
        )

class Series(models.Model):
    """
    Series information
    """
    name = models.CharField(max_length=256, null=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Series'
        db_table = 'catalogue_series'
        ordering = ['name']

class Book(models.Model):
    """
    Book record
    """

    uid = models.CharField(max_length=1024, null=False)
    uid_scheme = models.CharField(max_length=64, null=False)

    title = models.TextField(null=False)
    authors = models.ManyToManyField(Author, through='BookAuthor')
    series = models.ManyToManyField(Series, through='BookSeries')
    tags = models.ManyToManyField(Tag, through='BookTag')

    language = models.CharField(max_length=64, null=False)

    # MSS: probably, this needs to be replaced with FileField or something
    file = models.TextField(null=False)
    file_stamp = models.DateTimeField()

    mimetype = models.CharField(max_length=128, null=False)

    format = models.ForeignKey(BookFormat, null=False)

    annotation = models.TextField(null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        unique_together = (
            ('uid', 'uid_scheme'),
        )

class BookAuthor(models.Model):
    """
    Link between books and authors
    """

    book = models.ForeignKey(Book)
    author = models.ForeignKey(Author)
    position = models.PositiveIntegerField(null=False)

    class Meta:
        unique_together = (
            ('book', 'author'),
        )
        ordering = ['position']

class BookSeries(models.Model):
    """
    Link between books and series
    """

    book = models.ForeignKey(Book)
    series = models.ForeignKey(Series)
    number = models.IntegerField()

    class Meta:
        unique_together = (
            ('book', 'series', 'number'),
        )

class BookTag(models.Model):
    """
    Link between book and tags
    """

    book = models.ForeignKey(Book)
    tag = models.ForeignKey(Tag)

    class Meta:
        unique_together = (
            ('book', 'tag'),
        )

# vim:ts=4:sw=4:et
