from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import *
from qiskit.tools.monitor import job_monitor
from qiskit.opflow.expectations import PauliExpectation
from qiskit.tools.jupyter import *
from qiskit.visualization import *
from qiskit.opflow.state_fns import *
from qiskit.quantum_info import *
from qiskit.transpiler.passes import *
from qiskit.opflow import *
from qiskit.providers.aer import QasmSimulator
from qiskit.utils import QuantumInstance
import numpy as np
import pickle


# SPECIFY The `trotter_steps` you want to evaluate on
MY_TROTTER_STEPS = 8
TARGET_TIME = np.pi  # we'll not change this, you can use it for convenience

def my_trotter(trotter_steps):

    t = Parameter('t')
    t = TARGET_TIME / trotter_steps
    
    def reduced_cnot(t):
        qr = QuantumRegister(2)
        qc = QuantumCircuit(qr)
        qc.cnot(0,1)
        qc.rx(2*t-np.pi/2, 0)
        qc.rz(2 * t, 1)
        qc.h(0)
        qc.cnot(0,1)
        qc.h(0)
        qc.rz(-2 * t, 1)
        qc.cnot(0,1)
        qc.rx(np.pi/2,0)
        qc.rx(-np.pi/2,1)
        return qc

    def sim_circ(trot_steps,t):
        reduced_cnot_instructions=reduced_cnot(t).to_instruction()
        Tr=QuantumRegister(3)
        Tc=QuantumCircuit(Tr)
        Tc.append(reduced_cnot_instructions, [0,1])
        Tc.append(reduced_cnot_instructions, [1,2])
        Tc=Tc.to_instruction()
        Trot_qr=QuantumRegister(3)
        Trot_qc=QuantumCircuit(Trot_qr, name='xxx')
        for _ in range(trot_steps):
            Trot_qc.append(Tc, [Trot_qr[0],Trot_qr[1],Trot_qr[2]])

        return Trot_qc

    # Combine subcircuits into a single multiqubit gate representing a single trotter step
    num_qubits = 3

    # Convert custom quantum circuit into a gate
    Trot_qr = QuantumRegister(num_qubits)
    Trot_qc = QuantumCircuit(Trot_qr, name='Trot')
   
    # End of my trotter implementation
    Trot_gate = sim_circ(1,t).to_instruction()
    return Trot_gate, [1, 3, 5]
