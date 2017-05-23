"""
https://stackoverflow.com/a/2070509/855632
"""


def find_subset(array):
    array = sorted(array)
    length = len(array)
    for i in range(0, length - 2):
        j = i + 1
        k = length - 1
        while k >= j:
            sum_of_tree = array[i] + array[j] + array[k]
            if sum_of_tree == 0:
                return (array[i], array[j], array[k])
            elif sum_of_tree > 0:
                k -= 1
            else:
                j += 1
