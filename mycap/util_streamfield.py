from django import forms
from wagtail.wagtailcore.blocks import StructBlock, StreamBlock, TextBlock, CharBlock, RichTextBlock, FieldBlock, RawHTMLBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel


class PullQuoteBlock(StructBlock):
    quote = TextBlock('Quote title')
    attribution = CharBlock()

    class Meta:
        icon = 'openquote'


class ImageAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=[
        ('left', 'Wrap Left'),
        ('right', 'Wrap right'),
        ('mid', 'Mid width'),
        ('full', 'Full width'),
    ], )


class ImageAlignedBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageAlignmentChoiceBlock()


class HtmlAlignedFieldBlock(FieldBlock):
    field = forms.ChoiceField(choices=[
        ('normal', 'Normal'),
        ('full', 'Full width'),
    ])

    class Meta:
        icon = 'code'


class HtmlAlignedBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HtmlAlignedFieldBlock()


class PageStreamBlock(StreamBlock):
    h2 = CharBlock(icon='title')
    h3 = CharBlock(icon='title')
    h4 = CharBlock(icon='title')
    intro = RichTextBlock(icon='pilcrow', classname='full')
    pullquote = PullQuoteBlock()
    aligned_image = ImageAlignedBlock(label="Aligned image", icon="image")
    aligned_html = HtmlAlignedBlock(label='Aligned html', icon='pilcrow')
    document = DocumentChooserBlock(icon='doc-full-inverse')
