import numpy as np
from scipy.linalg import norm

H_matrix = 1/np.sqrt(2) * np.array([[1, 1],
                                    [1, -1]])

X_matrix = np.array([[0, 1], 
                     [1, 0]])

Z_matrix = np.array([[1, 0],
                     [0, -1]])

S_matrix = np.array([[1, 0],
                    [0, 0+ 1j]])

#print(S_matrix.imag)

CNOT_matrix = np.array([[1,0,0,0],
                        [0,1,0,0],
                        [0,0,0,1],
                        [0,0,1,0]])
                    

CNOT_tensor = np.reshape(CNOT_matrix, (2,2,2,2))

class Reg:
    def __init__(self, n):
        self.n = n
        self.psi = np.zeros((2,) *n )
        self.psi[(0,) *n ] = 1





#main_circ = np.zeros((2,2,2))

#print (main_circ)
#print(main_circ.size)



#print(CNOT_tensor)