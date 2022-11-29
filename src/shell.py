from run import *

while True:
    text = input("jinjax: ")
    result, error = run("<stdinfile>", text)

    if error:
        print(error.as_string())
    else:
        print(result)
