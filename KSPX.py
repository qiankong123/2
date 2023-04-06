
# Here is an implementation of the Quick Sort algorithm in Python:

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        left = []
        right = []
        for i in arr[1:]:
            if i < pivot:
                left.append(i)
            else:
                right.append(i)
        return quick_sort(left) + [pivot] + quick_sort(right)

# To use this function, simply call it with a list of numbers as the argument:
my_list = [3, 6, 1, 8, 4, 2]
sorted_list = quick_sort(my_list)
print(sorted_list)

# Output: [1, 2, 3, 4, 6, 8]