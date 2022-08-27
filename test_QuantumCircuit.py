from QuantumCircuit import Reg

def basicTest():
    reg = Reg(4)
    print(reg.measure)
    print(reg.psi)
    med_reg = reg.transversal('H_matrix')
    final_reg = reg.transversal('S_matrix')
    print(final_reg.psi)
    reset_reg = final_reg.measure_qubit(2).measure
    print(reset_reg)


counter = 0
i=0
while i < 100:
    reg = Reg(4)
    #print(reg.measure)
    #print(reg.psi)
    #final_reg = reg.transversal(reg.H)
    med_reg = reg.transversal('H_matrix')
    #final_reg = reg.transversal('S_matrix')
    #print(final_reg.psi)
    reset_reg = med_reg.measure_qubit(2).measure
    
    #print(reset_reg)
    if reset_reg[2] == 0:
        counter +=1
        
    i+=1
        
print(counter)
print(i)

#print(testEqualProb())
        
def testTwoQubitGates():
    reg2 = Reg(3)
    reg2 = reg2.one_qubit_op('X_matrix', 2)
    print(reg2.psi)

    reg2.CX_op(2, 0)
    print(reg2.psi)
    reg2.CZ_op(0, 2)
    print(reg2.psi)


    


