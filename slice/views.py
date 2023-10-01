from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib.auth.models import User
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
import requests
import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import random
import ast
import time
from datetime import date

def home(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except ObjectDoesNotExist:
            profile = 1
    else:
        profile = None
    context = {
        'profile': profile,
    }

    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            profile = Profile(user=user)
            profile.save()

            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('home')

def loginUser(request):
    if request.user.is_authenticated:
       return redirect('home')
   

    if request.method == 'POST':

        username = request.POST.get('username').lower()
        password = request.POST.get('password')


        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)          
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')


    return render(request, 'login.html')


def profile(request):
    profile = request.user.profile

    cuisine = [
    'Seafood', 'Mexican','Chinese','Italian','Indian',
    'Japanese','French','Thai', 'Mediterranean','American',
    ]
    
    interests = ['Indoor Entertainment', 'Outdoor Activities', 'Cultural Attractions',
                  'Nightlife', 'Shopping', 'Sports',
                  'Relaxation', 'Fitness']


    context = {
        'profile': profile,
        'cuisine':cuisine,
        'interests': interests
    }

    if request.method == 'POST':
        profile.name = request.POST.get('name')
        profile.email = request.POST.get('email')
        profile.birthday = request.POST.get('birthday')
        profile.food_pref = request.POST.getlist('food')
        profile.interests = request.POST.getlist('selected_interests')
        profile.save()

    return render(request, 'profile.html', context)


def plan(request):
    profile = request.user.profile
    context = {'profile': profile}
    if request.method == 'POST':
        profile.date_of_plan = request.POST.get('dateofplan')
        profile.start_time = request.POST.get('start-time')
        profile.end_time = request.POST.get('end-time')
        profile.save()
        return redirect('plansub1')
    return render(request, 'plan.html', context)

def plansub1(request):
    profile = request.user.profile
    context = {
        'profile': profile,
        }
    if request.method == 'POST':
        profile.budget = request.POST.get('budget')
        if request.POST.get("hunger") == 'on':
            profile.hunger_level = None
        else:
            profile.hunger_level = request.POST.get("hunger")
        profile.save()
        return redirect('plansub2')
    return render(request, 'plansub1.html', context)

def plansub2(request):
    profile = request.user.profile
    context = {
        'profile': profile,
        }
    if request.method == 'POST':
        profile.boroughs = request.POST.getlist('borough')
        profile.save()
        return redirect('plansub3')
    return render(request, 'plansub2.html', context)


