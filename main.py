from clint.textui import colored, puts, indent
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import requests
import os
import textwrap
import zmq
from dotenv import load_dotenv, dotenv_values

def main():
  """Main function"""
  load_dotenv()
  puts(colored.red("-----------------------------------------------------------------"))
  puts(colored.red("-This is a CLI Tool for Exercises created by Matthew Cheng"))
  puts(colored.red("-This CLI Tool can be used to get information about gym exercises"))
  puts(colored.red("-You can use your arrow keys and ENTER to select options"))
  puts(colored.red("-Select Help for more information"))
  puts(colored.red("-----------------------------------------------------------------"))
  print("\n")
  while True:
    selection = select()
    if selection == "Search an exercise":
      search()
    elif selection == "View list of exercises":
      print("Choose to view exercises from these muscle groups")
    elif selection == "Generate a random powerlifting exercise":
      with indent(4):
        puts(colored.cyan(random_exercise()))
    elif selection == "Help":
      help()
    elif selection == None:
      print("Quitting tool...")
      quit()

def select():
  """Select options"""
  selection = inquirer.select(
    message="Select an option:",
    choices=[
      "Search an exercise",
      "View list of exercises",
      "Generate a random powerlifting exercise",
      "Help",
      Choice(value=None, name="Quit"),
    ],
    default="Search an exercise"
  ).execute()
  return selection

# My partner's microservice
def random_exercise():
  """Generate a random powerlifting exercise"""
  context = zmq.Context()

  socket = context.socket(zmq.REQ)
  socket.connect("tcp://localhost:5555")

  socket.send_string("Random exercise is being generated.")
  name = "Name: " + socket.recv_string()
  return name




def search():
  """Search for an exercise by their name"""
  exercise = inquirer.text(
    message="Enter the exercise name:",
  ).execute()

  req = requests.get("https://api.api-ninjas.com/v1/exercises?name="+ exercise, headers={'X-Api-Key': f'{os.getenv("KEY")}'})
  if req.status_code == requests.codes.ok:
    res = req.json()
    for ex in res:
      name = "Exercise Name: " + ex.get("name")
      type = "Type: " + ex.get("type").capitalize()
      muscle = "Muscle: " + ex.get("muscle").capitalize()
      equipment = "Equipment: " + ex.get("equipment").capitalize()
      difficulty = "Difficulty: " + ex.get("difficulty").capitalize()
      instructions = "Instructions: " + ex.get("instructions").capitalize()
      wrapped_instructions = textwrap.wrap(instructions, width=200, initial_indent=" " * 4, subsequent_indent=" " * 4)
      with indent(4):
        puts(colored.cyan(name))
        puts(colored.cyan(type))
        puts(colored.cyan(muscle))
        puts(colored.cyan(equipment))
        puts(colored.cyan(difficulty))
      for line in wrapped_instructions:
        puts(colored.cyan(line))
      print("\n")
  else:
    puts(colored.blue(f"Error: {req.status_code} {req.text}"))

def help():
  """Displays more information about the options"""
  with indent(4):
    puts(colored.cyan("Searching for an exercise requires you to type the name of the exercise"))
    puts(colored.cyan("If the name entered matches multiple exercises, it will return all matches"))
    puts(colored.cyan("Using the search can be beneficial if you know what exercise you are looking for"))
    puts(colored.cyan("Viewing a list of exercises will bring you to another menu that will let you"))
    puts(colored.cyan("select a muscle group to view exercises from"))
    puts(colored.cyan("When you generate a random powerlifting exercise, the name of a random powerlifting exercise will be returned."))
    puts(colored.cyan("The user can then use the search function to get more details on the exercise."))

if __name__ == "__main__":
  main()