# CREATE A FUNCTION THAT RETURNS A LIST LISTs that contain the meals and the food items in each meal
# [[meal,[food item, food item]],[meal,[food item, food item]], ]]


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
            password='Lawrencehardy1!',
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
            password='Lawrencehardy1!',
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
    

functionOutput = mealHistory('cole0hardy@gmail.com')           

for mealList in functionOutput :
    print(mealList[0])
    for foodItem in mealList[1]:
        print(f'\t{foodItem}')



