# Verbalez

Hi there! I'm Ganesh, a student from McMaster University, Ontario who probably spends way too much time coding (sleep is for the weak, right?). I created Verbalez because I was tired of language apps like Duolingo that seem more obsessed with keeping streaks than actually helping you speak. Don't get me wrong, Duolingo is great for vocabulary, but it takes forever to get to the juicy stuff—the phrases you actually need in real conversations and split them into 11 categories. thanks! chatGPT. and 

The name Verbalez is a blend of "verbal" and "mentalese" (I thought it sounded cool). I wanted a name that captures the essence of speaking and thinking in new languages. This app focuses on commonly used phrases to get basic speaking or any languaeg out soon, so you can jump straight into chatting with people without spending weeks on basics you'll rarely use.

A big shout-out to AI for making this possible. With Verbalez, I aim to cross the bridge and make language speaking and learning quick, practical, and fun. So grab a coffee (or tea, if that's your thing), and let's start speaking!

> **"Culture is a bridge to cross, not a wall to divide us."** – Ganesh

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Loading a Language](#loading-a-language)
  - [Game Modes](#game-modes)
    - [Learning Mode](#learning-mode)
    - [Practice Mode](#practice-mode)
- [Languages and Categories](#languages-and-categories)
- [Adding New Languages](#adding-new-languages)
- [Sound Effects](#sound-effects)
- [Acknowledgments](#acknowledgments)

---

## Features

- **Interactive Flashcards**: Learn phrases categorized by themes like Greetings, Common Courtesies, and more.
- **Multiple Languages**: Currently supports Hindi, Spanish, Malayalam, and Farsi.
- **Text-to-Speech**: Hear the correct pronunciation to enhance your speaking skills.
- **Progress Tracking**: Monitor your learning journey with visual progress bars.
- **User-Friendly Interface**: An intuitive design that feels familiar and fun.

---

## Installation

### Prerequisites

- **Python 3.x** installed on your system. [Download Python](https://www.python.org/downloads/)
- **Required Python packages**:
  - `tkinter` (usually comes with Python)
  - `gtts`
  - `playsound`
  - `Pillow`

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/verbalez.git
   cd verbalez
   ```

2. **Install Dependencies**

   ```bash
   pip install gtts playsound Pillow
   ```

   > **Note**: On macOS, you might need to install `PyObjC` for `playsound` to work:

   ```bash
   pip install PyObjC
   ```

3. **Download Language Files**

   Create a folder named `languages` in the project directory and place all your JSON language files inside it.

   ```
   verbalez/
   ├── flashcards.py
   ├── languages/
   │   ├── hindi_phrases.json
   │   ├── spanish_phrases.json
   │   ├── malayalam_phrases.json
   │   └── farsi_phrases.json
   └── ...
   ```

4. **Run the Application**

   ```bash
   python flashcards.py
   ```

## Usage

### Loading a Language

Upon launching Verbalez, you'll see a red button labeled **"No Language Loaded"** at the top-right corner. Click this button to load a language JSON file from the `languages` folder.

- The button turns green and displays the name of the loaded language.
- The animated "Hello" text will alternate between English and the equivalent greeting in the loaded language.

### Game Modes

After loading a language, choose between two game modes:

#### Learning Mode

- Designed for beginners.
- No penalties for incorrect answers.
- Progress increases with each correct answer.
- Cards remain yellow, providing a stress-free learning environment.

#### Practice Mode

- Ideal for testing your knowledge.
- Progress increases only when you select "Correct" after recalling a phrase.
- Cards change color based on how many times you've viewed the answer:
  - **First Time**: 💛 Yellow
  - **Second Time**: 🧡 Orange
  - **Third Time and Beyond**: 💚 Green
- Encourages you to recall phrases with minimal hints.

---

## Languages and Categories

### Available Languages

- Hindi
- Spanish
- Malayalam
- Farsi

### Phrase Categories

Each language includes phrases organized into 11 everyday speaking categories:

1. **Greetings and Introductions**
2. **Common Courtesies**
3. **Basic Questions and Responses**
4. **Everyday Phrases**
5. **Expressing Needs and Feelings**
6. **Directions and Locations**
7. **Numbers and Time**
8. **Emergency Phrases**
9. **Social Phrases**
10. **Making Plans**
11. **Flirting** (Because why not? 😉)

---

## Adding New Languages

Want to add Klingon or Elvish? Go for it!

1. **Create a JSON File**

   - Follow this generic structure:

     ```json
     {
       "Category Name": [
         {
           "English": "Hello",
           "TargetLanguage": "Hola",
           "Transliteration": "Hola"
         },
         // ... more phrases
       ],
       // ... more categories
     }
     ```

   - Replace `"TargetLanguage"` with the actual language name (e.g., `"Spanish"`).

2. **Save the File**

   - Name the file as `<language>_phrases.json`.
   - Place it inside the `languages` folder.

3. **Load the Language**

   - Click the **"No Language Loaded"** button in the app and select your new JSON file.

---

## Sound Effects

*(Placeholders are in the program; sounds will be added in a future update.)*

The application supports optional sound effects to enrich your learning experience.

### Available Sound Actions

- **Clicking Main Menu Buttons**
- **Selecting Correct Answer**
- **Selecting Incorrect Answer**
- **Showing the Answer**
- **Returning to Main Menu**

### Adding Sound Files

1. **Prepare MP3 Files**

   - Name the files accordingly:
     - `click.mp3`
     - `correct.mp3`
     - `incorrect.mp3`
     - `show.mp3`
     - `back.mp3`

2. **Place in Sounds Folder**

   - Create a folder named `sounds` in the project directory.
   - Place all your MP3 files inside it.

     ```
     verbalez/
     ├── flashcards.py
     ├── sounds/
     │   ├── click.mp3
     │   ├── correct.mp3
     │   ├── incorrect.mp3
     │   ├── show.mp3
     │   └── back.mp3
     └── ...
     ```

> **Note**: Sound effects are optional. The application will run smoothly even without them.

---

## Acknowledgments

Made with love and AI ❤️ – *Ganesh*

This project is a small step towards connecting people through language. Feel free to contribute, suggest new features, or add more languages. Let's make the world a little smaller, one word at a time.

---

**Enjoy your language learning journey!**

---

*P.S. If you find any bugs, remember they're features in disguise. Happy learning!*
