from http.client import PRECONDITION_FAILED
from sqlite3 import paramstyle
import numpy as np
from scipy.linalg import norm
from abc import ABC, abstractmethod

class NoisyChannel(ABC):

    @abstractmethod
    def __init__(self, *args):
        pass

    @abstractmethod
    def one_qubit_noise(self, *args):
        pass

    @abstractmethod
    def multi_qubit_noise(self,  *args):
        pass


class DepolarizingNoise(NoisyChannel):

    def __init__(self, param):

        self.depol_param = param

        self.pauli_matrices = {0: np.array([[1,0], [0,1]]),
                               1: np.array([[0,1], [1,0]]),
                               2: np.array([[0,-1j], [1j,0]]),
                               3: np.array([[1,0], [0,-1]])}

        
    @staticmethod
    def one_qubit_noise(one_qubit_op):
        def wrapper_one_qubit_noise(cls, *args):
            param = cls.err_model.depol_param
            prob = np.random.random()
            if prob > param:
                one_qubit_op(cls, *args)
            else:
                num = np.random.randint(1, 4)
                cls.psi = np.tensordot(cls.err_model.pauli_matrices[num], cls.psi, (1, args[1]))
                one_qubit_op(cls, *args)
        return wrapper_one_qubit_noise

    def multi_qubit_noise(self, reg, *args):
        return super().multi_qubit_noise(reg, *args)

                    
class Reg:


    def __init__(self, n):


        self.n = n
        self.psi = np.zeros((2,) *n )
        self.psi[(0,) *n ] = 1
        self.measure = [None] * n
    
        self._one_qubit_gates = {'H_matrix' : 1/np.sqrt(2) * np.array([[1, 1],
                                                                      [1, -1]]),
                                 'X_matrix': np.array([[0, 1], 
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

        self._projectors= [np.array([[1,0],[0,0]]), np.array([[0,0],[0,1]])] # list containing the projectors |0><0| and |1><1|

        self.err_model = DepolarizingNoise(0.01)
    
    @DepolarizingNoise(0.01).one_qubit_noise
    def one_qubit_op(self, operator, i):
        self.psi = np.tensordot(self._one_qubit_gates[operator], self.psi, (1, i))
        self.psi = np.moveaxis(self.psi, 0, i)
        return self
    
    def CX_op(self, control, target):
        self.psi = np.tensordot(self._CX_tensor, self.psi, ((2, 3), (control, target)))
        self.psi = np.moveaxis(self.psi, (0,1), (control, target))
        return self

    
    def CX_multiqubit(self, control, target_arr):
        for i in target_arr:
            self.CX_op(control, i)
        return self
    
    def CZ_op(self, control, target):
        self.psi = np.tensordot(self._CZ_tensor, self.psi, ((2, 3), (control, target)))
        self.psi = np.moveaxis(self.psi, (0,1), (control, target))
        return self
    
    def CZ_multiqubit(self, control, target_arr):
        for i in target_arr:
            self.CZ_op(control, i)
        return self

    def transversal(self, operator):
        i=0
        while i < self.n:
            self.one_qubit_op(operator, i)
            i+=1
        return self
    
    
    def qubit_reset(self, i):
        self = self.measure_qubit(i)
        if self.measure[i] == 1:
            self.psi = np.tensordot(np.array([[0,1], [1,0]]), self.psi, (1, i)) #want to use X operator which will not have noise, even after nosie decorator is added to one_qubit_op
            self.psi = np.moveaxis(self.psi, 0, i)
        
        return self

    def reg_reset(self):
        self.psi = np.zeros((2,) *self.n )
        self.psi[(0,) * self.n ] = 1
        return self


    def project(self, i, j): # RETURN state with ith qubit of reg projected onto |j>
        self.psi = np.tensordot(self._projectors[j], self.psi, (1, i))
        self.psi = np.moveaxis(self.psi, 0, i)
        return self
    
    def measure_qubit(self, i):
        trial_zero_proj = Reg(self.n)
        trial_one_proj  = Reg(self.n)

        trial_zero_proj.psi = self.psi
        trial_one_proj.psi = self.psi

        projected_zero = trial_zero_proj.project(i, 0)
        norm_projected_zero = norm(projected_zero.psi.flatten())
        random = np.random.random()
        
        if random < norm_projected_zero ** 2:
            self.psi = projected_zero.psi / norm_projected_zero
            self.measure[i] = 0
        else:
            projected_one = trial_one_proj.project(i, 1)
            norm_projected_one = norm(projected_one.psi.flatten())
            self.psi = projected_one.psi / norm_projected_one
            self.measure[i] = 1
        
        return self

    def measure_all(self):
        for i in range(self.n):
            self.measure_qubit(i)
        
        return self



