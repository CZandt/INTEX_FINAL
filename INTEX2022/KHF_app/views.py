from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import recommendation, user, food_item, food_item_in_meal, meal
import requests
import json
import cgi

# Create your views here.

def sqlDayNutrientSum(email, nutrient, day):
    import psycopg2
    from psycopg2 import Error
    record = 0
    rawQuery = f"SELECT SUM(quantity * {nutrient}) AS sumPH "
    rawQuery += f"FROM \"KHF_app_user\" AS Cuser "
    rawQuery += f"INNER JOIN \"KHF_app_meal\" AS meal ON meal.user_id = Cuser.id "
    rawQuery += f"INNER JOIN \"KHF_app_food_item_in_meal\" AS fiim ON fiim.meal_id = meal.id "
    rawQuery += f"INNER JOIN \"KHF_app_food_item\" AS FI ON FI.id = fiim.food_name_id "
    rawQuery += f"WHERE Cuser.email = \'{email}\' AND date = \'{day}\'"
    try:
        connection = psycopg2.connect(user='postgres',
        password='PASSWORD',
        host='127.0.0.1',
        database='KHFtracker')

        cursor = connection.cursor()

        cursor.execute(rawQuery)

        record = cursor.fetchall()

    except (Exception, Error) as error:
        print('Error while connecting to DB', error)
    finally:
        if(connection):
            cursor.close()
            connection.close()

    return record

def sqlDayWaterSum(email, day):
    import psycopg2
    from psycopg2 import Error

    rawQuery = f"SELECT SUM(quantity) "
    rawQuery += f"FROM \"KHF_app_user\" AS Cuser "
    rawQuery += f"INNER JOIN \"KHF_app_meal\" AS meal ON meal.user_id = Cuser.id "
    rawQuery += f"INNER JOIN \"KHF_app_food_item_in_meal\" AS fiim ON fiim.meal_id = meal.id "
    rawQuery += f"INNER JOIN \"KHF_app_food_item\" AS FI ON FI.id = fiim.food_name_id "
    rawQuery += f"WHERE Cuser.email = \'{email}\' AND date = \'{day}\' AND meal_type = \'Water\' AND food_name = \'Water\' "
    try:
        connection = psycopg2.connect(user='postgres',
        password='PASSWORD',
        host='127.0.0.1',
        database='KHFtracker')

        cursor = connection.cursor()

        cursor.execute(rawQuery)

        record = cursor.fetchall()

    except (Exception, Error) as error:
        print('Error while connecting to DB', error)
    finally:
        if(connection):
            cursor.close()
            connection.close()

    return record

def sqlUserRecs(email):

    import psycopg2
    from psycopg2 import Error
    record = 0
    rawQuery = f'SELECT sodium, protein, water, potassium, phosphates '
    rawQuery += f'FROM \"KHF_app_recommendation\" AS Rec '
    rawQuery += f'INNER JOIN \"KHF_app_user\" AS Cuser ON Cuser.comorbidity_id = Rec.id '
    rawQuery += f'WHERE Cuser.email = \'{email}\''
    try:
        connection = psycopg2.connect(user='postgres',
        password='PASSWORD',
        host='127.0.0.1',
        database='KHFtracker')

        cursor = connection.cursor()

        cursor.execute(rawQuery)

        record = cursor.fetchall()

    except (Exception, Error) as error:
        print('Error while connecting to DB', error)
    finally:
        if(connection):
            cursor.close()
            connection.close()

    return record

def getNutrients(foodSelection) :
    import requests
    import json
    r = requests.get(f'https://api.nal.usda.gov/fdc/v1/food/{foodSelection}?nutrients=203&nutrients=204&nutrients=205&api_key=qYgvm24Uuid52ZmJ6cM3wfhgbeWH33cYhssaUW5O')
    returnDict = json.loads(r.text)
    nutrients = ['protein', 'sodium', 'potassium', 'phosphorus']
    returnList = ['name','unit',0,0,0,0]
    returnList[0] = returnDict['description']
    returnList[1] = returnDict['servingSizeUnit']
    for nutrient in returnDict['labelNutrients']:
        if nutrient == nutrients[0]:
            returnList[2] = returnDict['labelNutrients']['protein']['value']
        if nutrient == nutrients[1]:
            returnList[3] = returnDict['labelNutrients']['sodium']['value']
        if nutrient == nutrients[2]:
            returnList[4] = returnDict['labelNutrients']['potassium']['value']
        if nutrient == nutrients[3]:
            returnList[5] = returnDict['labelNutrients']['phosphorus']['value']
    return returnList

def getDate():
    from datetime import date
    today = date.today()

    currentDate = today.strftime('%Y-%m-%d')

    return currentDate

