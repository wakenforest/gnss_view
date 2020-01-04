from django.db import models

# Create your models here.
class AntiSpf(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "antispf显示"

    def __str__(self):
        return self.title
