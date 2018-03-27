import time
import sys
from bluetooth import *

def setup_bluetooth():
    if sys.version < '3':
        input = raw_input
    addr = None
    len_array = 0

    if len(sys.argv) < 2:
        print("no device specified.  Searching all nearby bluetooth devices for")
        print("the Rpi_zero_server service")
    else:
        addr = sys.argv[1]
        print("Searching for Rpi_zero_server on %s" % addr)
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_matches = find_service( uuid = uuid, address = addr )
    if len(service_matches) == 0:
        print("couldn't find the Rpi_zero_server service =(")
        sys.exit(0)
    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]
    print("connecting to \"%s\" on %s" % (name, host))
    # Create the client socket
    sock=BluetoothSocket( RFCOMM )
    sock.connect((host, port))
    print("connected")
    return sock

sock = setup_bluetooth()

byte_to_send = bytes([i//250 for i in range(8000)])
print("size of byte sent")
print(len(byte_to_send))
bytearray_returned = bytearray(len(byte_to_send))
start_time = time.time()
sock.send(byte_to_send)
get_data = True
# must change this to allocated chunks
i = 0
while get_data:
    data = sock.recv(1024)
    bytearray_returned[i*1008:(i*1008) + len(data)] = data
    i += 1
    if (((i-1)*1008) + len(data)) == len(byte_to_send):
        print("data returned")
        get_data = False

end_time = time.time()
print(byte_to_send == bytearray_returned)
total_time = end_time - start_time
print("total time")
print(total_time)
speed = len(byte_to_send)/ total_time
print("speed")
print(speed/1e3)
print("kbytes/s")
sock.close()

