# Main Functions to handle installing and running errors
# LDB Errors will be handled in the main files
# last edit: 21.04.2018 (callFEELD)

import sys, time                    # used to handle errors

# function to handle errors
def error(error):
    print('[i]  [status]        ERROR')
    print("     [error type]        "+str(error))
    if error == 1:
        print("     [error msg]         Missing files to run the bot. Make sure you installed everything correct.")

    elif error == 2:
        print("     [error msg]         Couldn't read the token. Please insert the token into the token.json file.")

    elif error == 3:
        print("     [error msg]         Critical Error! Maybe wrong Token!")


    time.sleep(5)
    sys.exit()