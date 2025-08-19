from django.db import models
from django.utils import timezone

# Create your models here.
class reg(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    age=models.IntegerField()
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100,null=True,blank=True)
    image=models.FileField(upload_to='image/')
    
class sreg(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    age=models.IntegerField()
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100,null=True,blank=True)
    image=models.FileField(upload_to='image/')  
    
class sproduct(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    image=models.FileField(upload_to='picture/',null=True,blank=True)
    quantity=models.IntegerField(null=True,blank=True)
    price=models.IntegerField(null=True,blank=True) 

class cart(models.Model):
    user = models.ForeignKey(reg,on_delete=models.CASCADE) 
    product = models.ForeignKey(sproduct,on_delete=models.CASCADE,null=True,blank=True)   
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(null=True,blank=True)
    
    
    def _str_(self):
       return f"Cart of {self.user.name}" 
        
class buy(models.Model):
    user = models.ForeignKey(reg,on_delete=models.CASCADE) 
    product = models.ForeignKey(sproduct,on_delete=models.CASCADE,null=True,blank=True)   
    address = models.TextField(max_length=100,null=True,blank=True)
    phone_no= models.IntegerField(null=True,blank=True)
    assigned = models.BooleanField(default=False) 
    ordered_at = models.DateTimeField(default=timezone.now) 
       
    
    
class DeliveryPerson(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=15)
    zone = models.CharField(max_length=50, null=True, blank=True)
    approved = models.BooleanField(default=False)
    image = models.FileField(upload_to='images/', null=True, blank=True)
    def __str__(self):
        return self.name  
    
class AssignedDelivery(models.Model):
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.CASCADE, related_name="assignments")
    order = models.ForeignKey(buy, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.order.id} → {self.delivery_person.name}"

class DeliveredRecord(models.Model):
    assignment = models.OneToOneField(AssignedDelivery, on_delete=models.CASCADE, related_name="delivery_record")
    marked_at = models.DateTimeField(auto_now_add=True)
    
class Feedbacks(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    rating = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name  
   