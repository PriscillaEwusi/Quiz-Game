import random  # used to shuffle questions and answer options

'''The question bank
A dictionary where each KEY is a category name and each VALUE
is a list of questions. Every question is itself a dictionary
with the question text, 4 options and the correct answer.'''

QUESTIONS = {
    "Python Basics": [
        {"question": "Which function prints text to the screen?",
         "options": ["echo()", "print()", "display()", "write()"],
         "answer": "print()"},
        {"question": "Which symbol starts a single-line comment in Python?",
         "options": ["//", "/*", "#", "--"],
         "answer": "#"},
        {"question": "What does len('Python') return?",
         "options": ["5", "6", "7", "Error"],
         "answer": "6"},
        {"question": "Which data type stores True or False?",
         "options": ["int", "str", "bool", "float"],
         "answer": "bool"},
        {"question": "Which keyword is used to define a function?",
         "options": ["def", "func", "define", "function"],
         "answer": "def"},
    ],
    "General Knowledge": [
        {"question": "What is the largest continent?",
         "options": ["Africa", "Asia", "Europe", "North America"],
         "answer": "Asia"},
        {"question": "What is the capital city of Japan?",
         "options": ["Seoul", "Beijing", "Tokyo", "Bangkok"],
         "answer": "Tokyo"},
        {"question": "How many continents are there?",
         "options": ["5", "6", "7", "8"],
         "answer": "7"},
        {"question": "Which planet is known as the Red Planet?",
         "options": ["Mars", "Venus", "Jupiter", "Mercury"],
         "answer": "Mars"},
        {"question": "Which is the largest ocean?",
         "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
         "answer": "Pacific"},
    ],
    "Science": [
        {"question": "What is the chemical formula for water?",
         "options": ["H2O", "CO2", "O2", "NaCl"],
         "answer": "H2O"},
        {"question": "Which gas do plants absorb from the air?",
         "options": ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"],
         "answer": "Carbon dioxide"},
        {"question": "What is the closest star to Earth?",
         "options": ["Alpha Centauri", "The Sun", "Sirius", "Polaris"],
         "answer": "The Sun"},
        {"question": "What is the hardest natural substance?",
         "options": ["Gold", "Iron", "Quartz", "Diamond"],
         "answer": "Diamond"},
        {"question": "How many bones does an adult human have?",
         "options": ["106", "206", "306", "406"],
         "answer": "206"},
    ],
}

LETTERS = "ABCD"  # labels for the answer options

# Best score per category, remembered while the program is running.
# Example: {"Science": {"name": "Ama", "score": 4, "total": 5}}
high_scores = {}

'''Input helpers. They keep asking until the input is valid,
so the program never crashes on bad input.'''

def get_valid_number(prompt, minimum, maximum):
    """Ask for a whole number between minimum and maximum."""
    while True:
        try:
            number = int(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if minimum <= number <= maximum:
            return number
        print(f"Please enter a number from {minimum} to {maximum}.")
 
 
def get_player_name():
    """Ask for a non-empty player name."""
    while True:
        name = input("Enter your name: ").strip()
        if name:
            return name
        print("Name cannot be empty.")
 
 
def get_answer_letter(prompt):
    """Ask for A, B, C or D (upper or lower case) and return the index 0-3."""
    while True:
        text = input(prompt).strip().upper()
        if len(text) == 1 and text in LETTERS:
            return LETTERS.index(text)  # "A" -> 0, "B" -> 1, ...
        print("Invalid answer. Please type A, B, C or D.")

# Menus

def show_menu(player):
    #Print the main menu.
    print(f"\n===== QUIZ GAME (Player: {player}) =====")
    print("1. Start a quiz")
    print("2. View high scores")
    print("3. How to play")
    print("4. Exit")

def choose_category():
    """Let the player pick a category and return its name."""
    categories = list(QUESTIONS.keys())  # ["Python Basics", "General Knowledge", ...]
    print("\nChoose a category:")
    for number, name in enumerate(categories, start=1):
        print(f"{number}. {name}")
    choice = get_valid_number(f"Enter 1-{len(categories)}: ", 1, len(categories))
    return categories[choice - 1]  # lists start at 0, our menu starts at 1

# Ask one question and report whether it was correct
def ask_question(number, total, item):
    """Show one question. Returns True if the player answered correctly."""
    options = item["options"][:]  # [:] makes a copy so the original isn't changed
    random.shuffle(options)       # shuffle so the answer isn't always in the same place
 
    print(f"\nQuestion {number} of {total}")
    print(item["question"])
    for letter, option in zip(LETTERS, options):
        print(f"  {letter}. {option}")
 
    index = get_answer_letter("Your answer (A/B/C/D): ")
    chosen = options[index]
 
    if chosen == item["answer"]:
        print("Correct!")
        return True
    print(f"Wrong. The correct answer was: {item['answer']}")
    return False

# Run a full quiz
def run_quiz(player):
    """Play one quiz in a chosen category and show the result."""
    category = choose_category()
    # random.sample shuffles the order of the questions
    questions = random.sample(QUESTIONS[category], len(QUESTIONS[category]))
    total = len(questions)
    score = 0
 
    print(f"\nCategory: {category}. Good luck, {player}!")
 
    for number, item in enumerate(questions, start=1):
        if ask_question(number, total, item):
            score += 1  # add 1 point for each correct answer
 
    show_result(player, category, score, total)
    update_high_score(player, category, score, total)
 
 
def show_result(player, category, score, total):
    """Print the final score, percentage and a message."""
    percent = score / total * 100
    print("\n----- RESULT -----")
    print(f"{player}, you scored {score}/{total} ({percent:.0f}%) in {category}.")
 
    if percent == 100:
        print("Perfect score! Amazing!")
    elif percent >= 60:
        print("Well done! Good job.")
    else:
        print("Keep practising. You'll do better next time!")

# Update the high score for a category if the player did better than before
def update_high_score(player, category, score, total):
    """Save the score if it is the best so far for this category."""
    best = high_scores.get(category)  # None if no score yet
    if best is None or score > best["score"]:
        high_scores[category] = {"name": player, "score": score, "total": total}
        print("New high score for this category!")
 
 
def view_high_scores():
    """Display the best score for each category."""
    print("\n----- HIGH SCORES -----")
    if not high_scores:
        print("No scores yet. Play a quiz first!")
        return
    for category, best in high_scores.items():
        print(f"{category}: {best['name']} - {best['score']}/{best['total']}")
 
 
def show_instructions():
    """Explain the rules."""
    print("\n----- HOW TO PLAY -----")
    print("1. Choose Start a quiz, then pick a category.")
    print("2. Each question has 4 options labelled A, B, C and D.")
    print("3. Type the letter of the answer you think is correct.")
    print("4. You get 1 point for every correct answer.")
    print("5. Your best score in each category is saved as a high score.")

# Main loop - the loop-based menu.
# It repeats until the user chooses Exit.
def main():
    """Run the quiz game."""
    print("Welcome to the Quiz Game!")
    player = get_player_name()
 
    while True:
        show_menu(player)
        choice = get_valid_number("Choose an option (1-4): ", 1, 4)
 
        if choice == 1:
            run_quiz(player)
        elif choice == 2:
            view_high_scores()
        elif choice == 3:
            show_instructions()
        elif choice == 4:
            print(f"Thanks for playing, {player}. Goodbye!")
            break  # leave the loop, which ends the program
 
# Run main() only when this file is run directly
if __name__ == "__main__":
    main()