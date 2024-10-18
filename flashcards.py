import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import random
from gtts import gTTS
from gtts.lang import tts_langs
import playsound
from PIL import Image, ImageTk
import threading
import time
import tempfile
import tkinter.font as tkFont

class FlashcardApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Language Flashcards")
        self.master.geometry("800x600")

        # Use Helvetica font for general text
        self.font_name = 'Helvetica'
        # Use Didot font for English text on flashcards
        self.english_font_name = 'Didot'
        # Use pixelated font for buttons
        self.pixel_font_name = 'Press Start 2P'

        # Register the custom font
        self.register_custom_font()

        self.phrases = {}
        self.progress = {}
        self.current_phrase = None
        self.mode = None  # No default mode
        self.show_count = 0  # To track how many times "Show Answer" is pressed

        # Initialize TTS variables
        self.tts_language_code = None
        self.language_supported = True  # Flag to check if TTS is supported

        # Load sound effects (Optional)
        self.load_sound_effects()

        # Initialize progress variables
        self.total_phrases = 0
        self.correct_answers = 0

        # Added to keep track of cards in current session
        self.session_phrases = []

        # Added to track if a language is loaded
        self.language_loaded = False
        self.greetings = ["Hello!"]

        self.create_main_menu()

    def register_custom_font(self):
        # Path to the font file
        font_path = os.path.join('fonts', 'PressStart2P.ttf')
        if os.path.exists(font_path):
            try:
                tkFont.Font(font=(self.pixel_font_name, 12))
                self.master.option_add("*Font", (self.pixel_font_name, 12))
            except Exception as e:
                messagebox.showerror(
                    "Font Error",
                    f"An error occurred while loading the custom font:\n{e}"
                )
                self.pixel_font_name = self.font_name  # Fallback to default font
        else:
            # Font file not found, fallback to default font
            self.pixel_font_name = self.font_name

    def load_sound_effects(self):
        # Dictionary to store sound file paths
        self.sounds = {
            'click': 'sounds/click.mp3',
            'correct': 'sounds/correct.mp3',
            'incorrect': 'sounds/incorrect.mp3',
            'show': 'sounds/show.mp3',
            'back': 'sounds/back.mp3'
        }
        # Ensure the sounds directory exists
        if not os.path.exists('sounds'):
            os.makedirs('sounds')

    def play_sound(self, sound_name):
        # Play sound in a separate thread to avoid blocking
        def _play():
            sound_file = self.sounds.get(sound_name)
            if sound_file and os.path.exists(sound_file):
                playsound.playsound(sound_file)
        threading.Thread(target=_play).start()

    def create_main_menu(self):
        self.main_menu_frame = tk.Frame(self.master)
        self.main_menu_frame.pack(fill='both', expand=True)

        # Unified Language Button/Indicator at Top-Right
        self.language_button = tk.Button(
            self.main_menu_frame,
            text="No Language Loaded",
            bg='red',
            fg='white',
            font=(self.pixel_font_name, 12),
            command=self.load_language_file
        )
        self.language_button.place(relx=0.95, rely=0.05, anchor='ne')

        # Animated "Hello" Text
        self.hello_text = tk.StringVar()
        self.hello_label = tk.Label(
            self.main_menu_frame,
            textvariable=self.hello_text,
            font=(self.font_name, 48, 'bold')
        )
        self.hello_label.place(relx=0.5, rely=0.3, anchor='center')

        # Cursor for Typing Effect
        self.cursor_label = tk.Label(
            self.main_menu_frame,
            text="|",
            font=(self.font_name, 48, 'bold')
        )
        self.cursor_label.place_forget()

        # Subheading with Adjusted Kerning
        subheading_text = 'F L A S H   C A R D   L A N G U A G E   G A M E'
        self.subheading_label = tk.Label(
            self.main_menu_frame,
            text=subheading_text,
            font=(self.font_name, 16, 'normal')
        )
        self.subheading_label.place(relx=0.5, rely=0.45, anchor='center')

        # Mode Buttons in Single Column
        self.mode_frame = tk.Frame(self.main_menu_frame)
        self.mode_frame.place(relx=0.5, rely=0.65, anchor='center')

        self.learning_button = tk.Button(
            self.mode_frame,
            text="Learning Mode",
            font=(self.pixel_font_name, 12),
            width=20,
            command=lambda: self.start_flashcards(mode='learning')
        )
        self.learning_button.pack(pady=5)

        self.practice_button = tk.Button(
            self.mode_frame,
            text="Practice Mode",
            font=(self.pixel_font_name, 12),
            width=20,
            command=lambda: self.start_flashcards(mode='practice')
        )
        self.practice_button.pack(pady=5)

        self.exit_button = tk.Button(
            self.mode_frame,
            text="Exit",
            font=(self.pixel_font_name, 12),
            width=20,
            command=self.master.quit
        )
        self.exit_button.pack(pady=5)

        # Developer Footnote with Heart Icon
        self.create_developer_footnote()

        # Start the animation
        self.animate_hello()

    def create_developer_footnote(self):
        # Create a frame to hold the text and heart icon
        self.dev_frame = tk.Frame(self.main_menu_frame)
        self.dev_frame.place(relx=0.5, rely=0.95, anchor='center')

        # Label for the first part of the text
        self.dev_text1 = tk.Label(
            self.dev_frame,
            text="Made with Love and AI ",
            font=(self.font_name, 10)
        )
        self.dev_text1.pack(side='left')

        # Load and resize the heart.png image
        try:
            heart_image = Image.open(os.path.join('icons', 'heart.png'))
            heart_image = heart_image.resize((12, 12), Image.LANCZOS)  # Adjust size to match text
            self.heart_photo = ImageTk.PhotoImage(heart_image)
        except Exception as e:
            messagebox.showerror(
                "Image Loading Error",
                f"An error occurred while loading heart.png:\n{e}"
            )
            self.heart_photo = None

        # Label for the heart icon
        if self.heart_photo:
            self.dev_heart = tk.Label(
                self.dev_frame,
                image=self.heart_photo
            )
            self.dev_heart.pack(side='left', padx=(0, 2))  # Slight padding for spacing
        else:
            # Fallback if heart.png fails to load
            self.dev_heart = tk.Label(
                self.dev_frame,
                text="<3",
                font=(self.font_name, 10, 'bold'),
                fg='red'
            )
            self.dev_heart.pack(side='left')

        # Label for the second part of the text
        self.dev_text2 = tk.Label(
            self.dev_frame,
            text=" - turnerboy",
            font=(self.font_name, 10)
        )
        self.dev_text2.pack(side='left')

    def animate_hello(self):
        # Alternate between "Hello" in English and the loaded language

        def type_text(text):
            self.hello_text.set('')
            self.update_cursor_position()
            for char in text:
                self.hello_text.set(self.hello_text.get() + char)
                self.update_cursor_position()
                self.master.update()
                time.sleep(0.1)
            time.sleep(1)

        def erase_text():
            text = self.hello_text.get()
            for _ in text:
                self.hello_text.set(self.hello_text.get()[:-1])
                self.update_cursor_position()
                self.master.update()
                time.sleep(0.05)

        def blink_cursor():
            while True:
                if self.cursor_label.winfo_ismapped():
                    self.cursor_label.place_forget()
                else:
                    self.cursor_label.place(x=self.cursor_x, y=self.cursor_y)
                time.sleep(0.5)

        def loop_animation():
            threading.Thread(target=blink_cursor, daemon=True).start()
            while True:
                for greeting in self.greetings:
                    type_text(greeting)
                    erase_text()

        # Start the animation thread
        threading.Thread(target=loop_animation, daemon=True).start()

    def update_cursor_position(self):
        self.main_menu_frame.update_idletasks()
        x = self.hello_label.winfo_x()
        y = self.hello_label.winfo_y()
        width = self.hello_label.winfo_width()
        self.cursor_x = x + width
        self.cursor_y = y
        self.cursor_label.place(x=self.cursor_x, y=self.cursor_y)

    def load_language_file(self):
        self.play_sound('click')
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json")]
        )
        if file_path:
            self.language_file_path = file_path  # Store the file path
            with open(file_path, 'r', encoding='utf-8') as f:
                self.phrases = json.load(f)
            self.language_name = os.path.splitext(
                os.path.basename(file_path))[0]
            self.language_loaded = True
            self.language_button.config(
                text=f"Language: {self.language_name.capitalize()}",
                bg='green'
            )
            # Determine the foreign language key dynamically
            sample_category = next(iter(self.phrases.values()))
            sample_phrase = sample_category[0]
            self.foreign_language_key = next(
                key for key in sample_phrase.keys() if key not in ['English', 'Transliteration']
            )
            # Update greetings immediately
            self.greetings = ["Hello!"]
            if 'Greetings and Introductions' in self.phrases:
                for phrase in self.phrases['Greetings and Introductions']:
                    if phrase['English'] in ['Hello / Hi', 'Hello']:
                        greeting = phrase[self.foreign_language_key] + '!'
                        self.greetings.append(greeting)
                        break
            # Initialize progress
            self.total_phrases = sum(
                len(category) for category in self.phrases.values())
            # Set TTS language code
            self.set_tts_language_code()
        else:
            messagebox.showwarning(
                "No File Selected",
                "Please select a language file."
            )

    def set_tts_language_code(self):
        # Extract language code from filename
        # Expected filename format: "<language>_phrases.json"
        base_name = os.path.basename(self.language_file_path)
        language_part = base_name.split('_')[0].lower()

        # Map language names to gTTS language codes
        language_code_map = {
            'hindi': 'hi',
            'spanish': 'es',
            'malayalam': 'ml',
            'farsi': 'fa',
            'persian': 'fa',
            # Add more mappings as needed
        }

        # Use the mapping if available, else use the extracted language part
        self.tts_language_code = language_code_map.get(language_part, language_part)

        # Check if the language code is supported by gTTS
        supported_languages = tts_langs()
        if self.tts_language_code not in supported_languages:
            # If not supported, default to 'en' and set a flag
            self.tts_language_code = 'en'
            self.language_supported = False
        else:
            self.language_supported = True

    def start_flashcards(self, mode):
        self.play_sound('click')
        if not self.language_loaded:
            messagebox.showwarning(
                "No Language Loaded",
                "Please load a language file first."
            )
            return
        self.mode = mode
        self.main_menu_frame.destroy()
        self.show_flashcard()

    def show_flashcard(self):
        self.card_frame = tk.Frame(self.master)
        self.card_frame.pack(fill='both', expand=True)

        # Back Button
        self.back_button = tk.Button(
            self.card_frame,
            text="Back to Menu",
            font=(self.pixel_font_name, 12),
            command=self.back_to_menu
        )
        self.back_button.pack(pady=5)

        # Progress Bar
        self.progress_bar_canvas = tk.Canvas(
            self.card_frame, width=600, height=20)
        self.progress_bar_canvas.pack()
        self.progress_bar_bg = self.progress_bar_canvas.create_rectangle(
            0, 0, 600, 20, fill='white', outline='black')
        self.progress_bar = self.progress_bar_canvas.create_rectangle(
            0, 0, 0, 20, fill='green', outline='')

        # Progress Label
        self.progress_label = tk.Label(
            self.card_frame,
            text="Progress: 0%",
            font=(self.font_name, 12)
        )
        self.progress_label.pack(pady=5)

        # Flashcard Display
        self.flashcard_canvas = tk.Canvas(
            self.card_frame, width=500, height=300)
        self.flashcard_canvas.pack(pady=20)
        self.card_front = True  # To track card side
        self.card_background = self.flashcard_canvas.create_rectangle(
            0, 0, 500, 300, fill='#FFCC00', outline='black')
        self.card_text = self.flashcard_canvas.create_text(
            250, 150,
            text="",
            font=(self.english_font_name, 24, 'bold'),
            width=480
        )
        # Transliteration Text
        self.transliteration_text = self.flashcard_canvas.create_text(
            250, 200,  # Position it below the main text
            text="",
            font=(self.font_name, 16),
            width=480
        )

        # Speaker Icon Button
        speaker_image = Image.open(os.path.join('icons', 'speaker.png'))
        speaker_image = speaker_image.resize((30, 30), Image.LANCZOS)
        self.speaker_icon = ImageTk.PhotoImage(speaker_image)
        self.speaker_button = tk.Button(
            self.card_frame,
            image=self.speaker_icon,
            command=self.pronounce_phrase
        )
        self.speaker_button.pack(pady=5)

        # Buttons Frame
        self.buttons_frame = tk.Frame(self.card_frame)
        self.buttons_frame.pack(pady=10)

        # Load icons for buttons
        self.load_button_icons()

        # Show Answer Button
        self.show_answer_button = tk.Button(
            self.buttons_frame,
            image=self.show_answer_icon,
            command=self.toggle_show_answer
        )
        self.show_answer_button.grid(row=0, column=0, padx=5)

        # Correct Button
        self.correct_button = tk.Button(
            self.buttons_frame,
            image=self.correct_icon,
            command=lambda: self.record_answer(correct=True)
        )
        self.correct_button.grid(row=0, column=1, padx=5)

        # Incorrect Button
        self.incorrect_button = tk.Button(
            self.buttons_frame,
            image=self.incorrect_icon,
            command=lambda: self.record_answer(correct=False)
        )
        self.incorrect_button.grid(row=0, column=2, padx=5)

        # Next Button
        self.next_button = tk.Button(
            self.buttons_frame,
            image=self.next_icon,
            command=self.next_flashcard
        )
        self.next_button.grid(row=0, column=3, padx=5)

        # Initialize Flashcards
        self.session_phrases = []
        for category in self.phrases.values():
            self.session_phrases.extend(category.copy())
        random.shuffle(self.session_phrases)
        self.update_progress()
        self.next_flashcard()

    def load_button_icons(self):
        # Determine the resampling method based on Pillow version
        try:
            resample_method = Image.Resampling.LANCZOS  # Pillow >= 9.1.0
        except AttributeError:
            resample_method = Image.LANCZOS  # Older versions

        # Load and resize icons
        show_answer_image = Image.open(
            os.path.join('icons', 'show_answer.png'))
        show_answer_image = show_answer_image.resize(
            (50, 50), resample_method)
        self.show_answer_icon = ImageTk.PhotoImage(show_answer_image)

        correct_image = Image.open(
            os.path.join('icons', 'correct.png'))
        correct_image = correct_image.resize(
            (50, 50), resample_method)
        self.correct_icon = ImageTk.PhotoImage(correct_image)

        incorrect_image = Image.open(
            os.path.join('icons', 'incorrect.png'))
        incorrect_image = incorrect_image.resize(
            (50, 50), resample_method)
        self.incorrect_icon = ImageTk.PhotoImage(incorrect_image)

        next_image = Image.open(
            os.path.join('icons', 'next.png'))
        next_image = next_image.resize(
            (50, 50), resample_method)
        self.next_icon = ImageTk.PhotoImage(next_image)

        # Keep references to prevent garbage collection
        self.icons = [
            self.show_answer_icon,
            self.correct_icon,
            self.incorrect_icon,
            self.next_icon
        ]

    def update_progress(self):
        if self.total_phrases == 0:
            progress_percentage = 0
        else:
            progress_percentage = int(
                (self.correct_answers / self.total_phrases) * 100)
        self.progress_label.config(text=f"Progress: {progress_percentage}%")
        # Update progress bar
        self.progress_bar_canvas.coords(
            self.progress_bar, 0, 0, 6 * progress_percentage, 20)

    def next_flashcard(self):
        self.show_count = 0  # Reset show count
        self.card_front = True
        if self.current_phrase:
            # Append the current card back into session_phrases at a random position
            index = random.randint(0, len(self.session_phrases))
            self.session_phrases.insert(index, self.current_phrase)
        if self.session_phrases:
            self.current_phrase = self.session_phrases.pop()
            self.flashcard_canvas.itemconfig(
                self.card_text,
                text=self.current_phrase['English'],
                font=(self.english_font_name, 24, 'bold')
            )
            self.flashcard_canvas.itemconfig(
                self.transliteration_text, text="")
            self.flashcard_canvas.itemconfig(
                self.card_background,
                fill='#FFCC00'  # Yellow
            )
            self.flashcard_canvas.delete('animation')  # Clear animations
        else:
            messagebox.showinfo(
                "Completed",
                "You've completed all flashcards!"
            )
            self.card_frame.destroy()
            self.create_main_menu()

    def toggle_show_answer(self):
        self.play_sound('show')
        if self.card_front:
            # Show the answer
            translation = self.current_phrase[self.foreign_language_key]
            self.flashcard_canvas.itemconfig(
                self.card_text, text=translation, font=(self.font_name, 24))
            transliteration = self.current_phrase.get('Transliteration', '')
            self.flashcard_canvas.itemconfig(
                self.transliteration_text, text=transliteration)
            self.card_front = False
            if self.mode == 'practice':
                # Update card color based on show count
                self.show_count += 1
                if self.show_count == 1:
                    self.flashcard_canvas.itemconfig(
                        self.card_background, fill='yellow')
                elif self.show_count == 2:
                    self.flashcard_canvas.itemconfig(
                        self.card_background, fill='orange')
                elif self.show_count >= 3:
                    self.flashcard_canvas.itemconfig(
                        self.card_background, fill='green')
        else:
            # Show the question
            self.flashcard_canvas.itemconfig(
                self.card_text, text=self.current_phrase['English'], font=(self.english_font_name, 24, 'bold'))
            self.flashcard_canvas.itemconfig(
                self.transliteration_text, text="")
            self.card_front = True

    def record_answer(self, correct):
        if correct:
            self.correct_answers += 1
            self.play_sound('correct')
            self.correct_animation()
            # Remove the card from session
            if self.current_phrase in self.session_phrases:
                self.session_phrases.remove(self.current_phrase)
            self.update_progress()
            if self.mode == 'practice':
                self.save_progress()
            self.next_flashcard()  # Automatically move to next card
        else:
            self.play_sound('incorrect')
            self.incorrect_animation()
            self.update_progress()
            if self.mode == 'practice':
                self.save_progress()

    def save_progress(self):
        progress_data = {
            'correct_answers': self.correct_answers,
            'total_phrases': self.total_phrases
        }
        with open(f"{self.language_name}_progress.json", 'w') as f:
            json.dump(progress_data, f)

    def pronounce_phrase(self):
        if self.current_phrase:
            if self.card_front:
                text_to_speak = self.current_phrase['English']
                tts_language = 'en'
            else:
                if self.language_supported:
                    text_to_speak = self.current_phrase[self.foreign_language_key]
                    tts_language = self.tts_language_code
                else:
                    # Fallback to Transliteration
                    text_to_speak = self.current_phrase.get('Transliteration', '')
                    tts_language = 'en'  # Use English TTS for transliteration

            def speak():
                try:
                    if text_to_speak.strip() == '':
                        raise ValueError("No text available for TTS.")
                    tts = gTTS(text=text_to_speak, lang=tts_language)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                        temp_file = fp.name
                    tts.save(temp_file)
                    playsound.playsound(temp_file)
                    os.remove(temp_file)  # Delete the temporary file manually
                except Exception as e:
                    messagebox.showerror(
                        "TTS Error",
                        f"An error occurred while trying to speak:\n{e}"
                    )

            threading.Thread(target=speak).start()

    def back_to_menu(self):
        self.play_sound('back')
        self.correct_answers = 0  # Reset progress in learning mode
        self.card_frame.destroy()
        self.create_main_menu()

    # Animation methods
    def correct_animation(self):
        # Zoom animation for correct answer
        for scale in range(10, 13):
            self.flashcard_canvas.scale(
                'all', 250, 150, scale/10, scale/10)
            self.master.update()
            time.sleep(0.02)
        for scale in range(13, 10, -1):
            self.flashcard_canvas.scale(
                'all', 250, 150, scale/10, scale/10)
            self.master.update()
            time.sleep(0.02)
        self.flashcard_canvas.itemconfig(
            self.card_background, fill='light green')
        self.master.update()
        time.sleep(0.5)
        self.flashcard_canvas.itemconfig(
            self.card_background, fill='#FFCC00')  # Back to yellow

    def incorrect_animation(self):
        # Jiggle animation for incorrect answer
        for move in range(-5, 6, 1):
            self.flashcard_canvas.move('all', move, 0)
            self.master.update()
            time.sleep(0.01)
            self.flashcard_canvas.move('all', -move, 0)
        self.flashcard_canvas.itemconfig(
            self.card_background, fill='red')
        self.master.update()
        time.sleep(0.5)
        self.flashcard_canvas.itemconfig(
            self.card_background, fill='#FFCC00')  # Back to yellow

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
