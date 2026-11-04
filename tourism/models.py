from django.db import models


class District(models.Model):

    name = models.CharField(
        max_length=100
    )

    slug = models.SlugField(
        unique=True
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to='districts/',
        blank=True,
        null=True
    )


    def __str__(self):

        return self.name


class Destination(models.Model):

    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='destinations'
    )

    name = models.CharField(
        max_length=150
    )

    category = models.CharField(
        max_length=100
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to='destinations/',
        blank=True,
        null=True
    )

    best_time = models.CharField(
        max_length=200,
        blank=True
    )

    approx_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    famous_for=models.TextField(blank=True)

    location = models.CharField(
        max_length=255,
        blank=True
    )

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True
    )


    def __str__(self):

        return self.name

 # =========================================
# DESTINATION IMAGES
# =========================================

class DestinationImage(models.Model):

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='gallery'
    )

    image = models.ImageField(
        upload_to='destinations/gallery/'
    )

    caption = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return f"{self.destination.name} - Image"

 