from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, CarImage, Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('home')


# ================= HOME =================
def home(request):
    cars = Car.objects.all()
    return render(request, "index.html", {"cars": cars})


# ================= CAR DETAIL =================
def car_detail(request, id):
    car = get_object_or_404(Car, id=id)
    images = CarImage.objects.filter(car=car)

    return render(request, "car_detail.html", {
        "car": car,
        "images": images
    })


# ================= LOGIN =================
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        print("USERNAME:", username)
        print("PASSWORD:", password)

        user = authenticate(request, username=username, password=password)

        print("USER:", user)

        if user is not None:
            login(request, user)

            profile = Profile.objects.get(user=user)

            if profile.role == "dealer":
                return redirect("dealer_dashboard")
            else:
                return redirect("home")

        else:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "login.html")

# ================= SIGNUP =================
def signup_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # 🔥 Prevent duplicate user
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,
            password=password
        )

        if role == "dealer":
            Profile.objects.create(user=user, role="dealer", approved=False)
        else:
            Profile.objects.create(user=user, role="customer", approved=True)

        return redirect("login")

    return render(request, "signup.html")


# ================= DEALER DASHBOARD =================
@login_required
def dealer_dashboard(request):

    profile = Profile.objects.get(user=request.user)

    # ❌ Block customers
    if profile.role != "dealer":
        return redirect("home")

    cars = Car.objects.filter(owner=request.user)

    if request.method == "POST":

        make = request.POST.get("make")
        model = request.POST.get("model")
        year = request.POST.get("year")
        owners = request.POST.get("owners")
        price = request.POST.get("price")
        mileage = request.POST.get("mileage")
        fuel = request.POST.get("fuel")
        transmission = request.POST.get("transmission")

        car = Car.objects.create(
            owner=request.user,
            make=make,
            model=model,
            year=year,
            owners=owners,
            price=price,
            mileage=mileage,
            fuel=fuel,
            transmission=transmission
        )

        # 🔥 Save images
        images = request.FILES.getlist("images")
        for img in images:
            CarImage.objects.create(car=car, image=img)

        return redirect("dealer_dashboard")

    return render(request, "dealer_dashboard.html", {
        "cars": cars
    })


# ================= DELETE CAR =================
@login_required
def delete_car(request, id):

    car = get_object_or_404(Car, id=id)
    profile = Profile.objects.get(user=request.user)

    # ✅ Only dealer & owner can delete
    if profile.role == "dealer" and car.owner == request.user:
        car.delete()

    return redirect("dealer_dashboard")

def about(request):
    return render(request, "about.html")
def contact(request):
    return render(request, "contact.html")
def privacy(request):
    return render(request, "privacy-policy.html")
def terms(request):
    return render(request, "terms.html")