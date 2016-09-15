from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from .models import ArticleIndexPage, ArticlePage, ArticleCategory
from django.shortcuts import get_object_or_404
from django.conf import settings


def tag_view(request, tag):
    index = ArticleIndexPage.objects.first()
    return index.serve(request, tag=tag)


def category_view(request, category):
    index = ArticleIndexPage.objects.first()
    return index.serve(request, category=category)


def author_view(request, author):
    index = ArticleIndexPage.objects.first()
    return index.serve(request, author=author)


class LatestEntriesFeed(Feed):
    '''
    If a URL ends with "rss" try to find a matching BlogIndexPage
    and return its items.
    '''

    def get_object(self, request, article_slug):
        return get_object_or_404(ArticleIndexPage, slug=article_slug)

    def title(self, article):
        if article.seo_title:
            return article.seo_title
        return article.title

    def link(self, article):
        return article.full_url

    def description(self, article):
        return article.search_description

    def items(self, article):
        num = getattr(settings, 'ARTICLE_PAGINATION_PER_PAGE', 10)
        return article.get_descendants()[:num]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.specific.body

    def item_link(self, item):
        return item.full_url


class LatestEntriesFeedAtom(LatestEntriesFeed):
    feed_type = Atom1Feed


class LatestCategoryFeed(Feed):
    description = "An Article"

    def title(self, category):
        return "Article: " + category.name

    def link(self, category):
        return "/article/category/" + category.slug

    def get_object(self, request, category):
        return get_object_or_404(ArticleCategory, slug=category)

    def items(self, obj):
        return ArticlePage.objects.filter(
            categories__category=obj).order_by('-date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body
