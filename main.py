#!pip install mediapipe opencv-python
#!pip install tkintertable
#pip install numpy

import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import *
from typing import Text, get_type_hints
from gtts import gTTS
import os
from playsound import playsound



def calculate_angle(a,b,c):                 #using numpy calculate angle between 3 vectors
    a = np.array(a)                         #first point
    b = np.array(b)                         #mid  point   
    c = np.array(c)                         #End point 
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0 :
        angle = 360-angle
    
    return angle

def bicepCurl():
    cap = cv2.VideoCapture(0)     # 0 represents webcam

    #Curls Counter variables
    counter = 0
    stage =None
    playsound('letsgo.mp3')


    with mp_pose.Pose(min_detection_confidence=0.8,min_tracking_confidence=0.8) as pose:  # setup mediapipe instance
        while cap.isOpened():     # taking current feed from webcam
            ret, frame = cap.read() # ret is return variable frame is going to give img from the web cam
    
            #Detect stuff and render it 
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)#recoloring img
            image.flags.writeable = False
    
            #make detection
            results = pose.process(image)
    
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)# recoloring it back to bgr
        
            #extracting landmarks due to some cam issues if landmark not detected then pass
            try:
                landmarks = results.pose_landmarks.landmark
            
                #getting coordinates
                shoulder =[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow =[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,]
                wrist =[landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,]
            
                #calculate angle
                angle = calculate_angle(shoulder,elbow,wrist)
            
                #visualize angle
                cv2.putText( image, str(angle),
                            tuple(np.multiply(elbow, [640, 480]).astype(int)),        #this will give coordinates accounding to the size of the image
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA
                           )
            
                # Curl counter logic
                if angle > 160:
                    if(stage == 'up'):
                        playsound('go_up.mp3',False)
                    stage = 'down'                   #flag
                    
                if angle < 30 and stage == 'down':
                    if(stage == 'down'):
                        playsound('go_down.mp3',False)
                    stage='up'
                    counter += 1
                    print(counter)
                
            
            except:
                pass
        
            #render curl counter
            #setup status box
            cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
            #rep data
            cv2.putText(image, 'REPS', (15,12),
                       cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,0), 1,cv2.LINE_AA)
            cv2.putText(image, str(counter),(10,60),
                      cv2.FONT_HERSHEY_SIMPLEX, 2,(255,255,255), 2, cv2.LINE_AA)
        
           #STage data
            cv2.putText(image, 'STAGE', (65,12),
                       cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,0), 1,cv2.LINE_AA)
            cv2.putText(image, stage,(60,60),
                      cv2.FONT_HERSHEY_SIMPLEX, 2,(255,255,255), 2, cv2.LINE_AA)
        
        
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))
            #this are the specfication for drawing camponent with color thickness and circle radius first line for join and second for connection
        
        
            cv2.imshow("Mediapipe Feed", image) #this will visualize it 
    
            if cv2.waitKey(10) & 0xFF == ord('q'): # q will closedown the feed
                break  # to stop the while loop ig webcam
        

    cap.release()            # this 2 lines will break the video cam
    cv2.destroyAllWindows()   # ig close down video feed



