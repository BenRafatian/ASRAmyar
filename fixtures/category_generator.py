import random
import json

CATEGORY_CHOICES = list(range(1, 10))


'''
{
    "model": "shop.category",
    "pk": 3,
    "fields": {
      "name": "Plants",
      "parent": null,
      "slug": "plants",
      "lft": 1,
      "rght": 6,
      "tree_id": 1,
      "level": 0
}
'''


def product_generator():
    data = {}
    fields = {}
    data['model'] = "shop.product"
    fields['category'] = str(random.choice(CATEGORY_CHOICES))
    fields['name'] = ''  # TODO: add name generator
    fields['slug'] = slugify(fields['name'])
    fields['image'] = ''
    fields['description'] = ''
    fields['price'] = random.randint(1, 100)
    fields['available'] = is_available()
    fields['created'] = create_time()
    fields['updated'] = fields['created']

    data['fields'] = fields
    return data


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
    if a > 90:
        return False
    return True


def create_time():
    year = '{:02d}'.format(random.randint(10, 20))
    month = '{: 02d}'.format(random.randint(1, 12))
    day = '{: 02d}'.format(random.randint(1, 30))

    string = f"20{year}-{month}-{day}T09:36:19.536Z".replace(' ', '')
    return string


data = []
file = open('products.json', 'w')
for i in range(5):
    data.append(product_generator())

json.dump(data, file, indent=4)
file.close()
