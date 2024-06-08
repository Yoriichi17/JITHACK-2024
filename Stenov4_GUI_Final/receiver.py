import socket
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import font
import winsound as ws

#Decode steganographic message using BB84 key
def stega_decoder(new_carrier_msg, BB84_key):
    b = int(BB84_key, 2)
    message = ""
    bitstring = ""
    for char in new_carrier_msg:
        if char.isalnum():  # Check alphanumeric 
            if char.isupper():
                bitstring += "1"
            else:
                bitstring += "0"
        if len(bitstring) == 7:
            x = int(bitstring, 2)
            message += chr(b ^ x)
            bitstring = ""
    return message.encode('ascii', errors='ignore').decode('ascii')  


#Generate and plot the quantum circuit
def generate_and_plot_circuit(alice_key, B, C):
    n = len(alice_key)
    qr = QuantumRegister(n, name="qr")
    cr = ClassicalRegister(n, name="cr")
    qc = QuantumCircuit(qr, cr, name="QC")

    for i in range(len(alice_key)):
        if alice_key[i] == "1":
            qc.x(qr[i])

# Apply Alice's basis choices
    for i in range(len(B)):
        if B[i] == "H":
            qc.h(qr[i])

    qc.barrier()

# Apply Bob's basis choices
    for i in range(len(C)):
        if C[i] == "H":
            qc.h(qr[i])

    qc.barrier()
    for i in range(len(alice_key)):
        qc.measure(qr[i], cr[i])

    print("Quantum Circuit:") 
    qc.draw(output="mpl")
    plt.show()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 1234))  
    server_socket.listen(1)
    print("Server is listening on port 1234...")

    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    full_message = conn.recv(1024).decode()
    print(f"Received message: {full_message}")

    alice_key, B, C, bb84_key, encrypted_message = full_message.split(":", 4)
    B = B.split(",")
    C = C.split(",")

    print("Alice Key:", alice_key)
    print("Alice Basis:", B)
    print("Bob Basis:", C)
    print("BB84 Key:", bb84_key)
    print("Encrypted Message:", encrypted_message)
    decoded_message = stega_decoder(encrypted_message, bb84_key)
    print("Decoded Message (before Tkinter):", decoded_message)  # Print decoded message

    window = tk.Tk()
    window.title("Decoded Message")
    window.geometry("400x100")  
    window.configure(bg="black")
    font_style = font.Font(family="Courier New", size=18,slant="italic") 
    filtered_message = ''.join(c for c in decoded_message if c.isprintable())
    message_label = tk.Label(window, text=filtered_message, wraplength=400, fg="#00FF00", bg="black", font=font_style)
    [ws.Beep(3000,100)for _ in range(3)]

    message_label.pack()
    window.mainloop()

    conn.close()
    server_socket.close()


if __name__ == "__main__":
    start_server()
