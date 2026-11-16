import json
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from .models import District, Destination


# =================================
# HOME PAGE
# =================================

def home(request):

    # Fetch all districts from the database
    districts = District.objects.all().order_by("name")

    # Check whether visitor clicked View All Districts
    show_all = request.GET.get("show_all") == "1"

    # Show only 5 districts initially
    if show_all:
        displayed_districts = districts
    else:
        displayed_districts = districts[:5]

    context = {
        "districts": displayed_districts,
        "show_all": show_all,
        "total_districts": districts.count(),
    }

    return render(request, "tourism/home.html", context)


# =================================
# DISTRICT DETAILS PAGE
# =================================

def district_detail(request, slug):

    # Find district using its name, not slug
    district = get_object_or_404(
        District,
        name__iexact=slug
    )

    # Fetch destinations belonging to this district
    destinations = district.destinations.all()

    return render(
        request,
        "tourism/districtcards.html",
        {
            "district": district,
            "destinations": destinations
        }
    )


# =================================
# DESTINATION DETAILS PAGE
# =================================

def destination_detail(request, pk):

    destination = get_object_or_404(
        Destination,
        pk=pk
    )

    return render(
        request,
        "tourism/destinationdetails.html",
        {
            "destination": destination
        }
    )



# =========================================
# TRIP BUILDER & BUDGET
# =========================================

def trip_builder(request):

    districts = District.objects.prefetch_related(
        "destinations"
    ).order_by("name")

    destinations = Destination.objects.select_related(
        "district"
    ).order_by("district__name", "name")

    destination_data = []

    for destination in destinations:

        image_url = ""

        if destination.image:
            try:
                image_url = destination.image.url
            except ValueError:
                image_url = ""

        destination_data.append({

            "id": destination.id,
            "name": destination.name,
            "district_id": destination.district_id,
            "district_name": destination.district.name,
            "category": destination.category,
            "description": destination.description,
            "image": image_url,
            "best_time": destination.best_time,

            "approx_cost": (
                float(destination.approx_cost)
                if destination.approx_cost is not None
                else 0
            ),

            "famous_for": destination.famous_for,
            "location": destination.location,

            "latitude": (
                float(destination.latitude)
                if destination.latitude is not None
                else None
            ),

            "longitude": (
                float(destination.longitude)
                if destination.longitude is not None
                else None
            ),

        })

    context = {
        "districts": districts,
        "total_districts": districts.count(),
        "total_destinations": len(destination_data),
        "destination_data": destination_data,
    }

    print("TOTAL DISTRICTS:", districts.count())
    print("TOTAL DESTINATIONS:", len(destination_data))
    print("DESTINATION DATA:", destination_data[:2])

    return render(
        request,
        "tourism/tripbuilder.html",
        context
    )


# =========================================
# UTKALA GO: WHAT YOU LIKE FILTER
# =========================================

def filter_destinations(request):

    categories = [
        "Waterfall",
        "Temple",
        "Beach",
        "Wildlife",
        "Nature",
        "Adventure",
        "Lake & Natural Attraction",
        "Historical Place",
        "Hill Station",
        "Dam",
        "Port",
    ]

    selected_categories = request.GET.getlist("category")
    search_query = request.GET.get("q", "").strip()

    destinations = Destination.objects.select_related(
        "district"
    ).all()

    # Filter by selected interests
    if selected_categories:

        category_query = Q()

        for category in selected_categories:
            category_query |= Q(category__icontains=category)

        destinations = destinations.filter(category_query)

    # Search destination name, description or district
    if search_query:

        destinations = destinations.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(district__name__icontains=search_query)
        )

    destinations = destinations.order_by("name").distinct()

    context = {
        "categories": categories,
        "selected_categories": selected_categories,
        "search_query": search_query,
        "destinations": destinations,
        "has_filter": bool(selected_categories or search_query),
    }

    return render(
        request,
        "tourism/filter.html",
        context
    )
