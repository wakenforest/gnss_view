from django.db import models


# Create your models here.
class Index(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "首页"

    def __str__(self):
        return self.title