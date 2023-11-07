import time
import zmq
import requests
import os
import random
from clint.textui import colored, puts, indent
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from dotenv import load_dotenv, dotenv_values

load_dotenv()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    # Waiting to receive the request
    message = socket.recv()
    print("Received request: %s" % message)
    exercises = []
    time.sleep(1)

    response = requests.get("https://api.api-ninjas.com/v1/exercises?type=powerlifting", headers={'X-Api-Key': f'{os.getenv("KEY")}'})
    if response.status_code == requests.codes.ok:
      result = response.json()
      for exercise in result:
          exercises.append(exercise)

      num = random.randint(0, len(exercises))
      exercise_data = exercises[num]

      # Name of exercise sent back
      socket.send_string(exercise_data.get("name"))

    else:
       puts(colored.blue(f"Error: {response.status_code} {response.text}"))

