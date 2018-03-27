import time
from bluetooth import *

def advertise_server(name_server):
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)
    port = server_sock.getsockname()[1]
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    advertise_service( server_sock, name_server,
                       service_id = uuid)
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)
    return client_sock, server_sock

client_sock, server_sock = advertise_server("Rpi_zero_server")
a = bytearray(8000)
get_data = True
i = 0
while get_data:
    data=client_sock.recv(1024)
    a[i*1008:(i*1008) + len(data)] = data
    i += 1
    if (((i-1)*1008) + len(data)) == 8000:
        client_sock.send(bytes(a))
        print("sent")
        get_data = False
print("recieved data")
client_sock.close()
server_sock.close()
