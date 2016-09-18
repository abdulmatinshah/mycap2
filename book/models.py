from django.db import models

from wagtail.wagtailcore.models import Page

from mycap.util_streamfield import *
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


class BookIndex(Page):
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro = models.CharField(max_length=250, null=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        ImageChooserPanel('banner_image'),
    ]

    subpage_types = ['book.BookPage', ]

    @property
    def books(self):
        books = BookPage.objects.live().descendant_of(self)

        return books


CHOICES = (
    ('book/book_page.html', 'Book Page Template'),
    ('book/one.html', 'Design One'),
    ('book/two.html', 'Design Two'),
)


class BookPage(Page):
    body = StreamField(PageStreamBlock)
    template_string = models.CharField(max_length=250, choices=CHOICES, default='book/one.html')

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),

    ]
    settings_panels = Page.settings_panels + [
        FieldPanel('template_string')
    ]

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context['parent'] = self.get_parent().specific
    #     return context

    @property
    def index_page(self):
        return self.get_ancestors().type(BookIndex).last().specific

    @property
    def template(self):
        return self.template_string