#Generates a users meal history in a list of list of lists
def mealHistory(email):
    def userMeals(email):
        import psycopg2
        from psycopg2 import Error
        record = 0
        rawQuery = f"SELECT date, meal_type, meal.id "
        rawQuery += f"FROM \"KHF_app_meal\" AS meal "
        rawQuery += f"INNER JOIN \"KHF_app_user\" AS Cuser ON meal.user_id = Cuser.id "
        rawQuery += f"WHERE Cuser.email = \'{email}\' "
        try:
            connection = psycopg2.connect(user='postgres',
            password='PASSWORD',
            host='127.0.0.1',
            database='KHFtracker')

            cursor = connection.cursor()

            cursor.execute(rawQuery)

            record = cursor.fetchall()

        except (Exception, Error) as error:
            print('Error while connecting to DB', error)
        finally:
            if(connection):
                cursor.close()
                connection.close()

        return record

    #gets the items that are in each meal for the specified user
    def userItemsInMeals(email):
        import psycopg2
        from psycopg2 import Error
        record = 0
        rawQuery = f"SELECT food_name, quantity, measurement_unit, meal_id "
        rawQuery += f"FROM \"KHF_app_food_item_in_meal\" AS fiim "
        rawQuery += f"INNER JOIN \"KHF_app_food_item\" AS FI ON FI.id = fiim.food_name_id "
        rawQuery += f"WHERE meal_id IN (SELECT meal.id "
        rawQuery += f"FROM \"KHF_app_meal\" AS meal "
        rawQuery += f"INNER JOIN \"KHF_app_user\" AS Cuser ON Cuser.id = meal.user_id "
        rawQuery += f"WHERE Cuser.email = \'{email}\') "
        try:
            connection = psycopg2.connect(user='postgres',
            password='PASSWORD',
            host='127.0.0.1',
            database='KHFtracker')

            cursor = connection.cursor()

            cursor.execute(rawQuery)

            record = cursor.fetchall()

        except (Exception, Error) as error:
            print('Error while connecting to DB', error)
        finally:
            if(connection):
                cursor.close()
                connection.close()

        return record


    mealReturn = userMeals(email)

    itemsInMealReturn = userItemsInMeals(email)

    from datetime import date
    outputList = []
    for mealItem in mealReturn:

        mealDate = mealItem[0].strftime('%Y-%m-%d') #grabs teh time and converts it to a string
        mealName = f'{mealItem[1]} - {mealDate}' #formats the naming convention for the mealItem
        mealID = mealItem[2] #grabs the mealID
        mealList = [mealName]
        foodList = []

        for foodItem in itemsInMealReturn:
            if foodItem[3] == mealID: #IF THE ID's of the meal and the food item in meal are equal
                foodEntry = f'{foodItem[0]} {foodItem[1]} {foodItem[2]}'
                foodList.append(foodEntry)

        mealList.append(foodList)

        outputList.append(mealList)
    
    return outputList

def mealHistoryCurrentDay(email, date):
    def userMeals(email, date):
        import psycopg2
        from psycopg2 import Error
        record = 0
        rawQuery = f"SELECT date, meal_type, meal.id "
        rawQuery += f"FROM \"KHF_app_meal\" AS meal "
        rawQuery += f"INNER JOIN \"KHF_app_user\" AS Cuser ON meal.user_id = Cuser.id "
        rawQuery += f"WHERE Cuser.email = \'{email}\' AND date = \'{date}\' "
        try:
            connection = psycopg2.connect(user='postgres',
            password='PASSWORD',
            host='127.0.0.1',
            database='KHFtracker')

            cursor = connection.cursor()

            cursor.execute(rawQuery)

            record = cursor.fetchall()

        except (Exception, Error) as error:
            print('Error while connecting to DB', error)
        finally:
            if(connection):
                cursor.close()
                connection.close()

        return record

    #gets the items that are in each meal for the specified user
    def userItemsInMeals(email, date):
        import psycopg2
        from psycopg2 import Error
        record = 0
        rawQuery = f"SELECT food_name, quantity, measurement_unit, meal_id "
        rawQuery += f"FROM \"KHF_app_food_item_in_meal\" AS fiim "
        rawQuery += f"INNER JOIN \"KHF_app_food_item\" AS FI ON FI.id = fiim.food_name_id "
        rawQuery += f"WHERE meal_id IN (SELECT meal.id "
        rawQuery += f"FROM \"KHF_app_meal\" AS meal "
        rawQuery += f"INNER JOIN \"KHF_app_user\" AS Cuser ON Cuser.id = meal.user_id "
        rawQuery += f"WHERE Cuser.email = \'{email}\' AND date = \'{date}\' ) "
        try:
            connection = psycopg2.connect(user='postgres',
            password='PASSWORD',
            host='127.0.0.1',
            database='KHFtracker')

            cursor = connection.cursor()

            cursor.execute(rawQuery)

            record = cursor.fetchall()

        except (Exception, Error) as error:
            print('Error while connecting to DB', error)
        finally:
            if(connection):
                cursor.close()
                connection.close()

        return record


    mealReturn = userMeals(email, date)

    itemsInMealReturn = userItemsInMeals(email, date)

    from datetime import date
    outputList = []
    for mealItem in mealReturn:

        mealDate = mealItem[0].strftime('%Y-%m-%d') #grabs teh time and converts it to a string
        mealName = f'{mealItem[1]} - {mealDate}' #formats the naming convention for the mealItem
        mealID = mealItem[2] #grabs the mealID
        mealList = [mealName]
        foodList = []

        for foodItem in itemsInMealReturn:
            if foodItem[3] == mealID: #IF THE ID's of the meal and the food item in meal are equal
                foodEntry = f'{foodItem[0]} {foodItem[1]} {foodItem[2]}'
                foodList.append(foodEntry)

        mealList.append(foodList)

        outputList.append(mealList)
    
    return outputList
    
