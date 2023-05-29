import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import requests
from bs4 import BeautifulSoup
from ultralytics import YOLO
import pyttsx3 
from gtts import gTTS
from io import BytesIO
import playsound
import os


class RealTimePredictionTranslation:

    def __init__(self):

        #initiate main window
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.configure(background="grey")
        self.root.minsize(1100, 1100)
        self.root.maxsize(2000, 2000)
        self.root.geometry("300x300+50+50")
        self.root.title("Real Time Prediction and Translation")
        self.root.configure(bd=5)
        
        self.image = Image.open("pexel.jpg")
        self.photo = ImageTk.PhotoImage(self.image)
        self.background_label = tk.Label(self.root, image=self.photo)
        self.background_label.pack(fill=tk.BOTH, expand=True)

        #variable to get input string from user via GUI
        self.variable = tk.StringVar(self.root)

        # define camera variable and
        # initiate yolo model
        self.camera = None
        self.model = YOLO('yolov8n.pt')
        

        #initialize additional frame and button
        self.define_language()
        self.initiate_detect_frame()
        self.initiate_trans_frame()
        self.initiate_buttons()
        self.initiate_cam_widget()
        self.initiate_image_widget()
        self.define_detect_widget()
        self.define_trans_widget()
        

        # initiate text widget to render detection 
        # and translation on the GUI 
        self.text_widget1 = self.define_trans_widget()
        self.text_widget =  self.define_detect_widget()
        

        # Start the Tkinter event loop
        #self.root.mainloop()
        self.engine = pyttsx3.init()

        # Configure the properties of the TTS engine (optional)
        self.engine.setProperty('rate', 188)  # Speed of speech (words per minute)
        self.engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)


        self.mp_fp = BytesIO()
        self.word = "Default value"
        

 
    def run(self):
        self.root.mainloop()


    def speak(self, text, lan='en'):
        tts = gTTS(text=text, lang=lan)

        filename = "abc.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)

        
    ############ Add frame to handle text ################
    # Create a frame to display the text

    # Function to convert text to sound
    def text_to_speech(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def define_frame(self, x, y):

        """
        Template to create frame

        """

        frame= tk.Frame(self.root)
        frame.configure(
        highlightbackground="lightgreen",  # Border color
        highlightthickness=5  # Border thickness
        )
        frame.place(x=x,y=y)
        #frame.pack()

        return frame
    
    def initiate_detect_frame(self):

        """
        Initiate frame to display detected object label on GUI

        """

        detection_frame = self.define_frame(3, 540)

        return detection_frame
    
    def initiate_trans_frame(self):

        """
        Initiate frame to display translated label on GUI

        """

        translate_frame = self.define_frame(548, 540)

        return translate_frame

    
    def define_detect_widget(self):

        """
        Initiate Text widget inside the frame to display label of detected object
        """

        #Text widget for detection

        frame = self.initiate_detect_frame()

        text_widget = tk.Text(frame, width=48, height=19.47, font=("Arial", 16), background= "black", foreground= "orange")
        text_widget.pack()

        return text_widget
    
    def define_trans_widget(self):

        """
        Initiate Text widget inside frame to display translated label

        """

        #Text widget for translation
        frame1 = self.initiate_trans_frame()

        text_widget1= tk.Text(frame1, width=48, height=19.47, font=("Arial", 16), background="black", foreground="skyblue")
        text_widget1.pack()

        return text_widget1
      
    
    def label_widgets(self, x, y, width, height, back_col, high_col):

        """
        template to create Label widget

        """

        label_widget = tk.Label(self.root)
        #label_widget.pack() # if you pack before initiate the label widget nothin is display on the main frame
        label_widget.place(x=x, y=y, width=width, height=height)
        label_widget.configure(background=back_col, highlightbackground=high_col, highlightthickness=5)

        return label_widget

    def initiate_cam_widget(self):

        """
        function to initiate widget to store camera stream

        """

        # label widget to display camera
        label_widget = self.label_widgets(435, 0, 650, 500, "white", "lightgreen")

        #return label_widget,

        return label_widget
    
    def initiate_image_widget(self):

        """
        function to create widget inside the second frame to store image 
        image is displayed on the left upper corner of the GUI

        """

        # Add the additional frame
        
        lab_widget = self.label_widgets(10, 80, 350, 410, "skyblue", "skyblue")
        
        ####### Add second image to the frame ##########
        # Load the image for the additional frame
        im = Image.open("funny.jpg")
        resize_im = im.resize((350, 410), Image.LANCZOS)
        # Convert the PIL Image to a Tkinter PhotoImage
        self.ph = ImageTk.PhotoImage(resize_im)
        
        lab_widget.configure(image=self.ph)

        #return lab_widget

        return lab_widget
        

    def define_language(self):

        """
        function to initiate option menu for language selection
        user can select a language in which object label is translated

        """

        # Select language
        OPTIONS = ["Spanish", "French", "Italian", "Portuguese", "German"] #["es", "fr","it", "pt", "de", ]

        # Configure the style for the OptionMenu widget

        style = ttk.Style()
        style.configure("Custom.TMenubutton", font=("Arial", 16), relief="flat", borderwidth=0)

        #Create Option menu Button
        #global variable

        #variable = tk.StringVar(self.root)
        self.variable.set(OPTIONS[4]) # default value
        
        option_menu_widget = tk.OptionMenu(self.root, self.variable, *OPTIONS)
        #option_menu_widget.pack()

        ## Define the font for the options

        option_menu_widget.config(height=1, width=13, font=("Arial", 14), background="darkblue", foreground="orange", relief="raised")

        option_menu_widget.place(x=2, y=0)

        # Access the menu widget
        menu = option_menu_widget.nametowidget(option_menu_widget.menuname)

        # Configure the size of the options in the scrolling list
        menu.config(font=("Arial", 14))  # Set the font size to 12 

        
    # create button to get the choice of the users 
    def submit_lang(self):
        
        """
        function allows user to submit selected value through GUI
        return value selected by user
        """

        #variable = self.define_language()
        lani=''
        lang = self.variable.get()
        lan = ["Spanish", "French", "Italian", "Portuguese", "German"] 
        ln = ["es", "fr","it", "pt", "de", ]
        for i, item in enumerate(lan):
            if item == lang:
                lani=ln[i]
            
        #print("value is:" + lan)
        return lani 
      

    # Function to update the text in the frame
    def update_text(self, txt="Hello, World!"):

        """ 
        function updates text displayed on the GUI
        show 5 lines of text and update everytime with the most recent post
        5 most recents post are displayed on the GUI interface
        
        """
        # text_widget = self.define_detect_widget()
        # Retrieve text from another script or source
        text = txt
        
        # Get the current content of the Text widget
        current_content = self.text_widget.get("1.0", tk.END)

        # Split the content into separate lines
        lines = current_content.split("\n")

        # If there are already 5 lines, remove the first line
        if len(lines) >= 5:
            lines.pop(0)

        # Append the new text as a new line
        lines.append(text)

        # Join the lines back together
        updated_content = "\n".join(lines)

        # Clear the existing content in the Text widget
        self.text_widget.delete("1.0", tk.END)

        # Insert the updated text into the Text widget
        self.text_widget.insert(tk.END, updated_content)
        
    # Function to scrape definition from wordreference
    def scrap_trans(self, word):
        
        """
        function scrapes through wordreference
        requests translation from english to selected language
        Args: word to be translated
        return the translation
        
        """

        text = word
        translation=""
        
        # translate language 
        SOURCE_LANG = 'en'
        TARGET_LANG = self.submit_lang() #take the option selected by user through GUI
        
        print(f"Now translated in {TARGET_LANG}")
        
        # Pass the word to the WordReference API and get the translation page
        url = f'http://www.wordreference.com/{SOURCE_LANG}{TARGET_LANG}/{text}'
            
        # Make a query for translation
        response = requests.get(url)
        print(response.status_code)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the translation of the word
        translation = soup.find("tr", class_="even")
        if translation:
            text=translation.get_text()
        else:
            text=f"Translation not found"

        
        return text
    

        
    # Function to update translation on screen
    def update_trans(self, txt="Hello, World!"):

        """
        function update the last five translated words on GUI interface 
        
        """

        #text_widget1 = self.define_trans_widget()
        # Retrieve text from another script or source
        text = f"{txt}"
        
        # Get the current content of the Text widget
        current_content = self.text_widget1.get("1.0", tk.END)

        # Split the content into separate lines
        lines = current_content.split("\n")

        # If there are already 5 lines, remove the first line
        if len(lines) >= 5:
            lines.pop(0)

        # Append the new text as a new line
        lines.append(text)

        # Join the lines back together
        updated_content = "\n".join(lines)

        # Clear the existing content in the Text widget
        self.text_widget1.delete("1.0", tk.END)

        # Insert the updated text into the Text widget
        self.text_widget1.insert(tk.END, updated_content)

        
    #### Handling Camera #################

    def start_stream(self):
        """
        function to start the camera 
        run yolo model
        """
        self.camera = cv2.VideoCapture(0)
        self.update_frame()

    def stop_stream(self):

        """
        function to stop the stream of the camera

        """

        if self.camera is not None:
            self.camera.release()

    def refresh_stream(self):
        """
        function to refresh the camera stream
        """
        self.stop_stream()
        self.start_stream()


    def update_frame(self):

        """
        function 
        - reads stream from camera 
        - transform to Image 
        - made prediction of objects on the image with yolo8 model
        - request translation of the detected objects 
        - update translation on GUI
        
        """
        
        
        label_widget = self.initiate_cam_widget()

        #global camera
        if self.camera is not None:

            _, frame = self.camera.read()  # Read a frame from the camera

        
            img = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA) # convert image color
            
            cam_image = Image.fromarray(img)  # Convert the image to PIL format
            
            results = self.model(cam_image) # Run the image in YOLO
            list_ob =[]
            rand_name =""
            for r in results:
                for z, _ in enumerate(r):
                    self.word = f"The detected Object {z} is {self.model.names[int(r.boxes.cls[z])]} with {round (float(r.boxes.conf[z]), 2)} confidence"
        
                   
                    #update label of the detected object on the screen
                    self.update_text(self.word)
                    obj_name = self.model.names[int(r.boxes.cls[z])]
                    
                    if obj_name != rand_name:
                        t = self.scrap_trans(obj_name) # requests translation of the detected object
                        self.update_trans(t) # update translation on GUI
                        rand_name = obj_name
                    #self.speak(word, self.submit_lang)
                    
                    #append label of detected object in a list
                    list_ob.append(obj_name)
            
                res_plot = r.plot()
                
                # Create a Tkinter-compatible image
                pict = ImageTk.PhotoImage(image=Image.fromarray(res_plot))  
            
                # Displaying photoimage in the label
                label_widget.pict = pict

                # Configure image in the label
                label_widget.configure(image=pict)
                
            # Remove duplicate from the list of detected object
            list_ob = list(dict.fromkeys(list_ob))
            #for n in list_ob:

                #self.text_to_speech(f"{n} is detected")
                
                #t = self.scrap_trans(n) # requests translation of the detected object
                #print(t)
                #self.update_trans(t) # update translation on GUI

                #time.sleep(1)
            #    print("ööö")
                
            # Schedule the next frame update
            label_widget.after(40, self.update_frame)

            return list_ob
        
    def initiate_audio(self):

        #list_obj = self.update_frame()
        #lan = self.submit_lang()
             
        #for item in list_obj:
        #    text = f"{item} is detected"
        text = self.word
        self.speak(text)
        

    def create_button(self, title, width, height, x, y, command):

        """
        
        template to create button

        """

        button = tk.Button(self.root, text=title, width=width, height=height, command=command)
        button.configure(background="darkblue", foreground="orange", font=("Arial", 14))
        button.place(x=x, y=y)
        #button.pack()

        return button
        
    # Function to quit the main window
    def quit_window(self):

        """
        function allows the graphical user interface to quit
        """
        self.root.quit()


    def initiate_buttons(self):
        
        """
        function initiate the GUI button

        """
        
        submit_button = self.create_button("Submit Selection", 16, 1, 180, 0, command=self.submit_lang())

        quit_button = self.create_button("Quit", 18, 1, 780, 960, command=self.quit_window)

        open_camera_button = self.create_button("Open Camera", 20, 1, 650, 503, command=self.start_stream)

        stop_button = self.create_button("Stop Camera", 20, 1, 430, 960, command=self.stop_stream)

        refresh_camera_button = self.create_button("Refresh Camera", 18, 1, 90, 960, command=self.refresh_stream)

        play_audio = self.create_button("Play audio", 18,1, 90, 503, command=self.initiate_audio)

        
# run the script if the program is called

if __name__ == "__main__":
    real_time_detection1 = RealTimePredictionTranslation()
    real_time_detection1.run()


