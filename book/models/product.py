from django.db import models


class Product(models.Model):
    """Разновидность продукта питания"""
    classname = 'product'

    name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return '{} ----- {}'.format(self.id, self.name)
