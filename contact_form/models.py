
from modelcluster.fields import ParentalKey
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailcore.fields import RichTextField
from django.db import models
'''
class GoogleMapBlock(blocks.StructBlock):
    map_long = blocks.CharBlock(required=True, max_length=255)
    map_lat = blocks.CharBlock(required=True, max_length=255)
    map_zoom_level = blocks.CharBlock(default=14, required=True, max_length=3)

    class Meta:
        template = 'contact_form/blocks/google_map.html'
        icon = 'cogs'
        label = 'Google Map'

'''


class GoogleMap(models.Model):
    map_long = models.CharField(max_length=255, null=True, blank=True)
    map_lat = models.CharField(max_length=255, null=True, blank=True)
    map_zoom_level = models.CharField(max_length=3, default=14, null=True, blank=True)
    panels = [
        FieldPanel('map_long'),
        FieldPanel('map_lat'),
        FieldPanel('map_zoom_level'),
    ]

    class Meta:
        abstract = True


class FormFields(AbstractFormField):
    page = ParentalKey('ContactForm', related_name='form_fields')


class ContactForm(AbstractEmailForm, GoogleMap):
    intro = RichTextField(null=True)
    thank_you_text = RichTextField(blank=True)
ContactForm.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel('form_fields', label="Form fields"),
    FieldPanel('thank_you_text', classname="full"),
    MultiFieldPanel([
        FieldPanel('to_address', classname="full"),
        FieldPanel('from_address', classname="full"),
        FieldPanel('subject', classname="full"),
    ], "Email"),
    MultiFieldPanel(GoogleMap.panels, 'Google map'),

]
