from django.db import models


class SaleProduct(models.Model):

    link = models.URLField(primary_key=True, max_length=200)
    name = models.CharField(max_length=80)
    price = models.CharField(max_length=8)
    price_on_sale = models.CharField(max_length=8)

    def __str__(self):
        return f"LINK: {self.link}  \nNAME: {self.name}  \nPRICE: {self.price}  \nPRICE ON SALE: {self.price_on_sale}\n"
