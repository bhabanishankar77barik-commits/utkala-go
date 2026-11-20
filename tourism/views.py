import json
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from .models import District, Destination


# =================================
# HOME PAGE
# =================================

def home(request):
    query = request.GET.get("q", "").strip()
    districts = District.objects.all().order_by("name")
    matching_spots = Destination.objects.none()

    if query:
        districts = districts.filter(
            Q(name__icontains=query)
            | Q(destinations__name__icontains=query)
            | Q(destinations__description__icontains=query)
            | Q(destinations__famous_for__icontains=query)
        ).distinct()

        matching_spots = Destination.objects.select_related("district").filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(district__name__icontains=query)
            | Q(famous_for__icontains=query)
        ).distinct()

        displayed_districts = districts
        show_all = True
    else:
        show_all = request.GET.get("show_all") == "1"
        displayed_districts = districts if show_all else districts[:5]

    context = {
        "districts": displayed_districts,
        "matching_spots": matching_spots,
        "show_all": show_all,
        "total_districts": districts.count(),
        "search_query": query,
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
    districts = District.objects.prefetch_related("destinations").order_by("name")

    districts_data = []
    for district in districts:
        # Use district latitude/longitude if your District model has them, otherwise fallback
        d_lat = getattr(district, "latitude", None)
        d_lng = getattr(district, "longitude", None)

        spots_list = []
        valid_lats = []
        valid_lngs = []

        for spot in district.destinations.all().order_by("name"):
            s_lat = float(spot.latitude) if spot.latitude is not None else None
            s_lng = float(spot.longitude) if spot.longitude is not None else None
            if s_lat is not None and s_lng is not None:
                valid_lats.append(s_lat)
                valid_lngs.append(s_lng)

            spots_list.append({
                "id": str(spot.id),
                "name": spot.name,
                "description": spot.description or "",
                "ticket": float(spot.approx_cost) if spot.approx_cost is not None else 0,
                "coords": {
                    "lat": s_lat,
                    "lng": s_lng,
                },
            })

        # Fallback district coordinates to average of its spots or Odisha center (20.9517, 85.0985)
        final_d_lat = (
            float(d_lat) if d_lat is not None
            else (sum(valid_lats) / len(valid_lats) if valid_lats else 20.9517)
        )
        final_d_lng = (
            float(d_lng) if d_lng is not None
            else (sum(valid_lngs) / len(valid_lngs) if valid_lngs else 85.0985)
        )

        # Ensure every spot has valid numeric coords so haversineKm never returns NaN
        for s in spots_list:
            if s["coords"]["lat"] is None:
                s["coords"]["lat"] = final_d_lat
            if s["coords"]["lng"] is None:
                s["coords"]["lng"] = final_d_lng

        districts_data.append({
            "id": str(district.id),
            "name": district.name,
            "coords": {
                "lat": final_d_lat,
                "lng": final_d_lng,
            },
            "spots": spots_list,
        })

    context = {
        "districts": districts,
        "districts_data": districts_data,
        "initial_district_id": str(request.GET.get("district", "")),
    }
    return render(request, "tourism/tripbuilder.html", context)


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
