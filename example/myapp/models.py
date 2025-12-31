from django.db import models
from django.core.validators import MinValueValidator


class CoffeeBean(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    origin = models.CharField(max_length=100, verbose_name="Origin")
    roast_level = models.CharField(max_length=50, verbose_name="Roast Level")
    flavor_notes = models.TextField(verbose_name="Flavor Notes")
    stock_quantity = models.PositiveIntegerField(
        verbose_name="Stock Quantity", default=0
    )

    def __str__(self):
        return self.name


class Floorplan(models.Model):
    PLAN_2D = "2d"
    PLAN_3D = "3d"
    FLOORPLAN_TYPE_CHOICES = [
        (PLAN_2D, "2D"),
        (PLAN_3D, "3D"),
    ]
    FURNITURE_MODERN = "modern"
    FURNITURE_ARCHAIC = "archaic"
    FURNITURE_STYLE_CHOICES = [
        (FURNITURE_MODERN, "Modern"),
        (FURNITURE_ARCHAIC, "Traditionell"),
    ]
    RES_1080 = "1080"
    RES_2160 = "2160"
    RESOLUTION_CHOICES = [
        (RES_1080, "1080p"),
        (RES_2160, "2160p"),
    ]

    # general
    plan_type = models.CharField(
        max_length=2,
        verbose_name="Grundriss-Typ",
        choices=FLOORPLAN_TYPE_CHOICES,
    )
    number_of_floorplans = models.IntegerField(
        verbose_name="Anzahl Grundrisse",
        default=1,
        validators=[MinValueValidator(1)],
    )

    # personal information
    first_name = models.CharField(max_length=255, verbose_name="Vorname")
    last_name = models.CharField(max_length=255, verbose_name="Nachname")
    street = models.CharField(max_length=255, verbose_name="Straße")
    postcode = models.CharField(max_length=5, verbose_name="Postleitzahl")
    city = models.CharField(max_length=255, verbose_name="Stadt")
    country = models.CharField(max_length=255, verbose_name="Land")

    # 3d
    furniture_style = models.CharField(
        max_length=255,
        verbose_name="Einrichtungsstil",
        choices=FURNITURE_STYLE_CHOICES,
        blank=False,
        default=FURNITURE_MODERN,
    )
    show_measurements = models.BooleanField(
        default=False,
        verbose_name="Maße im Grundriss anzeigen",
    )

    # 2d
    resolution = models.CharField(
        max_length=255,
        verbose_name="Auflösung",
        choices=RESOLUTION_CHOICES,
        blank=False,
        default=RES_1080,
    )
    show_furniture = models.BooleanField(
        default=False,
        verbose_name="Möbel anzeigen",
    )

    @property
    def unit_price(self) -> int:
        if self.plan_type == self.PLAN_3D:
            return 39
        # 2d
        return 29 + (10 if self.resolution == self.RES_2160 else 0)

    @property
    def total_price(self) -> int:
        return self.unit_price * self.number_of_floorplans
