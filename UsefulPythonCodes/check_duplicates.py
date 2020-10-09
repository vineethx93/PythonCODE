

items = ['a', 'b', 'b', 'c', 'd', 'd', 'd']
item_count_set = set()
for item in items:
    count = items.count(item)
    if count > 1:
        item_count_str = str(item + ':' + str(count))
        item_count_set.add(item_count_str)

print(item_count_set)
