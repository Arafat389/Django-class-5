from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# One-to-One relationship
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # on_delete=models.CASCADE means parent data delete korle child data auto delete hobe.
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True,blank=True)
    location = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.user.username

# One-to-Many relationship
class ExpenseCategory(models.Model):
    name =models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Expense(models.Model):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.amount} for {self.category.name}"
    


    # Many-to-Many relationship
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author)
    year = models.IntegerField()
    isbn = models.CharField(max_length=13)
    
    def __str__(self):
        return self.title