def shoulderPress():
    cap = cv2.VideoCapture(0)     # 0 represents webcam

    #Curls Counter variables
    counter = 0
    stage =None
    playsound('letsgo_1.mp3')


    with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:  # setup mediapipe instance
        while cap.isOpened():     # taking current feed from webcam
            ret, frame = cap.read() # ret is return variable frame is going to give img from the web cam
    
            #Detect stuff and render it 
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)#recoloring img
            image.flags.writeable = False
    
            #make detection
            results = pose.process(image)
    
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)# recoloring it back to bgr
        
            #extracting landmarks due to some cam issues if landmark not detected then pass
            try:
                landmarks = results.pose_landmarks.landmark
                #getting coordinates
                shoulder =[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow =[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,]
                wrist =[landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,]              
                #calculate angle
                angle = calculate_angle(shoulder,elbow,wrist)
                #visualize angle
                cv2.putText( image, str(angle),
                            tuple(np.multiply(elbow, [640, 480]).astype(int)),        #this will give coordinates accounding to the size of the image
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA
                           )
                # Curl counter logic
                if angle < 100:
                    if(stage=='up'):
                        playsound('go_up.mp3',False)
                    stage = 'down'
                if angle > 165 and stage == 'down':
                    if(stage=='down'):
                        playsound('go_down.mp3',False)
                    stage='up'
                    counter += 1
                    print(counter)
                
            
            except:
                pass
        
            #render curl counter
            #setup status box
            cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
            #rep data
            cv2.putText(image, 'REPS', (15,12),
                       cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,0), 1,cv2.LINE_AA)
            cv2.putText(image, str(counter),(10,60),
                      cv2.FONT_HERSHEY_SIMPLEX, 2,(255,255,255), 2, cv2.LINE_AA)
        
           #STage data
            cv2.putText(image, 'STAGE', (65,12),
                       cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,0), 1,cv2.LINE_AA)
            cv2.putText(image, stage,(60,60),
                      cv2.FONT_HERSHEY_SIMPLEX, 2,(255,255,255), 2, cv2.LINE_AA)
        
        
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))
            #this are the specfication for drawing camponent with color thickness and circle radius first line for join and second for connection
        
        
            cv2.imshow("Mediapipe Feed", image) #this will visualize it 
    
            if cv2.waitKey(10) & 0xFF == ord('q'): # q will closedown the feed
                break  # to stop the while loop ig webcam
        

    cap.release()            # this 2 lines will break the video cam
    cv2.destroyAllWindows()   # ig close down video feed



def squats():
    cap = cv2.VideoCapture(0)     # 0 represents webcam

    #Curls Counter variables
    counter = 0
    stage =None


    with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:  # setup mediapipe instance
        while cap.isOpened():     # taking current feed from webcam
            ret, frame = cap.read() # ret is return variable frame is going to give img from the web cam
    
            #Detect stuff and render it 
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)#recoloring img
            image.flags.writeable = False
    
            #make detection
            results = pose.process(image)
    
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)# recoloring it back to bgr
        
            #extracting landmarks due to some cam issues if landmark not detected then pass
            try:
                #extra added for getting coordinates for squat
                hip =[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee =[landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y,]
                ankle =[landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y,]
                #extra for calculating angl
                angle = calculate_angle(hip,knee,ankle)
                #visualize angle
                cv2.putText( image, str(angle),
                            tuple(np.multiply(elbow, [640, 480]).astype(int)),        #this will give coordinates accounding to the size of the image
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA
                           )
                #squat counter logic
                if angle > 165 :
                    stage = 'up'
                if angle < 97 and stage == "up":
                    stage = 'down'
                    counter += 1
                    print(counter)
                
            
            except:
                pass
        
            #render curl counter
            #setup status box
            cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
            #rep data
            cv2.putText(image, 'REPS', (15,12),
                       cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,0), 1,cv2.LINE_AA)
            cv2.putText(image, str(counter),(10,60),
                      cv2.FONT_HERSHEY_SIMPLEX, 2,(255,255,255), 2, cv2.LINE_AA)
        
           #STage data
            cv2.putText(image, 'STAGE', (65,12),
                       cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,0), 1,cv2.LINE_AA)
            cv2.putText(image, stage,(60,60),
                      cv2.FONT_HERSHEY_SIMPLEX, 2,(255,255,255), 2, cv2.LINE_AA)
        
        
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))
            #this are the specfication for drawing camponent with color thickness and circle radius first line for join and second for connection
        
        
            cv2.imshow("Mediapipe Feed", image) #this will visualize it 
    
            if cv2.waitKey(10) & 0xFF == ord('q'): # q will closedown the feed
                break  # to stop the while loop ig webcam
    
    cap.release()            # this 2 lines will break the video cam
    cv2.destroyAllWindows()   # ig close down video feed




def clear_values():
    list_of_numbers.clear()
    e.delete(0,END)


def var_states():
   print("male: %d,\nfemale: %d\n" % (var1.get(), var2.get()))


