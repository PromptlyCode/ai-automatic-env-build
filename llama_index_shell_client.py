import socketio

# Create a Socket.IO client
sio = socketio.Client()

# Define event handlers
@sio.event
def connect():
    print('Connected to server')
    sio.send("connect")

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.event
def message(data):
    print('Message from server: ', data)

# Connect to the server
sio.connect('http://localhost:6000')

# Allow for multiple chat messages
try:
    while True:
        # the client need can input mutil chat message in terminal
        # q: Execute the installation command npm install. If successful, it will return to npm list. If it fails, it will return to node -v.
        message = input("Enter a message: ")
        if message:
            sio.send(message)
        else:
            sio.send("not-empty")
except KeyboardInterrupt:
    print("Exiting...")

# Wait for responses
sio.wait()

