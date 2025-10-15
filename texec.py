#!/usr/bin/python

import signal, os
from timeit import default_timer as timer
from subprocess import run as execute

# For graceful exit, breaks some loops without this
def handler(signum, frame):
  os._exit(os.EX_OK)

def get_time_limit():
  print("Write time limit as seconds for checking:")

  while True:
    try:
      limit = float(input())

      if limit <= 0:
        print("Write a value higher than 0.")
        continue

      return limit
    except:
      print("Write a valid integer/float.")
      continue

def get_inputs():
  print("Write a existed directory name for inputs, retrieves all .txt files as input:")

  while True:
    inputs = input()

    if not os.path.exists(inputs):
      print("Write a directory path that is existed.")
      continue

    return inputs

def get_command():
  print("Write command will be executed:")
  return input()

def get_redaction():
  print("Write \"yes\" if you want to redact output, otherwise write \"no\":")

  while True:
    decision = input()

    if decision == "yes":
      return True
    elif decision == "no":
      return False
    else:
      print("Please write \"yes\" or \"no\".")

if __name__ == "__main__":
  signal.signal(signal.SIGINT, handler)

  limit = get_time_limit()
  inputs = get_inputs()
  command = get_command()
  redaction = get_redaction()

  elapsed_count = 0
  error_count = 0
  count = 0

  with os.scandir(inputs) as entries:
    for entry in entries:
      if not entry.is_file() or not entry.name.endswith(".txt"):
        continue

      count += 1

      with open(entry.path) as input_file:
        try:
          start = timer()

          res = execute(
            [command],
            input = input_file.read(),
            capture_output=True,
            text=True,
            check=True
          )

          end = timer()

          elapsed = (end - start)

          if redaction:
            print(f"{entry.name[:-4]} => elapsed {(end - start):.2f} seconds")
          else:
            print(f"{entry.name[:-4]} => elapsed {(end - start):.2f} seconds\n{res.stdout}\n")

          if elapsed > limit:
            print(f"execution time of {entry.name[:-4]} is exceeded time limit")
            elapsed_count += 1

        except:
          print(f"There is a program error for {entry.name}")
          error_count += 1

  print(f"\nPassed {count - error_count - elapsed_count} testcases, {elapsed_count} time limit exceeded, {error_count} throwed error.")
  print(f"{count - error_count - elapsed_count} / {count}")
