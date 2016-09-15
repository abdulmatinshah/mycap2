from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsearch import index
from taggit.models import TaggedItemBase, Tag
from modelcluster.tags import ClusterTaggableManager
from modelcluster.fields import ParentalKey
import datetime


COMMENTS_APP = getattr(settings, 'COMMENTS_APP', None)


def get_article_context(context):
    """ Get context data useful on all blog related pages """
    context['authors'] = get_user_model().objects.filter(
        owned_pages__live=True,
        owned_pages__content_type__model='articlepage'
    ).annotate(Count('owned_pages')).order_by('-owned_pages__count')
    context['all_categories'] = ArticleCategory.objects.all()
    context['root_categories'] = ArticleCategory.objects.filter(
        parent=None,
    ).prefetch_related(
        'children',
    ).annotate(
        article_count=Count('articlepage'),
    )
    return context


class ArticleIndexPage(Page):
    @property
    def articles(self):
        # Get list of blog pages that are descendants of this page
        articles = ArticlePage.objects.descendant_of(self).live()
        articles = articles.order_by(
            '-date'
        ).select_related('owner').prefetch_related(
            'tagged_items__tag',
            'categories',
            'categories__category',
        )
        return articles

    def get_context(self, request, tag=None, category=None, author=None, *args, **kwargs):
        context = super(ArticleIndexPage, self).get_context(
            request, *args, **kwargs)
        articles = self.articles

        if tag is None:
            tag = request.GET.get('tag')
        if tag:
            articles = articles.filter(tags__slug=tag)
        if category is None:  # Not coming from category_view in views.py
            if request.GET.get('category'):
                category = get_object_or_404(
                    ArticleCategory, slug=request.GET.get('category'))
        if category:
            if not request.GET.get('category'):
                category = get_object_or_404(ArticleCategory, slug=category)
                articles = articles.filter(categories__category__name=category)
        if author:
            if isinstance(author, str) and not author.isdigit():
                articles = articles.filter(author__username=author)
            else:
                articles = articles.filter(author_id=author)

        # Pagination
        page = request.GET.get('page')
        page_size = 10
        if hasattr(settings, 'ARTICLE_PAGINATION_PER_PAGE'):
            page_size = settings.ARTICLE_PAGINATION_PER_PAGE

        if page_size is not None:
            paginator = Paginator(articles, page_size)  # Show 10 blogs per page
            try:
                articles = paginator.page(page)
            except PageNotAnInteger:
                articles = paginator.page(1)
            except EmptyPage:
                articles = paginator.page(paginator.num_pages)

        context['articles'] = articles
        context['category'] = category
        context['tag'] = tag
        context['author'] = author
        context['COMMENTS_APP'] = COMMENTS_APP
        context = get_article_context(context)

        return context

    class Meta:
        verbose_name = _('Article index')
    subpage_types = ['articles.ArticlePage']


@register_snippet
class ArticleCategory(models.Model):
    name = models.CharField(
        max_length=80, unique=True, verbose_name=_('Category Name'))
    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name="children",
        help_text=_(
            'Categories, unlike tags, can have a hierarchy. You might have a '
            'Jazz category, and under that have children categories for Bebop'
            ' and Big Band. Totally optional.')
    )
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _("Article Category")
        verbose_name_plural = _("Article Categories")

    panels = [
        FieldPanel('name'),
        FieldPanel('parent'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError('Parent category cannot be self.')
            if parent.parent and parent.parent == self:
                raise ValidationError('Cannot have circular Parents.')

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            count = ArticleCategory.objects.filter(slug=slug).count()
            if count > 0:
                slug = '{}-{}'.format(slug, count)
            self.slug = slug
        return super(ArticleCategory, self).save(*args, **kwargs)


class ArticleCategoryArticlePage(models.Model):
    category = models.ForeignKey(
        ArticleCategory, related_name="+", verbose_name=_('Category'))
    page = ParentalKey('ArticlePage', related_name='categories')
    panels = [
        FieldPanel('category'),
    ]


class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey('ArticlePage', related_name='tagged_items')


@register_snippet
class ArticleTag(Tag):
    class Meta:
        proxy = True


def limit_author_choices():
    """ Limit choices in blog author field based on config settings """
    LIMIT_AUTHOR_CHOICES = getattr(settings, 'ARTICLE_LIMIT_AUTHOR_CHOICES_GROUP', None)
    if LIMIT_AUTHOR_CHOICES:
        if isinstance(LIMIT_AUTHOR_CHOICES, str):
            limit = Q(groups__name=LIMIT_AUTHOR_CHOICES)
        else:
            limit = Q()
            for s in LIMIT_AUTHOR_CHOICES:
                limit = limit | Q(groups__name=s)
        if getattr(settings, 'ARTICLE_LIMIT_AUTHOR_CHOICES_ADMIN', False):
            limit = limit | Q(is_staff=True)
    else:
        limit = {'is_staff': True}
    return limit


class ArticlePage(Page):

    body = RichTextField(verbose_name=_('body'), blank=True)
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)
    date = models.DateField(
        _("Post date"), default=datetime.datetime.today,
        help_text=_("This date may be displayed on the blog post. It is not "
                    "used to schedule posts to go live at a later date.")
    )
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Header image')
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, null=True,
        limit_choices_to=limit_author_choices,
        verbose_name=_('Author'),
        on_delete=models.SET_NULL,
        related_name='author_pages',
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    article_categories = models.ManyToManyField(
        ArticleCategory, through=ArticleCategoryArticlePage, blank=True)

    settings_panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('go_live_at'),
                FieldPanel('expire_at'),
            ], classname="label-above"),
        ], 'Scheduled publishing', classname="publishing"),
        FieldPanel('date'),
        FieldPanel('author'),
    ]

    def save_revision(self, *args, **kwargs):
        if not self.author:
            self.author = self.owner
        return super(ArticlePage, self).save_revision(*args, **kwargs)

    def get_absolute_url(self):
        return self.url

    def get_article_index(self):
        # Find closest ancestor which is a blog index
        return self.get_ancestors().type(ArticleIndexPage).last()

    def get_context(self, request, *args, **kwargs):
        context = super(ArticlePage, self).get_context(request, *args, **kwargs)
        context['articles'] = self.get_article_index().articleindexpage.articles
        context = get_article_context(context)
        context['COMMENTS_APP'] = COMMENTS_APP
        return context

    class Meta:
        verbose_name = _('Article page')
        verbose_name_plural = _('Article pages')

    parent_page_types = ['articles.ArticleIndexPage']


ArticlePage.content_panels = [
    FieldPanel('title', classname="full title"),
    MultiFieldPanel([
        FieldPanel('tags'),
        InlinePanel('categories', label=_("Categories")),
    ], heading="Tags and Categories"),
    ImageChooserPanel('header_image'),
    FieldPanel('body', classname="full"),
]
