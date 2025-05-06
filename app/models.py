from django.db import models


# Create your models here.
 

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_no = models.CharField(max_length=15)
    description = models.TextField()
    def __str__(self):
        return self.name

class Enrollment(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField()
    gender = models.CharField(max_length=20)
    phone_no = models.CharField(max_length=12)
    dob = models.CharField(max_length=50)
    membership_plan = models.CharField(max_length=200)
    trainer = models.CharField(max_length=50)
    address = models.TextField()
    enroll_date = models.DateField(auto_now_add=True,blank=True)
    end_date = models.DateField(blank=True, null=True)
    payment_status = models.CharField(max_length=50, blank=True, null=True)
    payment_amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.fullname
    

class Trainer(models.Model):
    name = models.CharField(max_length=35)
    phone_no = models.CharField(max_length=12)
    gender = models.CharField(max_length=25)
    salary = models.IntegerField()
    join_date = models.DateField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return self.name
    
class MembershipPlan(models.Model):
    plan = models.CharField(max_length=50)
    price = models.IntegerField()
    duration=models.CharField(max_length=50)
    offer = models.IntegerField() 
    def __str__(self):
        return self.plan
    
class Feedback(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    contact=models.CharField(max_length=12)
    feedback = models.CharField(max_length=150)
    def __str__(self):
        return self.name
    
