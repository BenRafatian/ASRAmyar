import random
import json
import requests
from bs4 import BeautifulSoup
import urllib
import os


CATEGORY_CHOICES = list(range(1, 10))
current_path = os.path.dirname(os.path.realpath(__file__))
DATA = []


def product_generator(category, pk):
    details = product_links(category)
    products = []
    counter = 0
    for detail in details:
        counter += 1
        data = {}
        fields = {}

        data['model'] = "shop.product"
        fields['category'] = pk
        fields['name'] = detail['name']  # TODO: add name generator
        fields['slug'] = slugify(fields['name'])
        fields['image'] = detail['image']
        fields['description'] = detail['desc']
        fields['price'] = random.randint(1, 100)
        fields['available'] = is_available()
        fields['created'] = detail['created']
        fields['updated'] = fields['created']

        data['fields'] = fields
        DATA.append(data)


def product_links(category):
    number_of_products = random.randint(1, 10)
    url = f"https://www.florastore.com/en/{category}"
    res = requests.get(url)
    print(f'{number_of_products} products from {category}: code --> {res.status_code}')
    soup = BeautifulSoup(res.content, 'lxml')
    products = soup.find_all(
        'div', attrs={"class": "col-xs-6 col-sm-4 col-md-3 productWrapper nopadding"})[:number_of_products]
    links = [image.a['href'] for image in products]
    products_details = [product_details(link) for link in links]
    with open('test.json', 'w') as file:
        json.dump(products_details, file, indent=4)
    return products_details


def product_details(url):
    res = requests.get(url)
    print(f'{url}\t\tcode --> {res.status_code}')
    soup = BeautifulSoup(res.content, 'lxml')
    title = soup.find('h1').span.text
    description = soup.find('div', attrs={'class': 'intro'}).text.strip()
    image_url = soup.find('a', attrs={'id': 'main-product'})['href']
    created = create_time()
    image = download_image(image_url, created, slugify(title))
    result = {
        'name': title,
        'desc': description,
        'image': image,
        'created': created
    }

    return result


def slugify(name):
    if len(name) > 100:
        raise NameError
    for char in ',!@#$%^&*()_+=-./\\[]{};\'":<>?':
        if char in name:
            name = name.replace(char, '')
    if '  ' in name:
        name = name.replace('  ', ' ')
        slugify(name)
    temp = name.rstrip().split(' ')
    slug = '-'.join(temp)
    return slug


def is_available():
    a = random.randint(1, 100)
    if a > 98:
        return False
    return True


def create_time():
    year = '{:02d}'.format(random.randint(10, 20))
    month = '{:02d}'.format(random.randint(1, 12))
    day = '{:02d}'.format(random.randint(1, 30))

    string = f"20{year}-{month}-{day}T09:36:19.536Z".replace(' ', '')
    return string


def time_slug(time):
    time = time.replace('-', '/')
    time = time[:time.index('T')]

    return time


# data = []
# file = open('products.json', 'w')
# for i in range(5):
#     data.append(product_generator())

# json.dump(data, file, indent=4)
# file.close()


def download_image(url, date, name):
    date = time_slug(date)

    directory = f"FlowerShop/media/products/{date}"
    os.makedirs(directory, exist_ok=True)
    urllib.request.urlretrieve(
        url, f'{directory}/{name}.jpg')
    path = f"products/{date}/{name}.jpg"
    return path


# download_image(
#     'https://cdn.webshopapp.com/shops/30495/files/150206318/300x300x2/calathea-crocata-in-basket.jpg', '2020/12/3/', 'tester')
# # product_links('houseplants/bulbs/')

data = list()
with open(f'{current_path}/category_names.json', 'r') as file:
    cat_names = json.load(file)
    for i in range(len(cat_names)):
        name, pk = cat_names.popitem()
        print(f'start:\t{name}')
        # print(name, pk)
        product_generator(name, pk)

        print('\n----------------------------------------------------------------------------------------------\n')

    with open(f'{current_path}/products.json', 'w') as file:
        json.dump(DATA, file, indent=4)
