from http.client import PRECONDITION_FAILED
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


projectors=[np.array([[1,0],[0,0]]), np.array([[0,0],[0,1]]) ] # list containing the projectors |0><0| and |1><1|

                    
class Reg:

    def __init__(self, n):
        self.n = n
        self.psi = np.zeros((2,) *n )
        self.psi[(0,) *n ] = 1
    
    def one_qubit_op(self, operator, i):
        self.psi = np.tensordot(operator, self.psi, (1, i))
        self.psi = np.moveaxis(self.psi, 0, i)
        return self
    
    def CX_op(self, control, target):
        self.psi = np.tensordot(CX_tensor, self.psi, ((2, 3), (control, target)))
        self.psi = np.moveaxis(self.psi, (0,1), (control, target))
        return self
    
    def CZ_op(self, control, target):
        self.psi = np.tensordot(CZ_tensor, self.psi, ((2, 3), (control, target)))
        self.psi = np.moveaxis(self.psi, (0,1), (control, target))
        return self

    def transversal(self, operator):
        i=0
        while i < self.n:
            self.one_qubit_op(operator, i)
            i+=1
        return self
    
    def reg_reset(self):
        self.psi = np.zeros((2,) *self.n )
        self.psi[(0,) *self.n ] = 1
        return self

    def project(self, i, j): # RETURN state with ith qubit of reg projected onto |j>
        self.psi = np.moveaxis(np.tensordot(projectors[j], self.psi, (1, i)), 0, i)
        return self
    







##################################  TESTING   #########################################

reg = Reg(4)
#print(reg.psi)

#final_reg = reg.transversal(reg.H)
med_reg = reg.transversal(H_matrix)
final_reg = reg.transversal(S_matrix)

print(final_reg.psi)

reset_reg = final_reg.reg_reset()

print(reset_reg.psi)

reg2 = Reg(3)
reg2 = reg2.one_qubit_op(X_matrix, 2)
print(reg2.psi)

reg2.CX_op(2, 0)
reg2.CZ_op(0, 2)
print(reg2.psi)