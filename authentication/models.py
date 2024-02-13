from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    id = models.CharField(max_length=60, primary_key=True)
    type = models.CharField(max_length=20, choices=[('personal','personal'),('joint','joint'),
                                                    ('organization', 'organization'), ('visa', 'visa'),
                                                    ('retirement', 'retirement')], default="personal")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)
    country_code = models.CharField(max_length=5)
    phone = models.CharField(max_length=17)
    country = models.CharField(max_length=40)
    verified = models.BooleanField(default=False)
    enable_verification = models.BooleanField(default=False)
    verification_plus = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)
    key = models.CharField(max_length=70, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name}  {self.user.last_name}"

