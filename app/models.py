from django.db import models



class Product(models.Model):
    index = models.CharField(max_length=250)
    name = models.CharField(max_length=500, verbose_name='Nazwa')
    ean = models.CharField(max_length=100, verbose_name='Ean')
    category = models.CharField(max_length=100, verbose_name='Kategoria')
    count = models.IntegerField(verbose_name='Stan magazynowy (stan_mag)') #if max save max scraping
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Cena zakupu netto')

    class Meta:
        verbose_name = 'Produkty'
        verbose_name_plural = 'Produkty'

    def __str__(self):
        return self.name



class Limit(models.Model):
    max = models.IntegerField()
    min = models.IntegerField()

    class Meta:
        verbose_name = 'Limity wysyłania wiadomości'
        verbose_name_plural = 'Limity wysyłania wiadomości'