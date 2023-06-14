import numpy as np

def get_closest_element_and_index(arr, val):
    # find the index where val should be inserted to maintain the order of arr
    idx = np.searchsorted(arr, val)
    # check if idx is valid
    if idx == 0:
        # return the first element and its index
        return (arr[0], 0)
    elif idx == len(arr):
        # return the last element and its index
        return (arr[-1], len(arr)-1)
    else:
        # calculate the difference between val and the previous element and the next element
        diff_prev = np.abs(val - arr[idx-1])
        diff_next = np.abs(val - arr[idx])
        # check which one is closer to val
        if diff_prev < diff_next:
            # return the previous element and its index
            return (arr[idx-1], idx-1)
        else:
            # return the next element and its index
            return (arr[idx], idx)
