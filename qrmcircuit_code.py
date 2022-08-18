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

CX_matrix = np.array([[1,0,0,0],
                      [0,1,0,0],
                      [0,0,0,1],
                      [0,0,1,0]])

CZ_matrix = np.array([[1,0,0,0],
                      [0,1,0,0],
                      [0,0,1,0],
                      [0,0,0,-1]])
                    

CX_tensor = np.reshape(CX_matrix, (2,2,2,2))

CZ_tensor = np.reshape(CZ_matrix, (2,2,2,2))

                    
class Reg:
    def __init__(self, n):
        self.n = n
        self.psi = np.zeros((2,) *n )
        self.psi[(0,) *n ] = 1
    
    def one_qubit_op(self, operator, i):
        self.psi = np.tensordot(operator, self.psi, (1, i))
        self.psi = np.moveaxis(self.psi, 0, i)
        return self

    def transversal(self, operator):
        i=0
        while i < self.n:
            self.one_qubit_op(operator, i)
            i+=1
        return self



reg = Reg(4)
#print(reg.psi)

#final_reg = reg.transversal(reg.H)
med_reg = reg.transversal(H_matrix)
final_reg = reg.transversal(S_matrix)

print(final_reg.psi)








#main_circ = np.zeros((2,2,2))

#print (main_circ)
#print(main_circ.size)



#print(CNOT_tensor)