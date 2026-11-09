import subprocess

def play_mp3(filename):

    player = subprocess.Popen(["mpg123" , filename, "-q"],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    

    player.communicate(input=b'q')
 

japan = "japan"
Taiwan="taiwan"
China="china"
Vietnam="vietnam"

for i in range(100):
    user_input = input("Pick a Country: ").lower()
    if user_input == japan:
        print("To Japan we go")        
        play_mp3("/home/pi/Downloads/Test.mp3")
    elif user_input == China:
            print("To China we go")        
            play_mp3("/home/pi/Downloads/China.mp3")
    elif user_input == Taiwan:
            print("To Taiwan we go")        
            play_mp3("/home/pi/Downloads/Taiwan.mp3")
    elif user_input == Vietnam:
            print("To Vietnam we go")        
            play_mp3("/home/pi/Downloads/Vietnam.mp3")

    else:
        print("Sorry, we don't operate in that country just yet")


