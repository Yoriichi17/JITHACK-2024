import socket
import quantum_stenography
def send_message(alice_key, B, C, message, bb84_key):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP/IP socket
    client_socket.connect(('192.168.249.72', 1234))
    
    full_message = f"{alice_key}:{','.join(B)}:{','.join(C)}:{bb84_key}:{message}"
    client_socket.sendall(full_message.encode())
    client_socket.close()

if __name__ == "__main__":
    message = quantum_stenography.encrypted_message
    bb84_key = quantum_stenography.BB84_key
    alice_key = quantum_stenography.alice_key
    B = quantum_stenography.B
    C = quantum_stenography.C
    print("Encrypted message:", message)
    print("BB84 key:", bb84_key)
    send_message(alice_key, B, C, message, bb84_key)