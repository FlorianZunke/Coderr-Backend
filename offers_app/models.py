from django.db import models
from django.conf import settings

class Offer(models.Model):
    """ 
    Model representing an offer made by a user.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.FileField(upload_to='offers/images/', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    """
    Model representing detailed information about an offer.
    """
    OFFER_TYPE = [
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    ]
    
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)   
    offer_type = models.CharField(max_length=50, choices=OFFER_TYPE)

    def __str__(self):
        return f"{self.offer.title} - {self.title}"