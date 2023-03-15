from django.db import models
# from datetime import datetime
from realtors.models import Realtor

class Listing(models.Model):
  realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING)
  property_id = models.IntegerField(unique = True,default=0)
  title = models.CharField(max_length=200)
  address = models.CharField(max_length=200)
  city = models.CharField(max_length=20)
  state = models.CharField(max_length=20)
  description = models.TextField(blank=True)
  price = models.CharField(max_length=20)
  bedrooms = models.IntegerField()
  bathrooms = models.IntegerField()
  parking = models.CharField(max_length=20,blank=True,null=True)
  sqft = models.IntegerField(blank=True)
  photo_main = models.ImageField(default='default.jpg', upload_to='property_images')
  photo_1 = models.ImageField(blank=True, upload_to='property_images')
  photo_2 = models.ImageField(blank=True, upload_to='property_images')
  photo_3 = models.ImageField(blank=True, upload_to='property_images')
  photo_4 = models.ImageField(blank=True, upload_to='property_images')
  photo_5 = models.ImageField(blank=True, upload_to='property_images')
  photo_6 = models.ImageField(blank=True, upload_to='property_images')
  is_published = models.BooleanField(default=True)
  list_date = models.CharField(max_length=30)

  def __str__(self):
    return self.title