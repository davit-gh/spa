from django.db import models
from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import RichText, Orderable, Slugged

from mezzanine.utils.models import upload_to
from mezzanine.core.models import RichText, Orderable
from mezzanine.pages.models import Page
from django.utils.translation import ugettext_lazy as _

class HomePage(Page, RichText):
    '''
    A page representing the format of the home page
    '''

    content_heading = models.CharField(max_length=200,
        default="About us!")
    featured_portfolio = models.ForeignKey("Portfolio", blank=True, null=True,
        help_text="If selected items from this portfolio will be featured "
                  "on the home page.")

    class Meta:
        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")


class Slide(Orderable):
    '''
    A slide in a slider connected to a HomePage
    '''
    homepage = models.ForeignKey(HomePage, related_name="slides")
    image_back = FileField(verbose_name=_("Image back"),
        upload_to=upload_to("main.static.image", "slider"),
        format="Image", max_length=255, null=True, blank=True)

    image_front = FileField(verbose_name=_("Image front"),
        upload_to=upload_to("main.static.image", "slider"),
        format="Image", max_length=255, null=True, blank=True)
    text = models.CharField(verbose_name=_("Slide text"), max_length=400, blank=True)
    class Meta:
        verbose_name = _("Slide")
        verbose_name_plural = _("Slides")

COLUMN_CHOICES = (
    ('6', 'Two columns'), # 2 columns use span6
    ('4', 'Three columns'), # 3 columns use span4
    ('3', 'Four columns'), # 4 columns use span3
)

class Portfolio(Page):
    '''
    A collection of individual portfolio items
    ''' 
    content = RichTextField(blank = True)
    columns = models.CharField(max_length=1,choices=COLUMN_CHOICES,default='3')
    class Meta:
        verbose_name = _("Portfolio")
        verbose_name_plural = _("Portfolios")

class PortfolioItem(Page, RichText):
    
    featured_image = FileField(verbose_name=_("Featured Image"), upload_to=
            upload_to("main.PortfolioItem.featured_image", "portfolio"),\
            format="Image", max_length=255, null=True, blank=True)

    short_description = RichTextField(blank=True)
    categories = models.ManyToManyField("PortfolioItemCategory", 
            verbose_name=_("Categories"),\
            blank=True, related_name="portfolioitems")
    href = models.CharField(max_length=2000, blank=True,\
            help_text = "A link to the finished project (optional)")
    class Meta:
        verbose_name = _("Portfolio item")
        verbose_name_plural = _("Portfolio items")


class PortfolioItemImage(Orderable):
    portfolioitem = models.ForeignKey(PortfolioItem, related_name="images")
    file = FileField(_("File"), max_length=200, format="Image",\
        upload_to=upload_to("main.PortfolioItemImage.file", "portfolio items"))
    class Meta:
        verbose_name="Portfolio Item Image"
        verbose_name_plural="Portfolio Item Images"

class PortfolioItemCategory(Slugged):
    """
    A category for grouping portfolio items into a series.
    """
    
    class Meta:
        verbose_name=_("Portfolio Item Category")
        verbose_name_plural=_("Portfolio Item Categories")
        ordering=("title",)
