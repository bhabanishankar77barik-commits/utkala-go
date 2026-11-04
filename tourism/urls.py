from django.urls import path

from . import views


urlpatterns = [

    # =================================
    # HOME PAGE
    # =================================

    path("", views.home, name="home"),

    path("filter/", views.filter_destinations, name="filter_destinations"),




    # =================================
    # DISTRICT DETAILS
    # =================================

    path(
        'district/<slug:slug>/',
        views.district_detail,
        name='district_detail'
    ),


    # =================================
    # DESTINATION DETAILS
    # =================================

    path(
        'destination/<int:pk>/',
        views.destination_detail,
        name='destination_detail'
    ),

# =========================================
# TRIP BUILDER & BUDGET
# =========================================

path(
    'trip-builder/',
    views.trip_builder,
    name='trip_builder'
),

path(
    "filter/",
    views.filter_destinations,
    name="filter_destinations",
),

]