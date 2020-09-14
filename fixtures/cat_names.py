import json
import os

current = os.path.dirname(os.path.realpath(__file__))

with open(f'{current}/categories.json', 'r') as file:
    cat_json = json.load(file)

names = {}
for cat in cat_json:
    if cat['fields']['parent']:
        parent_pk = cat['fields']['parent']
        slug = []
        for temp in cat_json:
            if temp['pk'] == parent_pk:
                slug.append(temp['fields']['slug'])
        slug = slug[::-1]
        print(slug)
        pk = cat['pk']
        name = slug
    # print(name, pk)


# with open(f'{current}/category_names.json', 'w') as file:
#     json.dump(names, file)
