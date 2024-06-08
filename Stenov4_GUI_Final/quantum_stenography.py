import tkinter as tk
from tkinter import font as tkFont
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit import transpile
import numpy as np
import matplotlib.pyplot as plt
import random
import string
import winsound as ws

def get_secret_msg():
    global secret_msg
    secret_msg = entry.get()
    root.destroy()

root = tk.Tk()
root.title("Matrix Secret Message Input")

root.configure(bg="black")

matrix_font = tkFont.Font(family="Courier", size=12, weight="bold")

tk.Label(root, text="Enter your secret message:", font=matrix_font, fg="#00FF00", bg="black").pack(pady=10)
entry = tk.Entry(root, width=50, font=matrix_font, fg="#00FF00", bg="black", insertbackground="green")##########
entry.pack(pady=10)
tk.Button(root, text="Submit", command=get_secret_msg, font=matrix_font, fg="#00FF00", bg="black").pack(pady=10)

root.mainloop() #GUI event loop

if 'secret_msg' not in globals(): # Default secret message
    secret_msg = ""

# Number of qubits and classical bits
n = 7
qr = QuantumRegister(n, name='qr')
cr = ClassicalRegister(n, name='cr')
qc = QuantumCircuit(qr, cr, name='QC')

alice_key = np.random.randint(0, 2**n)
alice_key = np.binary_repr(alice_key, n)
print("Alice key:", alice_key)

# Encode Alice's key onto the quantum circuit
for i in range(len(alice_key)):
    if alice_key[i] == '1':
        qc.x(qr[i])

# Alice's basis choice (H or S) and apply Hadamard gates if chosen
B = []
for i in range(len(alice_key)):
    if 0.5 < np.random.random():
        qc.h(qr[i])
        B.append("H")
    else:
        B.append("S")

qc.barrier()
print("Alice Basis:", B)
qc.draw(output='mpl')
plt.show()

# Bob's basis choice (H or S)
C = []
for i in range(len(alice_key)):
    if 0.5 < np.random.random():
        qc.h(qr[i])
        C.append("H")
    else:
        C.append("S")

qc.barrier()
for i in range(len(alice_key)):
    qc.measure(qr[i], cr[i])

print("Bob Basis:", C)
qc.draw(output='mpl')
plt.show()

# Simulate the quantum circuit
simulator = AerSimulator()
compiled_circuit = transpile(qc, backend=simulator)
job = simulator.run(compiled_circuit)
result = job.result()
counts = result.get_counts(qc)
bob_key = list(counts.keys())[0]
print("Bob key:", bob_key)
print("Bob Basis:", C)

# Sift the key based on matching bases
def sifted_key(A_basis, B_basis, key):
    correct_basis = []
    sifted_key = ''
    for i in range(len(A_basis)):
        if A_basis[i] == B_basis[i]:
            correct_basis.append(i)
            sifted_key += key[i]
    return sifted_key, correct_basis

sifted = sifted_key(B, C, alice_key)
BB84_key = sifted[0]
print("Sifted key:", BB84_key)
print("Basis:", sifted[1])

# Encrypt a single character with the BB84 key
def encrypt(BB84_key, letter):
    b = int(BB84_key, 2)
    x = ord(letter)
    return format(b ^ x, "07b")

#Encode encrypted message into a carrier message
def stega_encoder(LM, carrier_msg):
    message = ""
    i = 0
    for bitstring in LM:
        for digit in bitstring:
            while i < len(carrier_msg) and not carrier_msg[i].isalpha():
                message += carrier_msg[i]
                i += 1
            if i < len(carrier_msg):
                if digit == "1":
                    message += carrier_msg[i].upper()
                else:
                    message += carrier_msg[i]
                i += 1
    if i < len(carrier_msg):
        message += carrier_msg[i:]
    return message

L = [encrypt(BB84_key, c) for c in secret_msg]
carrier_msg = ''.join(random.choice(string.ascii_lowercase) for _ in range(len(secret_msg) * 20)) # Ensure the carrier message has enough length
encrypted_message = stega_encoder(L, carrier_msg) # Encode the encrypted message into the carrier message
[ws.Beep(2000, 100) for _ in range(3)]
print("New carrier message:", encrypted_message)

if __name__ == "__main__":
    print("Encrypted message:", encrypted_message)
    print("BB84 key:", BB84_key)