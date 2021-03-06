from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


# utility field through abstract classes
class ContactFields(models.Model):
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    post_code = models.CharField(max_length=10, blank=True)

    panels = [
        FieldPanel('telephone'),
        FieldPanel('email'),
        FieldPanel('address_1'),
        FieldPanel('address_2'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('post_code'),
    ]

    class Meta:
        abstract = True


# classes
class MemberIndex(Page):
    subpage_types = ['member.MemberPage']

    @property
    def members(self):
        members = MemberPage.objects.live().descendant_of(self)
        return members


from wagtail.wagtailcore.models import Orderable
from modelcluster.fields import ParentalKey

class ImageLink(models.Model):
    imagelink = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    panels = [
        ImageChooserPanel('imagelink')
    ]


class ImageGallery(Orderable, ImageLink):
    page = ParentalKey('MemberPage', related_name='image_gallery')


class MemberPage(Page, ContactFields):
    full_name = models.CharField(max_length=255)
    intro = RichTextField(blank=True)
    biography = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('full_name'),
        index.SearchField('intro'),
        index.SearchField('biography'),
    ]
    parent_page_types = ['member.MemberIndex']


MemberPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('full_name'),
    FieldPanel('intro', classname="full"),
    FieldPanel('biography', classname="full"),
    ImageChooserPanel('image'),
    MultiFieldPanel(ContactFields.panels, "Contact"),
    InlinePanel('image_gallery', label="Image Gallery"),
]

MemberPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]
