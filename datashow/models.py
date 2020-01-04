from django.db import models

# Create your models here.
class DataShow(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "数据显示"

    def __str__(self):
        return self.title