def indexPageView(request):

    return render(request, 'index.html')

@login_required
def fillAccount(request):
    recommendations = recommendation.objects.all()

    #get email of registered user
    currEmail = request.user.email 
    #check if registered email is already in the db
    data = user.objects.filter(email=currEmail)

    if data.count() > 0:
        #if the email IS in the db, render the account page
        context = {
            "auth": request.user,
            "currUser" : data
        }
        return render(request, 'dashboard.html', context)
    else:
        context = {
            'data': recommendations,
            'user': request.user,
        }
        return render(request, 'account.html', context)

@login_required
def viewAccount(request):
    currEmail = request.user.email 
    #check if registered email is already in the db
    data = user.objects.filter(email=currEmail)
    context = {
        'currUser': data
    }
    
    return render(request, 'viewAccount.html', context)
@login_required
def viewDashboard(request):
    currEmail = request.user.email 
    
    #check if registered email is already in the db
    data = user.objects.filter(email=currEmail)

    today = str(getDate())

    #today = '2022-11-30'
    
    
    # THE QUERIES FOR THE SUMS OF THE DATA FOR THE PROGRESS BARS ON BOTTOM
    potassiumDaySum = sqlDayNutrientSum(currEmail, 'potassium', today)[0][0]
    proteinDaySum = sqlDayNutrientSum(currEmail, 'protein', today)[0][0]
    phosphorusDaySum = sqlDayNutrientSum(currEmail, 'phosphorus', today)[0][0]
    sodiumDaySum = sqlDayNutrientSum(currEmail, 'sodium', today)[0][0]
    userReccomendation = sqlUserRecs(currEmail)
    waterDaySum = sqlDayWaterSum(currEmail, today)[0][0]
    userMealHistory = mealHistory(currEmail)
    mealsToday = mealHistoryCurrentDay(currEmail,today)

    if potassiumDaySum == None:
        potassiumDaySum = 0

    if proteinDaySum == None:
        proteinDaySum = 0
    
    if phosphorusDaySum == None:
        phosphorusDaySum = 0

    if sodiumDaySum == None:
        sodiumDaySum = 0
    
    if waterDaySum == None:
        waterDaySum = 0

    
    #The Queries for the reccomendations for the progress bars
    sodiumRec = userReccomendation[0][0]
    proteinRec = userReccomendation[0][1]
    waterRec = userReccomendation[0][2]
    potassiumRec = userReccomendation[0][3]
    phosphatesRec = userReccomendation[0][4]

    #Math to get the values for the circle chart on the dashboard
    sodiumDone = (sodiumDaySum / sodiumRec) * 100
    sodiumLeft = 100 - sodiumDone

    proteinDone = (proteinDaySum / proteinRec) * 100
    proteinLeft = 100 - proteinDone

    waterDone = (waterDaySum / waterRec) * 100 
    waterLeft = 100 - waterDone

    potassiumDone = (potassiumDaySum / potassiumRec) * 100
    potassiumLeft = 100 - potassiumDone

    phosphatesDone = (phosphorusDaySum / phosphatesRec) * 100
    phosphatesLeft = 100 - phosphatesDone

    sodiumExceed = 1
    proteinExceed = 1
    waterExceed = 1
    potassiumExceed = 1
    phosphatesExceed = 1

    if sodiumLeft <= 0:
        sodiumExceed = 0
        sodiumLeft = 0

    if proteinLeft <= 0:
        proteinExceed = 0
        proteinLeft = 0

    if waterLeft <= 0:
        waterExceed = 0
        waterLeft = 0

    if potassiumLeft <= 0:
        potassiumExceed = 0
        potassiumLeft = 0

    if phosphatesLeft <= 0:
        phosphatesExceed = 0
        phosphatesLeft = 0


    context = {
        'currUser': data,
        'proteinSum': str(proteinDaySum),
        'potassiumSum': str(potassiumDaySum),
        'phosphorusSum': str(phosphorusDaySum),
        'sodiumSum': str(sodiumDaySum),
        'waterSum' : str(waterDaySum),
        'sodiumRec' : str(sodiumRec),
        'proteinRec' : str(proteinRec),
        'waterRec' : str(waterRec),
        'potassiumRec' : str(potassiumRec),
        'phosphatesRec' : str(phosphatesRec),
        'sodiumDone' : sodiumDone,
        'sodiumLeft' : sodiumLeft,
        'proteinDone' : proteinDone,
        'proteinLeft' : proteinLeft,
        'waterDone' : waterDone,
        'waterLeft' : waterLeft,
        'potassiumDone' : potassiumDone,
        'potassiumLeft' : potassiumLeft,
        'phosphatesDone' : phosphatesDone,
        'phosphatesLeft' : phosphatesLeft,
        'mealHistory' : userMealHistory,
        'mealToday' : mealsToday,
        'sodiumExceed' : sodiumExceed,
        'proteinExceed' : proteinExceed,
        'waterExceed' : waterExceed,
        'potassiumExceed' : potassiumExceed,
        'phosphatesExceed' : phosphatesExceed,
    }
    return render(request, 'dashboard.html', context)

