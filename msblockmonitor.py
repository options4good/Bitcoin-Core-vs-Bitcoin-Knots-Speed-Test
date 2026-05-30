import zmq
import binascii
from datetime import datetime

context = zmq.Context()

# Core Subscriber
core_sub = context.socket(zmq.SUB)
# Connect using standard Linux absolute path syntax for IPC
core_sub.connect("ipc:///tmp/core.hashblock")
# Note: ZeroMQ expects the topic string exactly as sent by Bitcoin. 
# "hashblock" is the topic name, followed by the payload.
core_sub.setsockopt_string(zmq.SUBSCRIBE, "hashblock")

# Knots Subscriber
knots_sub = context.socket(zmq.SUB)
knots_sub.connect("ipc:///tmp/knots.hashblock")
knots_sub.setsockopt_string(zmq.SUBSCRIBE, "hashblock")

poller = zmq.Poller()
poller.register(core_sub, zmq.POLLIN)
poller.register(knots_sub, zmq.POLLIN)

print("Listening for ZMQ block hashes down to the millisecond...")

try:
    while True:
        socks = dict(poller.poll())
        
        if core_sub in socks:
            msg = core_sub.recv_multipart()
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            # Bitcoin ZMQ sends data in a multipart message:
            # msg[0] = topic name ("hashblock")
            # msg[1] = binary block hash (32 bytes)
            # msg[2] = block sequence number (4 bytes LE)
            block_hash = binascii.hexlify(msg[1]).decode('utf-8')
            print(f"[{timestamp}] CORE ZMQ: New Block {block_hash}")
            
        if knots_sub in socks:
            msg = knots_sub.recv_multipart()
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            block_hash = binascii.hexlify(msg[1]).decode('utf-8')
            print(f"[{timestamp}] KNOTS ZMQ: New Block {block_hash}")
            
except KeyboardInterrupt:
    print("\nClosing sockets and exiting.")
    core_sub.close()
    knots_sub.close()
    context.term()
