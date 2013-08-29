from django.db import models

class List(models.Model):
    pass

class Item(models.Model):
    text = models.TextField()
    list = models.ForeignKey(List)

    class Meta:
        unique_together = ('list', 'text')


    def __str__(self):
        return self.text


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

