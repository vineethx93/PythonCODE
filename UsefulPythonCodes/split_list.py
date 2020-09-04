

# splits a passed list to m number of lists each having maximum of n elements
# parameters list_to_split, maximum elements in each of the generated splitted lists
def split_list(list_to_split, n_max):
    splitted_list = [list_to_split]
    for item in splitted_list:
        if len(item) > n_max:
            splitted_list.append(item[0:n_max])
            splitted_list.append(item[n_max:])
            splitted_list.remove(item)
    return splitted_list


list_to_split = [1, 2, 3, 4, 5]
n_max = 2
print(split_list(list_to_split, n_max))

