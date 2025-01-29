from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import F
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Car, Rental

def update_rental_availability():
    today = now().date()

    expired_rentals = Rental.objects.filter(end_date__lt=today)

    for rental in expired_rentals:
        rental.car.available = True
        rental.car.save()
        rental.delete()

@login_required
def index(request):

    update_rental_availability()
    available_cars = Car.objects.filter(available=True)  
    return render(request, "rentals/index.html", {"available_cars": available_cars})


@login_required
def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        
        if start_date and end_date:
            rental = Rental(user=request.user, car=car, start_date=start_date, end_date=end_date)
            rental.save()
            car.available = False
            car.save()
            return redirect("rentals:index")
    
    return render(request, "rentals/car_detail.html", {"car": car})


@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    
    if not car.available:
        return render(request, "rentals/car_detail.html", {
            "car": car,
            "error_message": "Toto auto nie je momentálne dostupné na prenájom.",
        })

    if request.method == "POST":
        start_date_str = request.POST["start_date"]
        end_date_str = request.POST["end_date"]

        try:
            start_date = timezone.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = timezone.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            return render(request, "rentals/car_detail.html", {
                "car": car,
                "error_message": "Dátumy musia byť vo formáte YYYY-MM-DD.",
            })

        today = timezone.now().date()

        if start_date < today:
            return render(request, "rentals/car_detail.html", {
                "car": car,
                "error_message": "Začiatok prenájmu nemôže byť v minulosti.",
            })

        if end_date < today:
            return render(request, "rentals/car_detail.html", {
                "car": car,
                "error_message": "Koniec prenájmu nemôže byť v minulosti.",
            })

        if end_date <= start_date:
            return render(request, "rentals/car_detail.html", {
                "car": car,
                "error_message": "Dátum konca prenájmu musí byť neskôr ako dátum začiatku.",
            })

        rental = Rental(user=request.user, car=car, start_date=start_date, end_date=end_date)
        rental.save()

        car.available = False
        car.save()

        return HttpResponseRedirect(reverse("rentals:car_details", args=(car.id,)))

    return render(request, "rentals/car_detail.html", {"car": car})




@login_required
def rental_details(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    rentals = Rental.objects.filter(car=car).order_by("-start_date")  
    
    if rentals.exists():
        last_rental = rentals.first()
    else:
        last_rental = None

    return render(request, "rentals/rental_details.html", {
        "car": car,
        "last_rental": last_rental,
    })

@login_required
def user_reservations(request):
    user_rentals = Rental.objects.filter(user=request.user).order_by("-start_date")

    return render(request, "rentals/user_reservations.html", {
        "user_rentals": user_rentals})


def register(request):
    message = " "
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        username = request.POST.get("username")
        if form.is_valid():
            user = form.save()
            login(request, user)
            message = "Registrácia bola úspešná! Vitajte, .'{username}'"
            return redirect("rentals:index")  
        else:
            message = "Registrácia zlyhala. Skontrolujte chyby nižšie."
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})



def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(f'User logged in: {user.username}')  
            return redirect("rentals:index")  
        else:
            print(f"Neplatné prihlasovacie údaje")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})



@login_required
def logout_view(request):
    logout(request)
    return redirect("rentals:login")



def delete_user(request):
    message = ""  
    if request.method == "POST":
        username = request.POST.get("username")
        if username: 
            try:
                user_to_delete = User.objects.get(username=username)
                user_to_delete.delete()
                message = f"Účet '{username}' bol úspešne odstránený."  
            except User.DoesNotExist:
                message = f"Používateľ s menom '{username}' neexistuje."  
        else:
            message = "Prosím zadajte používateľské meno."  

    return render(request, "accounts/delete_user.html", {"message": message})

@login_required
def cancel_reservation(request, car_id):
    rental = get_object_or_404(Rental, pk=car_id, user=request.user)

    if rental.end_date >= timezone.now().date():  
        car = rental.car
        rental.delete() 
        car.available = True  
        car.save()

    return HttpResponseRedirect(reverse('rentals:user_reservations'))



