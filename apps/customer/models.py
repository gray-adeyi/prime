from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import logging

logger = logging.getLogger(__name__)


class ThumbnailMixin:
    """
    Mixin to generate thumbnails
    from the source `ImageField`
    and save it in the target `ImageField`
    """
    THUMBNAIL_SIZE = (300, 300)

    def _generate_thumbnail(self, src_img, format='JPEG'):
        """
        Function helps in the generation of the thumbnail
        """
        logger.info("generating thumbnail")
        img = Image.open(src_img)
        img = img.convert('RGB')
        img.thumbnail(self.THUMBNAIL_SIZE, Image.ANTIALIAS)
        thumbnail_img = BytesIO()
        img.save(thumbnail_img, format=format)
        thumbnail_img.seek(0)
        return thumbnail_img

    def generate_thumbnail(self, src_field: models.ImageField, dest_field: models.ImageField) -> None:
        """
        Generates thumbnail of image of the
        source field `src_field` and saves
        it in the destination field `dest_field`
        """
        thumbnail = self._generate_thumbnail(src_img=src_field)
        dest_field.save(
            src_field.name,
            ContentFile(thumbnail.read()),
            save=False,
        )
        thumbnail.close()


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=50, blank=True)
    logo = models.ImageField(upload_to='customer/logo/images', blank=True)

    def __str__(self) -> str:
        return self.business_name if self.business_name is not None else self.user.firstname
        # return str(self.id)


class Job(models.Model):

    # TODO: Add more job type options
    JOB_TYPE_OPTIONS = (
        ('0', '4x6'),
        ('1', '5x7'),
        ('2', '8x10'),
    )

    STATUS_OPTIONS = (
        ('0', 'booking'),
        ('1', 'processing'),
        ('2', 'completed'),
        ('3', 'delivered'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    copies = models.PositiveIntegerField(blank=True)
    price_per_unit = models.DecimalField(
        max_digits=8, decimal_places=2, default=Decimal(50.0))
    write_up = models.TextField(max_length=200, blank=True)
    job_type = models.CharField(
        max_length=2, choices=JOB_TYPE_OPTIONS, default=JOB_TYPE_OPTIONS[1][0])
    status = models.CharField(
        max_length=2, choices=STATUS_OPTIONS, default=STATUS_OPTIONS[0][0])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.customer} job @ {self.timestamp}"

    @property
    def total_price(self):
        return sum([exposure.total_price for exposure in self.exposures.all()])

    @property
    def copies_count(self):
        self.update_copies()
        self.save()
        return self.copies

    def update_copies(self):
        self.copies = sum([photo.copies for photo in self.exposures.all()])


class Photo(ThumbnailMixin, models.Model):
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="exposures")
    image = models.ImageField()
    thumbnail = models.ImageField(blank=True)
    copies = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return str(self.image)

    # TODO: Implement logic
    @property
    def total_price(self):
        return self.job.price_per_unit * self.copies
