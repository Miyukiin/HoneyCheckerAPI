from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class HoneyCheckerTable(models.Model):
    class Meta:
        verbose_name = "HoneyChecker"  # Singular name
        verbose_name_plural = "HoneyChecker"  # Correct plural name
        
    user_random_index = models.IntegerField(_("User Random Index"),unique=True, null=False, blank=False, primary_key=True)
    user_sugarword_index = models.IntegerField(_("User Sugarword Index"), null=True, blank=True)
    
    def __str__(self):
        return f"Honey Index for {self.user_random_index} is {self.user_sugarword_index}"