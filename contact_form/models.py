
from modelcluster.fields import ParentalKey
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailcore.fields import RichTextField


class FormFields(AbstractFormField):
    page = ParentalKey('ContactForm', related_name='form_fields')


class ContactForm(AbstractEmailForm):
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
    ], "Email")
]
