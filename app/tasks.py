from celery.task.schedules import crontab
from celery.decorators import periodic_task
import pickle
import requests
from bs4 import BeautifulSoup
from .models import Product, Limit
from django.core.mail import send_mail
import sys

xml_url = 'https://sollux.ideaerp.pl/sollux-xml'
property_list_file = 'data.txt'


class Product1:
    def __init__(self, index, name, code, category, count, price):
        self.index = index
        self.name = name
        self.code = code
        self.category = category
        self.count = count
        self.price = price


def get_product(page_url):
    resp = requests.get(page_url)
    output = []
    # print(resp.text)
    soup = BeautifulSoup(resp.text, 'xml')
    products = soup.findAll('Produkt')
    i = 0
    for product in products:
        try:
            index = product.Indeks.text
        except:
            index = 'wrong'
        try:
            name = product.Nazwa.text
        except:
            name = ''
        try:
            ean = product.Ean.text
        except:
            ean = ''
        try:
            category = product.Kategoria.text
        except:
            category = ''
        try:
            count = product.Stan_mag.text
        except:
            count = ''
        try:
            price = product.Cena_zakupu_netto.text
        except:
            price = ''

        obj = Product1(index, name, ean, category, count, price)
        output.append(obj)
    return output


@periodic_task(run_every=(crontab(minute='*/2')))
def main():
    data = get_product(xml_url)

    for item in data:
        print(type(item.name))

    with open(property_list_file, "wb+") as fp:
        pickle.dump(data, fp)

    with open(property_list_file, "rb+") as fp:
        result = pickle.load(fp)

    print(len(result))
    for item in result:
        obj = Product()
        obj.index = item.index
        obj.name = item.name
        obj.ean = item.code
        obj.category = item.category
        obj.count = int(float(item.count))
        obj.price = float(item.price)
        obj.save()

    limit = Limit.objects.first()
    print(limit)
    if limit:
        if len(result) < limit.min:
            content = limit.alert_content + "Limit is " + str(limit.min) + ', and number of product is ' + str(len(result)) + '.'
            to = [limit.admin_email, ]
            send_mail("Product Alert", content, 'benjamin.langeriaf7@gmail.com', to)


