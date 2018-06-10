from .. import models
from constants import *

def add_item(params):
 
    if (params['user_id'] != ADMIN_ID) :
        return {KEY_STATUS: STATUS_FAILED, KEY_MESSAGE: NOT_AUTHORIZED}
    item_code = params['item_code']
    item_name = params['item_name']
    price = params['price']
    category = params['category']
    colour = params['colour']

    new_item = models.Item(
        item_code = item_code,
        item_name = item_name,
        price = price,
        category = category,
        colour = colour
        )

    new_item.save()

    return  {"id": new_item.id}

def remove_item(params):

    if (params['user_id'] != ADMIN_ID) :
        return {KEY_STATUS: STATUS_FAILED, KEY_MESSAGE: NOT_AUTHORIZED}
    item_id = params['item_id']
    models.Item.objects.get(id=item_id).delete()

    return {"status": "SUCCESS"}

def get_all_items():
    
    items = models.Item.objects.all()

    all_items = []
    for item in items :
        r = {
          "id" : item.id,
          "item_code": item.item_code,
          "price": item.price,
          "category": item.category,
          "colour": item.colour,
          "item_name": item.item_name
        }
        all_items.append(r)

    res = {"items": all_items}

    return res


def search():

    return 0