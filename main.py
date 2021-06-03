import multiprocessing
import copy
from ctypes import c_char_p

# Sample Data
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



# Beverage Object
class Beverage(object):

    # Initializing Beverage
    def __init__(self, beverage_name):
        self.ingredients = {}
        self.beverage_name = beverage_name

    # To add ingredients to make beverage
    def add_ingredient(self, ingredient, quantity):
        '''
        param:
            ingredient: ingredient name (string)
            quantity: quantity (numeric)

        '''
        if self.ingredients.get(ingredient, None) is not None:
            print('{} already exist'.format(ingredient))
            return

        self.ingredients[ingredient] = quantity
        print('{} added to beverage {}'.format(ingredient, self.beverage_name))

    # To remove ingredients
    def remove_ingredient(self, ingredient):
        '''
        param:
            ingredient: ingredient name (string)

        '''
        if self.ingredients.get(ingredient, None) is None:
            print('{} does not exist'.format(ingredient))
            return

        del self.ingredients[ingredient]
        print('{} removed from beverage {}'.format(ingredient, self.beverage_name))

    # To update quantity of ingredients required
    def update_ingredient(self, ingredient, quantity, increase=True):
        '''
        param:
            ingredient: ingredient name (string)
            quantity: quantity (numeric)
            increase(optional): to increase or decrease quantity (boolean)

        '''
        if self.ingredients.get(ingredient, None) is None:
            print('{} does not exist'.format(ingredient))
            return

        if not increase:
            quantity *= -1
            if self.ingredients[ingredient] + quantity < 0:
                print('Updated quantity is below zero so updating the quantity to 0')
                self.ingredients[ingredient] = 0
                print('Quantity of {} updated to 0'.format(ingredient))
                return

        self.ingredients[ingredient] += quantity
        print('Quantity of {} updated by {}'.format(ingredient, quantity))


    def get_ingredients(self):
        '''
        param:
            No parameters required
        '''

        print('Ingredients for {}: '.format(self.beverage_name))
        for ingredient in self.ingredients.keys():
            print('{}: {}'.format(ingredient, self.ingredients[ingredient]))


# Coffee Machine
class Coffee_Machine(object):

    # Initializing coffee machine
    def __init__(self, n, items):
        # Number of outlets (n)
        self.outlets = []
        for i in range(n):
            outlet = (i+1)
            print('Coffee outlet {} created'.format(i+1))
            self.outlets.append(outlet)

        # Ingredient quantity (item_quantity)
        self.item_quantity = items
        # Assuming that the max quantity is the inital quantity which is given
        self.max_item_quantity = copy.copy(items)

    # To serve beverage
    def serve_beverage(self, beverage, beverage_name):
        '''
        param:
            beverage: Dictionary with ingredients and quantities
            beverage_name: Beverage Name string

        '''
        item_dict = beverage
        new_item_quantity = self.item_quantity
        is_available = True
        for item in item_dict.keys():
            if new_item_quantity.get(item, None) is None:
                print('{} cannot be prepared because {} is not available'.format(beverage_name, item))
                is_available = False
                break

            elif new_item_quantity.get(item) < item_dict.get(item):
                print('{} cannot be prepared because {} is not sufficient'.format(beverage_name, item))
                is_available = False
                break
            else:
                new_item_quantity[item] -= item_dict.get(item)

        if is_available:
            self.item_quantity = new_item_quantity
            print('{} is prepared'.format(beverage_name))
            print('----------------------------------')
            print('Remaining ingredients:')
            # Display ingredient quantity after serving beverage
            self.indicate()
            print('----------------------------------')

    # Serve with outlets
    def serve(self, beverage, beverage_name):
        '''
        param:
            beverage: Dictionary with ingredients and quantities
            beverage_name: Beverage Name string

        '''
        outlet = None
        # Check for any available outlets
        if len(self.outlets) > 0:
            outlet = self.outlets.pop()
            # Serve beverage with that outlet
            self.serve_beverage(beverage, beverage_name)
        else:
            print('No coffee outlet is available to serve beverage')
            return

        self.outlets.append(outlet)

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
            print('Refilling Ingredients: {}'.format(','.join(refill_ingredients)))
            for ingredient in refill_ingredients:
                self.refill(ingredient)

    # To refill ingredients
    def refill(self, ingredient=None, amount=None):
        '''
        param:
            ingredients: Ingredient to be refilled
            amount: amount of ingredient to be refilled

        '''
        # To refill specific ingredients
        if ingredient is not None:

            # Refill ingredient with amount given
            if amount is not None:
                self.item_quantity[ingredient] = float(amount)
                print('{} refilled to {}'.format(ingredient, str(amount)))

            # Refill ingredient with the maximum amount
            else:
                self.item_quantity[ingredient] = self.max_item_quantity.get(ingredient)
                print('{}: {}| Refilled to max amount'.format(ingredient, self.item_quantity[ingredient]))

            return

        # If no ingredient is given refilling all ingredients
        self.item_quantity = self.max_item_quantity
        print('All ingredients refilled to max amount')


if __name__ == '__main__':
    n = x['machine']['outlets']['count_n']
    items = x['machine']['total_items_quantity']
    beverages = x['machine']['beverages']
    beverage_list = []

    # Beverage test cases
    for beverage in beverages.keys():

        # Creating new beverage
        obj = Beverage(beverage)
        beverage_list.append(obj)

        for ingredient in beverages[beverage].keys():

            # Adding ingredient to beverage
            obj.add_ingredient(ingredient, beverages[beverage][ingredient])

            # Uncomment below to remove ingredient from beverage
            # obj.remove_ingredient(ingredient)

            # Increase quantity of ingredient
            obj.update_ingredient(ingredient, 10, True)

            # Decrease quantity of ingredient
            obj.update_ingredient(ingredient, 10, False)

            # Decrease quantity of ingredient
            obj.update_ingredient(ingredient, 500, False)

            # Show all ingredients
            obj.get_ingredients()

    # Creating new coffee machine
    m = Coffee_Machine(n, items)

    # Coffee Machine test cases
    for beverage in beverage_list:

        # Serving Coffee
        m.serve_beverage(beverage.ingredients, beverage.beverage_name)

        # Serving Coffee through outlet
        m.serve(beverage.ingredients, beverage.beverage_name)

        # Indicate Current ingredient quantity
        m.indicate()

        # Refill all ingredients
        m.refill()

        # Refill single ingredient
        m.refill('ginger_syrup', 100)



    # Parallelizing is not working
    # for beverage in beverage_list:
    #     q = multiprocessing.Queue()
    #     x = multiprocessing.Value(c_char_p, beverage.beverage_name)
    #     q.put(beverage.ingredients)
    #     p1 = multiprocessing.Process(target=m.serve, args=(q, x))
    #     # p2 = multiprocessing.Process(target=m.serve, args=(q, x))
    #     # p3 = multiprocessing.Process(target=m.serve, args=(q, x))
    #     # # starting process 1
    #     p1.start()
    #     # # starting process 2
    #     # p2.start()
    #     # # starting process 3
    #     # p3.start()
    #     # # wait until process 1 is finished
    #     p1.join()
    #     # # wait until process 2 is finished
    #     # p2.join()
    #     # # wait until process 3 is finished
    #     # p3.join()
    #     # # both processes finished
