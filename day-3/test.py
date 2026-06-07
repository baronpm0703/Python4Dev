import numpy as np

# Short-hand code of defining list of n - random values with numpy
list_a = np.random.randint(1, 30, size=20)

# List c = concatenation of list a and list b
list_c = [x for x in list_a if x % 2 == 1]
print(f"List A: {list_a} \n")
