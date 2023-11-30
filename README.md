**Exercises Command Line Interface Tool**

This CLI Tool can be used to get more information on various exercises.
The user can generate a random powerlifting exercise, search for them, and browse for them.

Communication Contract:
1) Install zmq with Python, dotenv, InquirerPy, clint
2) Import time, zmq, requests, os, random, textwrap
3) To request data from the microservice:
* context = zmq.Context()
* socket = context.socket(zmq.REP)
* socket.bind("tcp://*:5555")
* socket.send_string("Random exercise is being generated.")
4) To receive data from the microservice:
* socket.send_string(exercise_data.get("name"))

![image](https://github.com/mattcheng591/exercise-cli-tool/assets/105122660/5be7590d-e558-44da-b320-976de1be86c4)

