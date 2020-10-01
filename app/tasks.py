from celery.task.schedules import crontab
from celery.decorators import periodic_task
import pickle
import requests
from bs4 import BeautifulSoup
from .models import Product, Limit
from django.core.mail import send_mail
from django.template.loader import render_to_string
import datetime
import pytz

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
    resp.encoding = resp.apparent_encoding
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


@periodic_task(run_every=(crontab(minute='*/60')))
def main(type=False):
    tz = pytz.timezone('Europe/Warsaw')
    warsaw_now = datetime.datetime.now(tz)
    print(warsaw_now)
    if not type:
        if not warsaw_now.hour == 6:
            return True

    products = Product.objects.filter(added_by_scrap=True)
    for item in products:
        item.delete()
    data = get_product(xml_url)

    with open(property_list_file, "wb+") as fp:
        pickle.dump(data, fp)

    with open(property_list_file, "rb+") as fp:
        result = pickle.load(fp)

    for item in result:
        obj = Product()
        obj.index = item.index
        obj.name = item.name
        obj.ean = item.code
        obj.category = item.category
        obj.count = int(float(item.count))
        obj.price = float(item.price)
        obj.added_by_scrap = True
        obj.save()
    check_product()
    return True


def check_product():
    limit = Limit.objects.first()
    products = Product.objects.filter(added_by_scrap=True, count__lt=limit.min)
    print(limit)

    if limit:
        if len(products):
            context = {
                'products': products,
                'header': limit.alert_content,
                'domain': limit.domain
            }
            content = render_to_string('email.html', context)
            to = [limit.admin_email, ]
            send_mail(limit.alert_subject, '', 'tg.code.sp.zo.o@gmail.com', to, html_message=content)