#var1.get() is male boolean var2.get()female boolean var3.get() is fatloss boolean and var4.get() is musclegain
#drop down code
# Change the label text
def show():
    label.config( text = clicked.get() )

    
#e1.get() is weight e2.get() is height e3.get() is age
#BMR calculator
def BMR():
    weight = int(e1.get())
    height = int(e2.get())
    age = int(e3.get())
    
    #bmr or fullbedrestcals requirement
    if(var1.get() == 1):
        bmr = 66+(6.3*weight)+(12.9*height)
        bmr -= 6.8*age
    elif(var2.get() == 1):
        bmr = 65.5+(4.3*weight)+(4.7*height)
        bmr -= 4.7*age
   
    e.insert(0,"your BMR is " + str(int(bmr)))
    return bmr


    
#maintance calerios calculator    
def maincal(n):
    #maintance calerios per day
    
    weight = int(e1.get())
    height = int(e2.get())
    age = int(e3.get())
    
    #bmr or fullbedrestcals requirement
    if(var1.get() == 1):
        bmr = 66+(6.3*weight)+(12.9*height)
        bmr -= 6.8*age
    elif(var2.get() == 1):
        bmr = 65.5+(4.3*weight)+(4.7*height)
        bmr -= 4.7*age
   
    
    main_cal=0.0
    if(n == 1):
        main_cal = 1.2*bmr
    elif(n == 2):
        main_cal = 1.375*bmr
    elif(n == 3):
        main_cal = 1.55*bmr
    elif(n == 4):
        main_cal = 1.725*bmr
    elif(n == 5):
        main_cal = 1.9*bmr
    e.insert(0,"your maintance cal. are " + str(int(main_cal)) + "cals")
    return main_cal
    #print("your maintaince cal. are ",main_cal,"cals" )   


    
def my_show(*args):
    str_out.set(options.get())

    

def count_macros(main_cal):
    #n = input("press M for gain and F for fatloss  ")

    if(var4.get() == 1):
        # caL_intake = (0.9895 or 0.9958 or 1 or 1.005 or 1.010 errors in the diet allowed but note if u  do one + side do a negative also)*
        cal_intake = main_cal + 250 #do crab cycle rotate the total amount of cal_intake by carbs up fat down
        #  35% of calories from proteins. 45% of calories from carbohydrates. 20% of calories from fats
        protien_bycal = 0.35*cal_intake
        carbs_bycal = 0.45*cal_intake
        fats_bycal = 0.20*cal_intake
        #protien,carbs,fats in grams  1gm protien=4cal carbs=4 fat=9
        protien = (1/4)*protien_bycal
        carbs = (1/4)*carbs_bycal
        fats = (1/9)*fats_bycal
        e.insert(0,"Musclegain- Protien:" + str(int(protien))+"gms carbs:"+str(int(carbs))+"gm fats:"+str(int(fats))+"gm")
        #print("||yours daily macros for muscle gain Protien: ",protien,"gms carbs: ",carbs,"gms fats: ",fats,"gms||")#in application scan barcode 
        
        macros_total = [protien,carbs,fats]

    elif (var3.get() == 1):
        # caL_intake = (0.9895 or 0.9958 or 1 or 1.005 or 1.010 errors in the diet allowed but note if u  do one + side do a negative also)*
        cal_intake = main_cal - 400 #select complex carbs and good fat
        #  30% protein,  43%carbs and 27% fat.
        protien_bycal = 0.30*cal_intake
        carbs_bycal = 0.43*cal_intake
        fats_bycal = 0.27*cal_intake
        #protien,carbs,fats in grams  1gm protien=4cal carbs=4 fat=9
        protien = (1/4)*protien_bycal
        carbs = (1/4)*carbs_bycal
        fats = (1/9)*fats_bycal
        e.insert(0,"Fatloss- Protien:" + str(int(protien))+"gms carbs:"+str(int(carbs))+"gm fats:"+str(int(fats))+"gm")
        #print("||yours daily macros for Fatloss Protien: ",protien,"gms carbs: ",carbs,"gms fats: ",fats,"gms||")#in application scan barcode 
        macros_total = [protien,carbs,fats]
        
    return  macros_total
    


