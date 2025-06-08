import zmq

context = zmq.Context()

socket_user_function = context.socket(zmq.REP)
socket_user_function.bind('tcp://*:5558')

functions = ['Choose player', 'See top 5 scorers']

try:
    while True:
        recieved = socket_user_function.recv_string()
        if recieved == "Close":
            break
        elif recieved == ('get functions'):
            socket_user_function.send_pyobj(functions)

finally:
    socket_user_function.close()
    context.term()
    print("done")