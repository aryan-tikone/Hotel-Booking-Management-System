from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.db.models import Q
from .models import (Amenities,Hotel,HotelBooking)
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail


def check_booking(start_date  , end_date ,uid , room_count):
    qs = HotelBooking.objects.filter(
        start_date__lte=start_date,
        end_date__gte=end_date,
        hotel__uid = uid
        )
    
    if len(qs) >= room_count:
        return False
    
    return True

def index(request):
    amenities_objs = Amenities.objects.all()
    hotel_objs = Hotel.objects.all()

    search=request.GET.get('search')
    amenities=request.GET.getlist('amenities')
 
    if search:
        hotel_objs=hotel_objs.filter(
            Q(hotel_name__icontains=search)|
            Q(description__icontains=search))
    if len(amenities):
        hotel_objs=hotel_objs.filter(amenities__amenity_name__in = amenities).distinct()
    contex = {'amenities_objs' : amenities_objs,'hotel_objs':hotel_objs,'search':search,'amenities':amenities}
    return render(request,'index.html',contex)

def hotel_detail(request, uid):
    hotel_obj = get_object_or_404(Hotel, uid=uid)

    if request.method == 'POST':
        # Get form data
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        room_type = request.POST.get('room_type')
        phone_number = int(request.POST.get('pno'))
        adults_count = request.POST.get('adults_count')
        children_count = request.POST.get('children_count')
        babies_count = request.POST.get('babies_count')
        email = request.POST.get('email')
        city = request.POST.get('city')

        # Validate form data

        if not checkin or not checkout or not phone_number or not email or not city:
            messages.error(request, "Please fill in all required fields.")
            return redirect(request.path)
      

        # Calculate the total price
        base_price = hotel_obj.hotel_price
        extra_charge = 500 if room_type == "AC" else 0
        total_price = base_price + extra_charge

        # Check room availability
        # if not check_booking(checkin, checkout, uid, hotel_obj.room_count):
        #     messages.warning(request, 'Hotel is already booked on these dates.')
        #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Create booking
        booking = HotelBooking.objects.create(
            hotel=hotel_obj,
            user=request.user,
            start_date=checkin,
            end_date=checkout,
            adults_count=adults_count,
            booking_type='post paid',
            children_count=children_count,
            babies_count=babies_count,
            email=email,
            city=city,
            total_price=total_price,
            phone_number=phone_number,
            room_type=room_type,
        )

        # Decrement room count
        hotel_obj.room_count -= 1
        hotel_obj.save()

        # Send email notification to the manager
        send_mail(
            subject=f"New Booking at {hotel_obj.hotel_name}",
            message=(
                f"New booking details:\n\n"
                f"Hotel: {hotel_obj.hotel_name}\n"
                f"Customer: {request.user.username}\n"
                f"Email: {email}\n"
                f"Phone: {phone_number}\n"
                f"Check-in: {checkin}\n"
                f"Check-out: {checkout}\n"
                f"Adults: {adults_count}, Children: {children_count}, Babies: {babies_count}\n"
                f"Room Type: {room_type}\n"
                f"City: {city}\n"
                f"Total Price: rs {total_price}\n"
            ),
            from_email="your_email@example.com",
            recipient_list=["jagtaponkar93@gmail.com","atikone18@gmail.com"],  
            fail_silently=False,
        )

        messages.success(request, 'Your booking has been saved, and an email has been sent to the hotel manager & he will contact you for payment .')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'hotel_detail.html', {'hotel_obj': hotel_obj})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect(reverse('index'))
    else:
        initial_data={'username':'','password1':'','password2':''}
        form = UserCreationForm(initial=initial_data)
   
    return render(request,'register.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect(reverse('index'))
    else:
        initial_data={'username':'','password':''}
        form = UserCreationForm(initial=initial_data)
   
    return render(request,'login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('index')

def reservations(request):
    if request.user.is_authenticated :
        bookings = HotelBooking.objects.filter(user=request.user)  # Fetch bookings for the logged-in user
        return render(request, 'reservations.html', {'bookings': bookings})
    else:
       
        return redirect('index')
        