root = Tk()
#main_window = Tk()
mp_drawing = mp.solutions.drawing_utils     #all drawing tools from mediapipe 
mp_pose = mp.solutions.pose                 #pose estimation tools from mp

list_of_numbers=[]

#text input area
e = Entry(root, width = 40, borderwidth =5) 
e.grid(row = 15, column = 1 ,columnspan = 20,rowspan=3, padx = 50)

# Adjust size
root.geometry( "640x720" )    


Label(root, text="Your sex:").grid(row=2,column=1, sticky=W)
var1 = IntVar()
Checkbutton(root, text="male", variable=var1).grid(row=2, column=2 , sticky=W)
var2 = IntVar()
Checkbutton(root, text="female", variable=var2).grid(row=2, column=3 , sticky=W)

tk.Label(root, text="enter body weight in lbs :").grid(row=3,column=1)
tk.Label(root, text="enter height  in inches :").grid(row=4,column=1)
tk.Label(root, text="enter age  in years :").grid(row=5,column=1)


e1 = tk.Entry(root)
e2 = tk.Entry(root)
e3 = tk.Entry(root)

e1.grid(row=3, column=2)
e2.grid(row=4, column=2)
e3.grid(row=5, column=2)



Label(root, text="Your goal:").grid(row=6,column=1, sticky=W)
var3 = IntVar()
Checkbutton(root, text="fatloss", variable=var3).grid(row=6, column=2 ,sticky=W)
var4 = IntVar()
Checkbutton(root, text="musclegain", variable=var4).grid(row=6 , column=3 ,sticky=W)



Label(root, text="Select your physical activity level:").grid(row=7, column=1)

#dropdown row=7
my_list = ["little to no exercise","lightly active","moderately active","very active","extra active"]
options = tk.StringVar(root)
options.set(my_list[1]) # default value

om1 =tk.OptionMenu(root, options, *my_list)
om1.grid(row=7,column=2)

str_out=tk.StringVar(root)
str_out.set("Output")

l2 = tk.Label(root,  textvariable=str_out, width=10 )  
l2.grid(row=7,column=3) 



options.trace('w',my_show)

# Create button, it will change label text
#button = Button( root , text = "click Me" , command = show ).grid(row=6,column=0)
  
# Create Label
label = Label( root , text = "Your Output for Calculator:" )
label.grid(row=14,column=1)

Button(root, text='Quit', command=root.quit).grid(row=22,column=1, sticky=W, pady=4)
Button(root, text='Submit Info', command=var_states).grid(row=8,column=1, sticky=W, pady=4)


buttnbmr = Button(root, text='calculate BMR', padx=40 , pady=20 , command =  BMR).grid(row=9 , column =1)
if(options.get() == my_list[0]):
    n=1
if(options.get() == my_list[1]):
    n=2
if(options.get() == my_list[2]):
    n=3
if(options.get() == my_list[3]):
    n=4
if(options.get() == my_list[4]):
    n=5
buttmain =Button(root, text='Calculate maintances cal',padx=40,pady=20,command = lambda : maincal(n)).grid(row=10 , column =1)
buttnbmr = Button(root, text='calculate my macros ', padx=40 , pady=20 , command = lambda :count_macros(maincal(n))).grid(row=11 , column =1)


label = Label( root , text = "AI powered tools exercisen repetation counters :" )
label.grid(row=18,column=1)

#bottun for gui by tkinter
buttn_for_bicep = Button( root , text='Bicep curls ', padx=40 , pady=20 , command = bicepCurl ).grid(row=19 , column =1)
buttn_for_shoulder = Button( root , text='Shoulder press', padx=40 , pady=20 , command =  shoulderPress).grid(row=20 , column =1)
buttn_for_squats = Button( root , text='Squats', padx=40 , pady=20 , command = squats ).grid(row=21 , column =1)





buttn =Button(root, text='clear',padx=18,pady=9,command = clear_values).grid(row=15 , column =3)

mainloop()