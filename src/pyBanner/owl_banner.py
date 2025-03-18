import os
import time
import datetime
import platform


# Function that return a banner with an owl icon
# para=0: Toppan owl with banner 
# para=1: Gravure owl with banner 
# para=2: Toppan owl without banner
def gl_banner(para):
    para-=1
    if para not in [0, 1, 2]:
        print("[ERROR] Invalid Input. Para has been set to 0")
        para=0

    print("\n")
    seed="00080909000409490251409504612094067110920007719200086183000950930009923300095273000940940008454500080909"
    length = len(seed)

    a=["*"," "]
    b=[" ","*"]

    for i in range(13):
        
        start_index = length - 8 * (i + 1)
        end_index = length - 8 * i
        seed_cup = seed[start_index:end_index]
        sub_seed = int(seed_cup)
      
        for _ in range(4):
            emp = sub_seed % 10   
            sub_seed //= 10       
            print( a[abs(para-1)] * emp, end="")  
            star = sub_seed % 10    
            sub_seed //= 10
            print( b[abs(para-1)] * star, end="") 

        time.sleep(0.05)
        print("")  

    projectName="Project Name"
    environment="Testing"
    version="1.0"
    extra_info="Full-Stack Ninja"
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os_info = platform.platform()
    banner = f"""

-- PROGRAM INITIALIZATION --
    PROJECT      : {projectName}
    ENVIRONMENT  : {environment}
    VERSION      : {version}
    DATE & TIME  : {current_time}
    OS           : {os_info}
    INFO         : {extra_info}

"""
    if(para<=1):
      print(banner.strip())
