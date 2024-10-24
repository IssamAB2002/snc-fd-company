import random
# create random slce function with params oringial array (arr) & wanted subarray size (subarray_size)


def random_slice(arr, subarray_size):
    # if wanted size is bigger than len of arr return arr
    if subarray_size > len(arr):
        return arr
    # define start index = random number from 0 & (len of arr - subarray_size)
    start_index = random.randint(0, len(arr) - subarray_size)
    # define end index = random number from start index (above) + subarray_size
    end_index = start_index + subarray_size
    # return sliced array from start to end index
    return arr[start_index:end_index]
