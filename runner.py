import os

command_list = [
    "python quote_validator.py",
    "python file_validator.py"
]

for i,cmd in enumerate(command_list):
    print("running", cmd)
    os.system(cmd)
    print(i+1, "completed")