from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    product_count = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='categories/')
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.slug == 'complete-skateboards':
            return reverse('shop:complete_skateboards')
        return reverse('shop:categories')


class Product(models.Model):
    LEVEL_BEGINNER = 'Beginner'
    LEVEL_INTERMEDIATE = 'Intermediate'
    LEVEL_PRO = 'Pro'

    LEVEL_CHOICES = [
        (LEVEL_BEGINNER, 'Beginner'),
        (LEVEL_INTERMEDIATE, 'Intermediate'),
        (LEVEL_PRO, 'Pro'),
    ]

    WIDTH_75 = 'w75'
    WIDTH_775 = 'w775'
    WIDTH_80 = 'w80'

    WIDTH_CHOICES = [
        (WIDTH_75, '7.5"'),
        (WIDTH_775, '7.75"'),
        (WIDTH_80, '8.0" and above'),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    brand = models.CharField(max_length=80)
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True)

    title = models.CharField(max_length=180)
    description = models.CharField(max_length=180)
    long_description = models.TextField()

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default=LEVEL_BEGINNER
    )

    width = models.CharField(
        max_length=20,
        choices=WIDTH_CHOICES,
        default=WIDTH_80
    )

    price = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.8)
    reviews = models.PositiveIntegerField(default=0)

    image = models.ImageField(upload_to='products/')
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f'{self.brand} — {self.name}'

    @property
    def price_display(self):
        return f'${self.price}'

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})


class ProductGalleryImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ImageField(upload_to='product-gallery/')
    alt_text = models.CharField(max_length=160, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Product gallery image'
        verbose_name_plural = 'Product gallery images'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f'Gallery image for {self.product}'


class ProductSpecification(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='specifications'
    )
    text = models.CharField(max_length=220)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.text