from run import *

while True:
    text = input("jinba: ")
    result, error = run("<stdinfile>", text)

    if error:
        print(error.as_string())
    else:
        print(result)
