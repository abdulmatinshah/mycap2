from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel

'''
Create carousel
Fields:
    image
    embed_url
    link:
        external
        page
        document
'''
class LinkFields(models.Model):
    external_link = models.URLField('External url', blank=True)
    page_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    document_link = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('external_link'),
        PageChooserPanel('page_link'),
        DocumentChooserPanel('document_link')
    ]

    @property
    def link(self):
        if self.page_link:
            return self.page_link.url
        elif self.ducument_link:
            return self.document_link.url
        else:
            return self.external_link

    class Meta:
        abstract = True


class CarouselItem(LinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    embed_link = models.URLField('Embed URL', null=True, blank=True)
    caption = models.CharField(max_length=250, null=True, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_link'),
        FieldPanel('caption'),
    ] + LinkFields.panels

    class Meta:
        abstract = True

