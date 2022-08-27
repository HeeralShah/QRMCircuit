from http.client import PRECONDITION_FAILED
import numpy as np
from scipy.linalg import norm

                    
class Reg:


    

    def __init__(self, n):


        self.n = n
        self.psi = np.zeros((2,) *n )
        self.psi[(0,) *n ] = 1
        self.measure = [None] * n
    
        self._one_qubit_gates = {'H_matrix' : 1/np.sqrt(2) * np.array([[1, 1],
                                                                      [1, -1]]),
                              'X_matrix;': np.array([[0, 1], 
                                                    [1, 0]]),
                              'Z_matrix' : np.array([[1, 0], 
                                                     [0, -1]]),
                              'S_matrix' : np.array([[1, 0],
                                                     [0, 0+ 1j]])}

        self._CX_matrix = np.array([[1,0,0,0],
                          [0,1,0,0],
                          [0,0,0,1],
                          [0,0,1,0]])
        self._CZ_matrix = np.array([[1,0,0,0],
                          [0,1,0,0],
                          [0,0,1,0],
                          [0,0,0,-1]])
                    
        self._CX_tensor = np.reshape(self._CX_matrix, (2,2,2,2))
        self._CZ_tensor = np.reshape(self._CZ_matrix, (2,2,2,2))

        self._projectors=[np.array([[1,0],[0,0]]), np.array([[0,0],[0,1]])] # list containing the projectors |0><0| and |1><1|
    
    def one_qubit_op(self, operator, i):
        self.psi = np.tensordot(self._one_qubit_gates[operator], self.psi, (1, i))
        self.psi = np.moveaxis(self.psi, 0, i)
        return self
    
    def CX_op(self, control, target):
        self.psi = np.tensordot(self._CX_tensor, self.psi, ((2, 3), (control, target)))
        self.psi = np.moveaxis(self.psi, (0,1), (control, target))
        return self
    
    def CZ_op(self, control, target):
        self.psi = np.tensordot(self._CZ_tensor, self.psi, ((2, 3), (control, target)))
        self.psi = np.moveaxis(self.psi, (0,1), (control, target))
        return self


    def transversal(self, operator):
        i=0
        while i < self.n:
            self.one_qubit_op(operator, i)
            i+=1
        return self
    def qubit_reset(self, i):
        return None
    #    move = np.moveaxis(self.psi, 0, i)
    #    move[(0,) * self.n ] = 1
    #   move[(1, 0,) * (self.n -1 )]
    
    def reg_reset(self):
        self.psi = np.zeros((2,) *self.n )
        self.psi[(0,) * self.n ] = 1
        return self
    def project(self, i, j): # RETURN state with ith qubit of reg projected onto |j>
        self.psi = np.moveaxis(np.tensordot(self._projectors[j], self.psi, (1, i)), 0, i)
        return self
    
    def measure_qubit(self, i):
        projected = self.project(i, 0)
        norm_projected = norm(projected.psi.flatten())
        if np.random.random() < norm_projected ** 2:
            self.psi = projected.psi / norm_projected
            self.measure[i] = 0
        else:
            projected = self.project(i, 0)
            norm_projected = norm(projected.psi.flatten())
            self.psi = projected.psi / norm_projected
            self.measure[i] = 1
        
        return self




##################################  TESTING   #########################################
