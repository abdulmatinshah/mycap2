from mycap.utils import *
from mycap.util_streamfield import *


class ContentPageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('content_page.ContentPage', related_name='carousel_items')


class ContentPage(Page):
    intro = models.CharField(max_length=250, null=True, blank=True)
    body = StreamField(PageStreamBlock(), null=True, blank=True)


ContentPage.content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname='full'),
        StreamFieldPanel('body'),
        InlinePanel('carousel_items', label='Carousel items')
    ]
