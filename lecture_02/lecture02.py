import random

class Food():
    def __init__(self, name, value, calories):
        self.name = name
        self.value = value
        self.calories = calories

    def get_value(self):
        return self.value

    def get_cost(self):
        return self.calories

    def density(self):
        return self.get_value()/self.get_cost()

    def __str__(self):
        return f'{self.name}: <{self.value}, {self.calories}>'


def build_menu(names, values, calories):
    """Create a list of Food. Names, values, calories lists of same length.

    Args:
        names (list[str]): List of food names.
        values (list[int]): List of food amount.
        calories (list[int]): list of food calories
    Return:
        menu (list[Food]): List of Foods
    """
    menu = [
        Food(name, val, cal) for name, val, cal in list(zip(names, values, calories))
    ]
    return menu


def greedy(items, max_cost, key_function):
    """Greedy algorithm for backpack problem.

    Args:
        items (list[Food]): List of Food class.
        max_cost (int): Max capability. max_cost >= 0.
        key_function: Maps elements of items to numbers.
    Return:
        result (list): list of Food class.
        total_value: amount of Food in result list.
    """
    items_copy = sorted(items, key=key_function, reverse=True)
    result = []
    total_value, total_cost = 0, 0

    for item in items_copy:
        if total_cost + item.get_cost() <= max_cost:
            result.append(item)
            total_cost += item.get_cost()
            total_value += item.get_value()
    return (result, total_value)


def test_greedy(items, constraint, key_function):
    taken, val = greedy(items, constraint, key_function)
    print('Total value of items taken =', val)
    for item in taken:
        print('\t', item)


def test_all_greedy(foods, max_units):
    print('Use greedy by value to allocate', max_units, 'calories.')
    test_greedy(foods, max_units, Food.get_value)
    print('Use greedy by cost to allocate', max_units, 'calories.')
    test_greedy(foods, max_units, lambda x: 1/Food.get_cost(x))
    print('Use greedy by density to allocate', max_units, 'calories.')
    test_greedy(foods, max_units, Food.density)



def max_val(to_consider, avail):
    """Assumes to_consider a list of items, avail a weight.
       Returns a tuple of the total value of a solution to the
       0/1 knapsack problem and the items of that solution"""
    if to_consider == [] or avail == 0:
        result = (0, ())
    elif to_consider[0].get_cost() > avail:
        #Explore right branch only
        result = max_val(to_consider[1:], avail)
    else:
        next_item = to_consider[0]
        #Explore left branch
        with_val, with_to_take = max_val(
            to_consider[1:], avail - next_item.get_cost()
        )
        with_val += next_item.get_value()
        #Explore right branch
        without_val, without_to_take = max_val(to_consider[1:], avail)
        #Choose better branch
        if with_val > without_val:
            result = (with_val, with_to_take + (next_item,))
        else:
            result = (without_val, without_to_take)
    return result


def fast_max_val(to_consider, avail, memo={}):
    """Assumes to_consider a list of subjects, avail a weight
    memo supplied by recursive calls.
    Returns a tuple of the total value of a solution to the
    0/1 knapsack problem and the subjects of that solution"""
    if (len(to_consider), avail) in memo:
        result = memo[(len(to_consider), avail)]
    elif to_consider == [] or avail == 0:
        result = (0, ())
    elif to_consider[0].get_cost() > avail:
        #Explore right branch only
        result = fast_max_val(to_consider[1:], avail, memo)
    else:
        next_item = to_consider[0]
        #Explore left branch
        with_val, with_to_take = fast_max_val(
            to_consider[1:], avail - next_item.get_cost(), memo
        )
        with_val += next_item.get_value()
        #Explore right branch
        without_val, without_to_take = fast_max_val(
            to_consider[1:], avail, memo
        )
        #Choose better branch
        if with_val > without_val:
            result = (with_val, with_to_take + (next_item,))
        else:
            result = (without_val, without_to_take)
    memo[(len(to_consider), avail)] = result
    return result


def test_max_val(foods, max_units, print_items=True):
    print(f'Use search tree to allocate {max_units} calories')
    val, taken = max_val(foods, max_units)
    print('Total values of items:', val)
    if print_items:
        for item in taken:
            print(f'\t{item}')

def test_fast_max_val(foods, max_units, algorithm, print_items=True):
    print('Menu contains', len(foods), 'items')
    print('Use search tree to allocate', max_units,
          'calories')
    val, taken = algorithm(foods, max_units)
    if print_items:
        print('Total value of items taken =', val)
        for item in taken:
            print('   ', item)


def build_bigger_menu(num_items, max_val, max_cost):
    items = []
    print(f'Try a menu with {num_items} items')
    for i in range(num_items):
        items.append(
            Food(
                str(i),
                random.randint(1, max_val),
                random.randint(1, max_cost)
            )
        )
    return items


if __name__ == '__main__':
    names = ['wine', 'beer', 'pizza', 'burger',
             'fries', 'cola', 'apple', 'donut', 'cake']
    values = [89, 90, 95, 100, 90, 79, 50, 10, 40]
    calories = [123, 154, 258, 354, 365, 150, 95, 195, 120]
    foods = build_menu(names, values, calories)
    # test_all_greedy(foods, 750)
    # print()
    # test_max_val(foods, 750)
    # for num_items in range(5, 65, 5):
    #     items = build_bigger_menu(num_items, 90, 250)
    #     test_max_val(items, 750, False)
    for numItems in (5, 10, 15, 20, 25, 30, 35, 40, 45, 50):
       items = build_bigger_menu(numItems, 90, 250)
       test_fast_max_val(items, 750, fast_max_val, False)
