from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class recommendation(models.Model):
    comorbidity = models.CharField(max_length=50)
    sodium = models.FloatField()
    protein = models.FloatField()
    water = models.FloatField()
    potassium = models.FloatField()
    phosphates = models.FloatField()

    def __str__(self):
        return(f'{self.comorbidity}')

class registeredUser(AbstractUser):
    pass
class user(models.Model):
    SEX = (
        ('Male', 'Male'),
        ('Female','Female'),
        ('Other','Other'),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    sex = models.CharField(max_length=6, choices=SEX)
    height = models.IntegerField()
    age = models.IntegerField()
    weight = models.FloatField()
    email = models.EmailField()
    comorbidity = models.ForeignKey(recommendation, on_delete=models.DO_NOTHING)

    def __str__(self):
        return(self.full_name)
    
    @property
    def full_name(self):
        return(f'{self.first_name} {self.last_name}')
    
class meal(models.Model):
    class meal_type_choice(models.IntegerChoices):
        Breakfast = 1, 'Breakfast'
        Lunch = 2, 'Lunch'
        Dinner = 3, 'Dinner'
        Snack = 4, 'Snack'
        Water = 5, 'Water'
    MEALCHOICE = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
        ('Water','Water'),
    )
    date = models.DateField()
    notes = models.CharField(max_length=1000) # 1000 character limit
    meal_type = models.CharField(max_length=9, choices=MEALCHOICE)
    user = models.ForeignKey(user, on_delete=models.DO_NOTHING)

    def __str__(self):
        return(f'{self.user} {self.date} {self.meal_type}')

class food_item(models.Model):
    food_name = models.CharField(max_length=50)
    measurement_unit = models.CharField(max_length=50)
    protein = models.FloatField()
    sodium = models.FloatField()
    potassium = models.FloatField()
    phosphorus = models.FloatField()
    meals = models.ManyToManyField(meal, blank=True, through='food_item_in_meal') 
    
    def __str__(self):
        return(self.food_name)


class food_item_in_meal(models.Model):
    food_name = models.ForeignKey(food_item, on_delete=models.CASCADE)
    meal = models.ForeignKey(meal, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return(f'{self.food_name} in {self.meal}')

