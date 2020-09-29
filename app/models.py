from django.db import models


class Product(models.Model):
    index = models.CharField(max_length=250)
    name = models.CharField(max_length=500, verbose_name='Nazwa')
    ean = models.CharField(max_length=100, verbose_name='Ean')
    category = models.CharField(max_length=100, verbose_name='Kategoria')
    count = models.IntegerField(verbose_name='Stan magazynowy (stan_mag)') #if max save max scraping
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Cena zakupu netto')
    added_by_scrap = models.BooleanField(null=True, default=False, verbose_name='Czy produkt dodany za pomocą automatycznego pobierania? (USTAWIC NA "NO" DLA PRODUKTÓW Z ADMINA)')

    class Meta:
        verbose_name = 'Produkty'
        verbose_name_plural = 'Produkty'

    def __str__(self):
        return self.name


class Limit(models.Model):
    max = models.IntegerField()
    min = models.IntegerField()
    admin_email = models.EmailField(max_length=30, default='')
    alert_content = models.CharField(max_length=255, default='')
    alert_subject = models.CharField(max_length=50, default='')
    domain = models.CharField(max_length=30, default='')


    class Meta:
        verbose_name = 'Limity wysyłania wiadomości'
        verbose_name_plural = 'Limity wysyłania wiadomości'