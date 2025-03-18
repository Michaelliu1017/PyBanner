import os
import sys
import time
import datetime
import platform
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from DemoPackage.furtune_cookie import dev_fortune_cookie
from DemoPackage.generate_emoji import generate_emoji  
from DemoPackage.owl_banner import gl_banner



def main():
   while True:
    print("________________________________________________________________________\n")
    choice = input("*** Select the function to be executed... \n\t(1: Owl Banner, 2: Fortune Cookie, 3: Generate Emoji, 4: Abort): ") or "1"
    
    try:
        choice = int(choice)
    except ValueError:
        print("[ERROR] Invalid input")
        choice = 1

    
    if choice == 4:
        print("\n************************")
        print("*  PROGRAM TERMINATED  *")
        print("************************\n")
        break  

    
    match choice:
        case 1:
            # Owl Banner
            para = int(input("\n\t🦉 Choose Your Style (1: Style A, 2: Style B, 3: Style C): ") or "3")
            gl_banner(para)

        case 2:
            # Fortune Cookie
            category = input("\n\t🔮 Choose fortune category (general, bug, debug, success): ") or "1"
            print(dev_fortune_cookie(category))

        case 3:
            # Generate Emoji
            emotion = input("\n\t😊 Enter an emotion (laugh, cry, love, etc.): ") or "happy"
            print(f"Your emoji: {generate_emoji(emotion)}")

        case _:
            print("[Invalid option] Please enter 1, 2, 3, or 4.")
    

if __name__ == "__main__":
    main()
