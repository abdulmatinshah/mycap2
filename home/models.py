from __future__ import absolute_import, unicode_literals

from mycap.utils import *
from mycap.util_streamfield import *


class HomePageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('HomePage', related_name='carousel_items')


class HomePage(Page):
    body = StreamField(PageStreamBlock(), null=True, blank=True)

HomePage.content_panels = [
    InlinePanel('carousel_items', label='Carousel items'),
    StreamFieldPanel('body')
]
