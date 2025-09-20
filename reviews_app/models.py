from django.db import models



class Review(models.Model):
    reviewer = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='reviews_made')
    business_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.reviewer} for {self.business_user} - Rating: {self.rating}"
