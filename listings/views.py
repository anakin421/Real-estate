from django.shortcuts import get_object_or_404, render
from .models import Listing
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def index(request):

  listings = Listing.objects.filter(is_published=True)

  paginator = Paginator(listings, 15)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'listings': paged_listings
  }

  return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
  return render(request, 'listings/listing.html')

def search(request):
  return render(request, 'listings/search.html')
