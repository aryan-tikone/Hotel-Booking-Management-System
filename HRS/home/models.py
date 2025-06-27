from django.contrib.auth.models import User
from django.db import models
from curses.ascii import US
import uuid


class BaseModel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class Amenities(BaseModel):
    amenity_name=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.amenity_name

class Hotel(BaseModel):
    hotel_name=models.CharField(max_length=100)
    hotel_price=models.IntegerField()
    description=models.TextField()
    place=models.TextField()
    amenities=models.ManyToManyField(Amenities)
    room_count=models.IntegerField(default=10)

    def __str__(self) -> str:
        return self.hotel_name

class hotelimages(BaseModel):
    hotel=models.ForeignKey(Hotel,related_name="hotel_images",on_delete=models.CASCADE)
    images = models.ImageField(upload_to = "hotels")


class HotelBooking(BaseModel):
    hotel = models.ForeignKey(Hotel, related_name="hotel_booking", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_booking", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    booking_type = models.CharField(
        max_length=100,
        choices=(('pre paid', 'Pre Paid'), ('post paid', 'Post Paid'))
    )
    total_price = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    room_type = models.CharField(
        max_length=10,
        
        null=True, blank=True
    )
    adults_count = models.IntegerField(default=1)
    children_count = models.IntegerField(default=0)
    babies_count = models.IntegerField(default=0)
    email = models.EmailField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Booking by {self.user.username} at {self.hotel.hotel_name}"

