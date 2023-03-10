from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from ...common.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(_("Slug"), max_length=100, unique=True, blank=True)
    description = models.TextField(max_length=255, blank=True)
    image = models.ImageField(upload_to="categories")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def get_absolute_url(self):
        return reverse("store:product_list_view", args=[self.slug])

    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save()
