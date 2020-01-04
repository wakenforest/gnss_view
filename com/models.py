from django.db import models

# Create your models here.
class COM(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "串口通信"

    def __str__(self):
        return self.title