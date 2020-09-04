from operator import getitem
from collections import OrderedDict

cost = dict()

cost['WK 1 AUG FY2020'] = {'week_num': 202001, 'week_name': 'WK 1 AUG FY2020', 'source': 0.00, 'target': 0.00,
                           'delta': 0.00, 'result': ''}

cost['WK 5 AUG FY2020'] = {'week_num': 202005, 'week_name': 'WK 5 AUG FY2020', 'source': 0.00, 'target': 0.00,
                           'delta': 0.00, 'result': ''}

cost['WK 3 AUG FY2020'] = {'week_num': 202003, 'week_name': 'WK 3 AUG FY2020', 'source': 0.00, 'target': 0.00,
                           'delta': 0.00, 'result': ''}

cost['WK 4 AUG FY2020'] = {'week_num': 202004, 'week_name': 'WK 4 AUG FY2020', 'source': 0.00, 'target': 0.00,
                           'delta': 0.00, 'result': ''}

cost['WK 2 AUG FY2020'] = {'week_num': 202002, 'week_name': 'WK 2 AUG FY2020', 'source': 0.00, 'target': 0.00,
                           'delta': 0.00, 'result': ''}

print('raw_dict:', cost)

# create an ordered dict to store the sorted items
sorted_cost = OrderedDict()

# now we sort the items on week_name and add it to ordered dict
for key, value in sorted(cost.items(), key=lambda x: getitem(x[1], 'week_name')):
    sorted_cost[key] = value

# print out ordered dict
print(sorted_cost)
