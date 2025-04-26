import tkinter as tk
from tkinter import Label, Button, Toplevel
import cv2
from PIL import Image, ImageTk
import threading
import time
import pyttsx3
import base64
import os
import speech_recognition as sr
from groq import Groq
import winsound  # For beep sound

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to send the image to Groq
def send_image_to_groq(image_path):
    base64_image = encode_image(image_path)

    client = Groq(api_key="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")

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "This is a picture showing a hand doing a sign in American Sign Language. Focus only on the hand and sign. What is the sign? Answer very briefly."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
    )

    return chat_completion.choices[0].message.content

# Function to speak text
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to play beep sound
def beep(frequency=1000, duration=500):
    winsound.Beep(frequency, duration)

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.configure(bg="#0B0C10")  # Dark background

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        self.label = Label(window, bg="#0B0C10")
        self.label.pack(pady=10)

        self.start_button = Button(window, text="▶ Start Capturing", width=30, height=2, 
                                   command=self.start_capture, bg="#1F2833", fg="white", font=("Arial", 12, "bold"))
        self.start_button.pack(pady=10)

        self.stop_button = Button(window, text="🛑 Stop", width=30, height=2, 
                                  command=self.stop, bg="#C3073F", fg="white", font=("Arial", 12, "bold"))
        self.stop_button.pack(pady=10)

        self.response_label = Label(window, text="", wraplength=500, font=("Arial", 16), 
                                    bg="#0B0C10", fg="#66FCF1")
        self.response_label.pack(pady=20)

        self.running = False
        self.update()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.label.configure(image=self.photo)
        self.window.after(10, self.update)

    def capture_loop(self):
        while self.running:
            beep(1200, 300)  # Beep to signal "get ready for picture"
            time.sleep(1)  # Give user time to prepare hand

            ret, frame = self.vid.read()
            if ret:
                image_path = "capture.jpg"
                cv2.imwrite(image_path, frame)

                try:
                    print("Sending image to Groq...")
                    response = send_image_to_groq(image_path)
                    print("Response:", response)

                    self.response_label.config(text="Sign Detected: " + response)
                    speak_text(response)

                    # Pause for speech input
                    self.running = False
                    self.window.after(1000, self.listen_and_display_text)
                    break  # Stop the loop temporarily

                except Exception as e:
                    print("Error:", e)
                    self.response_label.config(text="Error connecting to Groq")

            time.sleep(5)

    def listen_and_display_text(self):
        speech_window = Toplevel(self.window)
        speech_window.title("🎤 Speak Now")
        speech_window.configure(bg="#0B0C10")

        info_label = Label(speech_window, text="Listening... Please Speak!", font=("Arial", 16),
                           bg="#0B0C10", fg="#66FCF1")
        info_label.pack(pady=10)

        output_label = Label(speech_window, text="", font=("Arial", 14),
                             bg="#0B0C10", fg="white", wraplength=400)
        output_label.pack(pady=10)

        def skip_speaking():
            speech_window.destroy()
            self.running = True
            threading.Thread(target=self.capture_loop).start()

        skip_button = Button(speech_window, text="Skip Speaking 🏃", command=skip_speaking,
                             bg="#45A29E", fg="white", font=("Arial", 12, "bold"))
        skip_button.pack(pady=10)

        beep(800, 500)  # Beep to signal start speaking

        def listen_now():
            recognizer = sr.Recognizer()
            mic = sr.Microphone()

            try:
                with mic as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)

                output_label.config(text=f"You said:\n{text}")

            except sr.UnknownValueError:
                output_label.config(text="Sorry, could not understand the audio.")
            except sr.RequestError:
                output_label.config(text="Could not request results from Google.")
            except Exception as e:
                output_label.config(text=f"Error: {str(e)}")

            # After showing the result, wait then continue
            def resume_capture():
                speech_window.destroy()
                self.running = True
                threading.Thread(target=self.capture_loop).start()

            speech_window.after(4000, resume_capture)

        threading.Thread(target=listen_now).start()

    def start_capture(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.capture_loop).start()

    def stop(self):
        self.running = False

    def on_closing(self):
        self.running = False
        self.vid.release()
        self.window.destroy()

if __name__ == "__main__":
    App(tk.Tk(), "🤟 ASL Sign Recognizer + Voice Conversation - Powered by Groq AI")
