import numpy as np

a = np.arange(60.).reshape(3,2,2,5)
b = np.arange(24.).reshape(3,2,4)


c = np.tensordot(a,b, axes=([1,0],[1,0]))

#print(c)

a = np.array(range(1, 9))
a.shape = (2, 2, 2)
A = np.array(('a', 'b', 'c', 'd'), dtype=object)
A.shape = (2, 2)

print(a)
print(A)

td1 = np.tensordot(a, A, 1) #dot product

td2 = np.tensordot(a, A, (0, 1))

td3 = np.tensordot(a, A, (2, 1))

td4= np.tensordot(a, A, ((0, 1), (0, 1)))

td5 = np.tensordot(a, A, ((2, 1), (1, 0)))
td6 = np.tensordot(a, A, ((1, 2), (0, 1)))

print(td5)
print(td6)
