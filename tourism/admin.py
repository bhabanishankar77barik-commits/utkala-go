from django.contrib import admin
from .models import Destination, DestinationImage, District


# =========================================
# DISTRICT ADMIN
# =========================================

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'slug',
    )

    prepopulated_fields = {
        'slug': ('name',)
    }


# =========================================
# DESTINATION ADMIN
# =========================================

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'district',
        'category',
        'famous_for',
    )

    list_filter = (
        'district',
        'category',
    )
    # =========================================
# DESTINATION IMAGE ADMIN
# =========================================

@admin.register(DestinationImage)
class DestinationImageAdmin(admin.ModelAdmin):

    list_display = (
        'destination',
        'caption',
    )

    list_filter = (
        'destination',
    )