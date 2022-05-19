from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Photo
import logging

logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Photo)
def generate_image_thumbnail(sender, instance, **kwargs):
    logger.info(f"Generating Thumbnail for  '{instance.image.name}'")
    instance.generate_thumbnail(instance.image, instance.thumbnail)
