
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

    return render(
        request,
        "tourism/tripbuilder.html"
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
