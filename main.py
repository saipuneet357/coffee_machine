import json


x ={
  "machine": {
    "outlets": {
      "count_n": 3
    },
    "total_items_quantity": {
      "hot_water": 500,
      "hot_milk": 500,
      "ginger_syrup": 100,
      "sugar_syrup": 100,
      "tea_leaves_syrup": 100
    },
    "beverages": {
      "hot_tea": {
        "hot_water": 200,
        "hot_milk": 100,
        "ginger_syrup": 10,
        "sugar_syrup": 10,
        "tea_leaves_syrup": 30
      },
      "hot_coffee": {
        "hot_water": 100,
        "ginger_syrup": 30,
        "hot_milk": 400,
        "sugar_syrup": 50,
        "tea_leaves_syrup": 30
      },
      "black_tea": {
        "hot_water": 300,
        "ginger_syrup": 30,
        "sugar_syrup": 50,
        "tea_leaves_syrup": 30
      },
      "green_tea": {
        "hot_water": 100,
        "ginger_syrup": 30,
        "sugar_syrup": 50,
        "green_mixture": 30
      },
    }
  }
}






class CM():

    def __init__(self, n, items):

        self.n = n
        self.item_quantity = items

    def get_drink(self, beverages):

        items_available = []
        items_not_available = []
        for beverage in beverages:
            item_dict = beverages[beverage]
            new_item_quantity = self.item_quantity
            is_available = True
            for item in item_dict.keys():
                if new_item_quantity.get(item, None) is None:
                    print('{} is not available'.format(item))
                    items_not_available.append('{} cannot be prepared because {} is not available'.format(beverage, item))
                    is_available = False
                    break
                elif new_item_quantity.get(item) < item_dict.get(item):
                    print('{} is not sufficient'.format(item))
                    items_not_available.append('{} cannot be prepared because {} is not sufficient'.format(beverage, item))
                    is_available = False
                    break
                else:
                    new_item_quantity[item] -= item_dict.get(item)
                    continue

            if is_available:
                    self.item_quantity = new_item_quantity
                    items_available.append('{} is prepared'.format(beverage))

        return items_available, items_not_available

    def print_drinks(self, items_available, items_not_available):

        for items in items_available:
            print(items)
        for items in items_not_available:
            print(items)


class CM_OutLet(CM):



# l = json.loads(x)

n = x['machine']['outlets']['count_n']
items = x['machine']['total_items_quantity']

m = CM(n, items)
print(m.item_quantity)
items_available, items_not_available = m.get_drink(x['machine']['beverages'])

m.print_drinks(items_available, items_not_available)

print(m.item_quantity)