@login_required
def logout(request):
    django_logout(request)
    domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY
    return_to = 'http://127.0.0.1:8000'
    return redirect(f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}')

def storeUserPageView(request):
    if request.method == 'POST':

        new_user = user()

        #stores the data from each field into the specified spot in the database

        new_user.first_name = request.POST.get('first_name')

        new_user.last_name = request.POST.get('last_name')

        new_user.sex = request.POST.get('sex')

        new_user.height = request.POST.get('height')

        new_user.age = request.POST.get('age')

        new_user.weight = request.POST.get('weight')

        new_user.email = request.user.email

        new_comorbidity = recommendation.objects.get(comorbidity = request.POST.get('comorbidity'))

        new_user.comorbidity = new_comorbidity

        new_user.save()

    data = user.objects.all()

    context = {
        'users' : data
    }


    return render(request, 'dashboard.html', context)


# SEARCH FUNCTIONALITY
def searchView(request):
    if request.method == 'POST':
        parameter = request.POST.get('foodItem')
        searchResult = getFoodList(parameter)

    context = {
        'search' : searchResult
    }

    return context

def getFoodList(foodSelection) :
    r = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search?query=' + foodSelection + '&dataType=&pageSize=6&sortBy=dataType.keyword&sortOrder=asc&api_key=qYgvm24Uuid52ZmJ6cM3wfhgbeWH33cYhssaUW5O')
    y = json.loads(r.text)

    brand = []
    for x in y['foods'] :
        
        des = x['description']
        ss = x['servingSize']
        unit = x['servingSizeUnit']
        bra = x['brandName']

        brand.append([des, bra, ss, unit])
    
    return brand
#END OF SEARCH FUNCTIONALITY

def storeMealView(request):
    if request.method == 'POST':
        new_meal = meal()

        new_meal.date = request.POST.get('date')

        new_meal.notes = request.POST.get('notes')

        new_meal.meal_type = request.POST.get('mealType')

        userid = user.objects.get(email = request.user.email)

        new_user = user.objects.get(id = userid.id)

        new_meal.user = new_user

        new_meal.save()

        selected_Meals = request.POST.getlist('selectedFoods')

        for i in selected_Meals:

            mealAttributes = getNutrients(i)
            new_food = food_item()
            new_food.food_name = mealAttributes[0]
            new_food.measurement_unit = mealAttributes[1]
            new_food.protein = mealAttributes[2]
            new_food.sodium = mealAttributes[3]
            new_food.potassium = mealAttributes[4]
            new_food.phosphorus = mealAttributes[5]
            new_food.save()

            new_fiin = food_item_in_meal()

            new_food_fiin = food_item.objects.get(food_name = new_food.food_name)
            new_fiin.food_name = new_food_fiin #new_food

            new_meal_fiin = meal.objects.get(id = new_meal.id)
            new_fiin.meal = new_meal_fiin

            new_fiin.quantity = 5

            new_fiin.save()

            
        context = {
            'meals': selected_Meals
        }
        
    return render(request, 'dashboard.html', context)