

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


if __name__ == '__main__':
    names = ['wine', 'beer', 'pizza', 'burger',
             'fries', 'cola', 'apple', 'donut', 'cake']
    values = [89, 90, 95, 100, 90, 79, 50, 10, 40]
    calories = [123, 154, 258, 354, 365, 150, 95, 195, 120]
    foods = build_menu(names, values, calories)
    test_all_greedy(foods, 1000)
