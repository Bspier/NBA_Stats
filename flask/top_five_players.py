import zmq
context =zmq.Context()
socket_top_five = context.socket(zmq.REP)
socket_top_five.bind("tcp://*:5559")

try:
    while True:
        received = socket_top_five.recv_pyobj()
        if received == ["Close"]:
            break
        
        errorMSG = 'Invalid Request'

        if received is None:
            socket_top_five.send_string(errorMSG)
            continue

        if not isinstance(received[0],str) or not isinstance(received[1], dict):
            socket_top_five.send_string(errorMSG)
            continue

        stat = received[0]
        data = received[1]
        statIndex = None
        response = f' TOP 5 IN {stat}  \n'

        for i in range(len(data['resultSet']['headers'])):
            if data['resultSet']['headers'][i] == stat:
                statIndex = i

        player = data['resultSet']['rowSet']
        for i in range(5):
            response += f'{i+1}. {player[i][2]}: {player[i][statIndex]}' + "\n"
        socket_top_five.send_string(response)

finally:
    socket_top_five.close()
    context.term()
  