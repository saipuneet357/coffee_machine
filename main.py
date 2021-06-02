import json

x = {
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


class Coffee_Machine():

    # Initializing coffee machine
    def __init__(self, n, items):

        # Number of outlets (n)
        self.n = n
        # Ingredient quantity (item_quantity)
        self.item_quantity = items
        # Assuming that the max quantity is the inital quantity which is given
        self.max_item_quantity = items

    # To serve beverage
    def serve_beverage(self, beverage):
        '''
        param:
            beverage: Dictionary with ingredients and quantities

        '''
        item_dict = beverage
        new_item_quantity = self.item_quantity
        is_available = True
        for item in item_dict.keys():
            if new_item_quantity.get(item, None) is None:
                print('{} cannot be prepared because {} is not available'.format(beverage, item))
                is_available = False
                break

            elif new_item_quantity.get(item) < item_dict.get(item):
                print('{} cannot be prepared because {} is not sufficient'.format(beverage, item))
                is_available = False
                break
            else:
                new_item_quantity[item] -= item_dict.get(item)

        if is_available:
            self.item_quantity = new_item_quantity
            print('{} is prepared'.format(beverage))
            # Display ingredient quantity after serving beverage
            self.indicate()

    # To indicate quantity of available ingredients
    def indicate(self):
        '''
        param:
            No parameters required

        '''
        refill_ingredients = []
        for item in self.item_quantity.keys():
            # Checking if quantity is less than 20% of the maximum amount
            if self.item_quantity.get(item) < 0.2*self.max_item_quantity.get(item):
                refill_ingredients.append(item)
                print('{}: {} [ALERT] Low quantity'.format(item, self.item_quantity[item]))
            else:
                print('{}: {}'.format(item, self.item_quantity[item]))

        if len(refill_ingredients) > 0:
            print('Refilling Ingredients: {}'.format(refill_ingredients))
            self.refill(refill_ingredients)

    # To refill ingredients
    def refill(self, ingredients=None, amount=None):
        '''
        param:
            ingredients: list of ingredient names to be refilled

        '''
        # To refill specific ingredients
        if ingredients is not None:
            assert isinstance(ingredients, []), "Ingredients not provided in List"
            for ingredient in ingredients:
                # Refill ingredient with amount given
                if amount is not None:
                    self.item_quantity[ingredient] = float(amount)
                    print('{} refilled to {}'.format(ingredient, str(amount)))
                # Refill ingredient with the maximum amount
                else:
                    self.item_quantity[ingredient] = self.max_item_quantity.get(ingredient)
                    print('{} refilled to max amount'.format(ingredient))
            return

        # If no ingredient is given refilling all ingredients
        self.item_quantity = self.max_item_quantity
        print('All ingredients refilled to max amount')


n = x['machine']['outlets']['count_n']
items = x['machine']['total_items_quantity']

m = Coffee_Machine(n, items)

m.indicate()
# print(m.item_quantity)
# items_available, items_not_available = m.get_drink(x['machine']['beverages'])
#
# m.print_drinks(items_available, items_not_available)
#
# print(m.item_quantity)
