# photo_selector_with_camera.py
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import cv2
import subprocess

class PhotoSelectorApp:
    def __init__(self, root, filepath):
        self.filepath = filepath
        self.root = root
        self.cap = cv2.VideoCapture(0)  # Initialize webcam

        # Load a background image
        self.background_image = Image.open("start_bg.jpeg")  # Replace with your background image path
        self.background_image = self.background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Add background label
        self.background_label = Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Camera feed canvas
        self.camera_canvas = Canvas(self.root, width=400, height=300, bg="black")
        self.camera_canvas.grid(row=0, column=0, padx=10, pady=10)

        # Captured image display
        self.captured_image_label = Label(self.root, text="Captured Image", bg="gray", width=40, height=15)
        self.captured_image_label.grid(row=0, column=1, padx=10, pady=10)

        # Capture button
        self.capture_button = Button(self.root, text="Capture", command=self.capture_image)
        self.capture_button.grid(row=1, column=0, pady=10)

        # Proceed button
        self.proceed_button = Button(self.root, text="Proceed", command=self.submit_photo)
        self.proceed_button.grid(row=1, column=1, pady=10)

        # Start the camera feed update loop
        self.update_camera_view()

    def update_camera_view(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to an image format suitable for Tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(img)

            # Display the frame in the canvas
            self.camera_canvas.create_image(0, 0, anchor="nw", image=imgtk)
            self.camera_canvas.imgtk = imgtk  # Keep reference to avoid garbage collection

        self.root.after(10, self.update_camera_view)  # Update every 10 ms


    def close_app(self):
        self.cap.release()  # Release the webcam
        self.root.destroy()
        
    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to a PIL image
            self.captured_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Save for future use
            img = Image.fromarray(self.captured_frame)
            img.thumbnail((300, 300))  # Resize the image for the label

            # Update the captured image label
            imgtk = ImageTk.PhotoImage(img)
            self.captured_image_label.config(image=imgtk)
            self.captured_image_label.image = imgtk  # Keep reference to avoid garbage collection

    def submit_photo(self):
        # Save the captured image if it exists
        if hasattr(self, 'captured_frame'):
            img = Image.fromarray(self.captured_frame)
            img.save(f"{self.filepath}")
            self.captured_image_label.config(text="Image saved as image_1.jpg")
            self.captured_image_label.update()
        else:
            self.captured_image_label.config(text="No image to save.")
            self.captured_image_label.update()
        
        # Release the camera and close the app
        self.cap.release()
        self.root.destroy()



def create_ui(filepath):
    root = tk.Tk()
    root.title("Photo Selector for Player 1")
    root.geometry("800x600")  # Fixed size
    root.resizable(False, False)
    centre_window(root)
    app = PhotoSelectorApp(root, filepath)
    root.mainloop()

    return f"{filepath}"

def centre_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def main_screen():
    root = tk.Tk()
    root.title("Main Menu")
    root.geometry("800x600")  # Fixed size
    #root.resizable(False, False)
    centre_window(root)
    # Load a background image
    background_image = Image.open("start_bg.jpeg")  # Replace with your start screen background image path
    background_image = background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    background_photo = ImageTk.PhotoImage(background_image)

    # Add background label
    background_label = Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Add title label
    title_label = Label(root, text="Welcome to Campus Champions", font=("Comic Sans MS", 32, "bold"), fg="red")

    title_label.place(relx=0.5, rely=0.4, anchor=CENTER)
    # Create a button to start the photo selection process
    button = Button(root, text="START", font=("Segoe UI", 20), command=lambda: subprocess.run(["python", "main.py"]))
    button.place(relx=0.5, rely=0.5, anchor=CENTER)
    #button.pack()

    root.mainloop()


if __name__ == "__main__":
    main_screen()