def plansub3(request):
    if request.method == 'POST':
        return redirect('plansub3')
    api_key = 'nziQ8bipUOTjFJ1XR00G9jibOvfVNn69IQa5vwooyiU2L8EhH1zYMMC1LEuCwZ1ajY9obnCmh4h7Tw-oN8hGBnpIvjqCrvFUapAdfpK-A7Wm83SkThjw7rLWHXP_ZHYx'
    profile = request.user.profile
    api_url = 'https://api.yelp.com/v3/businesses/search'

    food_preferences = {
    "Light Snack": ["ice cream parlors", "smoothie bars", "Acai Bowls"],
    "Dessert": ["bakery", "creperies", "Bubble Tea", "Churros", "frozen yogurt shops", "ice cream", "gelato", "Donuts", 
                ],
    "Full Dining": ["restaurants", "food trucks", "fine dining", "food festivals"
    ],
}

    categories = {
    "Indoor Entertainment": [
        "bowling", "arcade games", "mini golf", "escape rooms", "amusement parks", "Paintball", "Trampoline Parks"
    ],
    "Outdoor Activities": [
        "hiking", "biking", "rock climbing", "archery", "park", 'Public Plazas',
    ],
    "Cultural Attractions": [
        "museums", "art galleries", "historical sites", "botanical gardens",
        "zoos", "aquariums"
    ],
    "Shopping": [
        "malls", "boutique shops", "flea markets", "antique shops"
    ],
    "Sports": [
        "stadiums", "sports arenas", "golf courses", "tennis courts"
    ],
    "Dining": [
        "restaurants", "food trucks", "fine dining", "cafes", "food festivals"
    ],
    "Relaxation": [
        "spas", "hot springs", "yoga studios", "massage centers", "meditation centers"
    ],
    "Fitness": [
        "Aerial Fitness", "crossfit", "pilates", "cycling classes", "Dance Studios", "Swimming Lessons"
    ],
    
}

    nightlife = [ "bars", "nightclubs", "live music venues", "comedy clubs", "karaoke"]
   
    def time_of_day(time):
        current_hour = time.hour
        
        if 6 <= current_hour < 12:
            return "Morning"
        elif 12 <= current_hour < 18:
            return "Afternoon"
        elif 18 <= current_hour < 21:
            return "Evening"
        else:
            return "Night"
        
    age = date.today().year - profile.birthday.year - ((date.today().month, date.today().day) < (profile.birthday.month, profile.birthday.day))
        
    boroughs = {
        'Manhattan': ['40.786742', '-73.956218', 10523],
        'Brooklyn': ['40.668592', '-73.923918', 11798],
        'Bronx': ['40.922847', '-73.852036', 9323],
        'Queens': ['40.737800', '-73.779805', 12494],
        'Staten Island': ['40.575159', '-74.165166', 10832],
        'All': ['40.721188', '-73.937057', 25571.82]
    }
    profile_boroughs = ast.literal_eval(profile.boroughs)

    interests = ast.literal_eval(profile.interests)
    

    hours =  (24 - profile.start_time.hour) - (24 - profile.end_time.hour)
    if hours < 0:
        hours += 24
    minutes = profile.end_time.minute - profile.start_time.minute

    if minutes < 60:
        minutes = minutes/100
    else:
        minutes = ((minutes - 60)/100) + 1 

    total_time = hours + minutes

    type = 0
    location = ""
    radius = 0  

    if len(profile_boroughs) > 1:
        location = boroughs['All'][0] + ',' + boroughs['All'][1]
        radius = boroughs['All'][2]
    else:
        location = boroughs[profile_boroughs[0]][0] + "," + boroughs[profile_boroughs[0]][1]
        radius = boroughs[profile_boroughs[0]][2]

    plan = []
    budget = profile.budget

    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    nightlife_count = 0
    print('total_time', total_time, 'budget', budget )
    while total_time >= 0 and budget >= 0:
        print('total_time', total_time, 'budget', budget )
        if profile.hunger_level != None:
            if profile.hunger_level == "Full Dining":
                query = random.choice(ast.literal_eval(profile.food_pref))
                params = {
                        'term': query,
                        'location': location, 
                        'radius': radius,  
                        'type': 'restaurant'
                }
                
            else:
                query = random.choice(food_preferences[profile.hunger_level])
                params = {
                    'term': query,  
                    'location': location, 
                    'radius': radius, 
                }
            response = requests.get(api_url, params=params, headers=headers)
            data = response.json()
            businesses = data.get('businesses', [])
            place = random.choice(businesses)

            name = place.get('name', '')
            if name not in plan:
                profile.hunger_level = None                
                total_time -= 2.1
                price_level = place.get('price', '')  
                if price_level == '':
                    price_level = '$'
                address =  place.get('location', {}).get('address1', '')
                img = place.get('image_url', '')
                alias = place.get('alias', '')
                plan.append([name, address, price_level, img, alias])

                if price_level == '$':
                    budget -= 10
                elif price_level == '$$':
                    budget -= 25
                elif price_level == '$$$':
                    budget -= 50
                elif price_level == '$$$$':
                    budget -= 80


        elif time_of_day(profile.end_time) == 'Night' and age >= 21 and 'Nightlife' in interests and nightlife_count < 1:
            if "LGBT spaces" in interests:
                query = "Gay bar"
            else:
                query = random.choice(nightlife)
                
            params = {
                    'term': query,  
                    'location': location, 
                    'radius': radius, 
                }
            response = requests.get(api_url, params=params, headers=headers)
            data = response.json()
            businesses = data.get('businesses', [])
            place = random.choice(businesses)

            name = place.get('name', '')
            if name not in plan:
                total_time -= 2.1
                nightlife_count += 1
                price_level = place.get('price', '')  
                if price_level == '':
                    price_level = '$'
                address =  place.get('location', {}).get('address1', '')
                img = place.get('image_url', '')
                alias = place.get('alias', '')
                plan.append([name, address, price_level, img, alias])

                if price_level == '$':
                    budget -= 10
                elif price_level == '$$':
                    budget -= 25
                elif price_level == '$$$':
                    budget -= 50
                elif price_level == '$$$$':
                    budget -= 80

        
        else:
            q = random.choice(interests)
            while q not in categories:
                q = random.choice(interests)
            print('THIS IS THE OPTION: ', q)
            query = random.choice(categories[q])
            print('THIS IS THE INTEREST: ', query)
            
            params = {
                'term': query,  
                'location': location, 
                'radius': radius, 
            }
            
        
            response = requests.get(api_url, params=params, headers=headers)
            data = response.json()
            businesses = data.get('businesses', [])
            place = random.choice(businesses)
            name = place.get('name', '')
            city = place.get('location', {}).get('display_address', '')
            if name not in plan:
                total_time -= 2.1
                price_level = place.get('price', '') 
                if price_level == '':
                    price_level = '$'
                address =  place.get('location', {}).get('address1', '')
                img = place.get('image_url', '')
                alias = place.get('alias', '')
                plan.append([name, address, price_level, img, alias])
                

                if price_level == '$' or price_level == None:
                    budget -= 10
                elif price_level == '$$':
                    budget -= 25
                elif price_level == '$$$':
                    budget -= 50
                elif price_level == '$$$$':
                    budget -= 80

  

    profile = request.user.profile
    context = {
        'profile': profile,
        'plan': plan,
        'budget': budget
    }
    return render(request, 'plansub3.html', context)
