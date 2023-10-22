from clint.textui import colored, puts, indent
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import requests
import os
import textwrap
from dotenv import load_dotenv, dotenv_values

def main():
  """Main function"""
  load_dotenv()
  puts(colored.red("-----------------------------------------------------------------"))
  puts(colored.red("-This is a CLI Tool for Exercises created by Matthew Cheng"))
  puts(colored.red("-This CLI Tool can be used to get information about gym exercises"))
  puts(colored.red("-You can use your arrow keys and ENTER to select options"))
  puts(colored.red("-Select Help for more information"))
  puts(colored.red("----------------------------------------------------------------`-"))
  print("\n")
  selection = select()
  if selection == "Search an exercise":
    search()
  elif selection == "View list of exercises":
    print("Choose to view exercises from these muscle groups")
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
      "Help",
      Choice(value=None, name="Quit"),
    ],
    default="Search an exercise"
  ).execute()
  return selection

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

if __name__ == "__main__":
  main()