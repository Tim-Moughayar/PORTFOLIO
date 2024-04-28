"""
This is a simple blackjack game, created using the tkinter library.

Input:
    User mouse

Output:
    Blackjack game

References:
 * https://stackoverflow.com/questions/61639278/to-detect-button-press-in-python-tkinter-module
 * https://www.geeksforgeeks.org/blackjack-console-game-using-python/
 * https://www.youtube.com/watch?v=xJZksz2UpqE
 * https://stackoverflow.com/questions/3136689/find-and-replace-string-values-in-list
 * https://web.archive.org/web/20201111190625id_/http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
 * https://tkinter.com/build-a-blackjack-card-game-python-tkinter-gui-tutorial-208/
 * https://stackoverflow.com/questions/67698873/how-to-remove-quotes-from-list-of-strings-and-store-it-as-list-again

CIS 216 Team 4:
Timothy El Moughayar
Frank Boxenbaum
Tyler Reynolds

"""

import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk


class BlackjackGame:
    """Creates blackjack game class"""
    def __init__(self, master):
        """Initializes deck of cards and deals hands to player and dealer."""
        self.master = master
        self.master.geometry("1200x700")
        self.master.title("Blackjack Game")
        self.master.configure(background="green")

        self.shuffle()

        self.player_bust = False
        self.dealer_bust = False
        self.player_stand = False
        self.reset_table = False

        self.create_widgets()

    def create_widgets(self):
        """Creates the on screen text, buttons and frames."""

        self.dealer_frame = tk.LabelFrame(self.master, text="Dealer", bd=0, height=100, width=200)
        self.dealer_frame.pack(pady=15)

        self.player_frame = tk.LabelFrame(self.master, text="Player", bd=0, height=100, width=200)
        self.player_frame.pack(pady=(0, 15))

        self.button_frame = tk.Frame(self.master, bg="green")
        self.button_frame.pack()

        self.quit_button = tk.Button(self.button_frame, text="Quit", command=self.master.destroy)
        self.quit_button.pack(side="left", padx=(0, 100), pady=30, ipadx=20)

        self.hit_button = tk.Button(self.button_frame, text="Hit", command=self.hit)
        self.hit_button.pack(side="left", padx=(20, 0), pady=30, ipadx=30)

        self.stand_button = tk.Button(self.button_frame, text="Stand", command=self.stand)
        self.stand_button.pack(side="left", padx=(10, 0), pady=30, ipadx=20)

        self.player_label = []

        for iteration, card_name in enumerate(self.player_hand):
            self.player_image = (self.resize_cards(f'images/cards/{card_name}.png'))
            self.player_label.append(tk.Label(self.player_frame, image=self.player_image))
            player_card = self.player_label[iteration]
            player_card.image = self.player_image
            player_card.pack(pady=20, padx=15, side=tk.LEFT)

        self.dealer_label = []

        for iteration, card_name in enumerate(self.dealer_hand):
            self.dealer_image = (self.resize_cards(f'images/cards/{card_name}.png'))
            self.dealer_label.append(tk.Label(self.dealer_frame, image=self.dealer_image, text=card_name.replace("_", " ")))
            dealer_card = self.dealer_label[iteration]
            dealer_card.image = self.dealer_image
            dealer_card.pack(pady=20, padx=15, side=tk.LEFT)

        self.update_display()

    def resize_cards(self, card):
        """Opens the card image and resizes it accordingly."""
        our_card_img = Image.open(card)

        our_card_resize_image = our_card_img.resize((150, 218))

        global our_card_image
        our_card_image = ImageTk.PhotoImage(our_card_resize_image)

        return our_card_image

    def shuffle(self):
        """Creates and shuffles the deck of cards."""
        suits = ["diamonds", "clubs", "hearts", "spades"]
        values = range(2, 15)
        # 11 = Jack, 12=Queen, 13=King, 14 = Ace

        self.deck = []

        for suit in suits:
            for value in values:
                self.deck.append(f'{value}_of_{suit}')

        random.shuffle(self.deck)

        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

    def calculate_hand_total(self, hand):
        """Calculate the value of the player and dealer's hands."""
        total = 0

        for card in hand:
            if card == 11 or card == 12 or card == 13:
                total += 10
            elif card == 14:
                total += 11
            else:
                total += card

        if total > 21 and hand.count(14) > 0:
            total -= 10

        return total

    def calculate_hand_values(self):
        """Calculate the value of a hand of cards for blackjack."""
        self.dealer_hand_values = []
        self.player_hand_values = []

        for card in self.dealer_hand:
            self.dealer_hand_values.append(int(card.split("_", 1)[0]))

        for card in self.player_hand:
            self.player_hand_values.append(int(card.split("_", 1)[0]))

    def update_display(self):
        """Updates the game area display with the current cards and scores."""

        self.calculate_hand_values()

        self.player_total = self.calculate_hand_total(self.player_hand_values)
        self.dealer_total = self.calculate_hand_total(self.dealer_hand_values)

        player_hand_text = self.player_hand
        dealer_hand_text = self.dealer_hand

        player_hand_text = [(text
            .replace("_", " ")
            .replace("14", "Ace")
            .replace("13", "King")
            .replace("12", "Queen")
            .replace("11", "Jack"))
            for text in player_hand_text]

        player_hand_text = '[%s]' % ', '.join(map(str, player_hand_text))

        dealer_hand_text = [(text
            .replace("_", " ")
            .replace("14", "Ace")
            .replace("13", "King")
            .replace("12", "Queen")
            .replace("11", "Jack"))
            for text in dealer_hand_text]

        dealer_hand_text = '[%s]' % ', '.join(map(str, dealer_hand_text))
        self.dealer_text = f"Dealer's Hand:  {dealer_hand_text} Total: {self.dealer_total}"
        self.player_text = f"Player's Hand: {player_hand_text} Total: {self.player_total}"

        if self.reset_table is False:
            self.dealer_frame.config(text=self.dealer_text)
            self.player_frame.config(text=self.player_text)
        else:
            pass

        if self.player_total == self.dealer_total == 21:
            self.end_game("It's a tie! Both have Blackjack!")
        elif self.player_total == 21:
            self.end_game("Player wins with Blackjack!")
        elif self.dealer_total == 21:
            self.end_game("Dealer wins with Blackjack!")

    def end_game(self, message):
        """Displays the results of the game round and asks if the user want to play again or quit."""
        self.reset_table = True
        messagebox.showinfo("Results", message)
        answer = messagebox.askyesno(title="Game Over", message="Do you want to play again?")
        if answer:
            self.player_hand = []
            self.dealer_hand = []
            self.player_total = 0
            self.dealer_total = 0
            self.player_stand = False
            self.player_frame.destroy()
            self.dealer_frame.destroy()
            self.button_frame.destroy()
            BlackjackGame(self.master)
        else:
            messagebox.showinfo("Goodbye", message="Thanks for playing!")
            self.master.destroy()

    def hit(self):
        """Adds another card from the deck to the player's hand."""
        self.player_hand.append(self.deck.pop())
        card = self.player_hand[-1]
        self.player_image = (self.resize_cards(f'images/cards/{card}.png'))
        card = tk.Label(self.player_frame, image=self.player_image)
        card.image = self.player_image
        card.pack(pady=20, padx=15, side=tk.LEFT)

        self.update_display()
        self.check_victory()

    def stand(self):
        """The player declines to draw another card and the game progresses to the outcome."""
        while self.calculate_hand_total(self.dealer_hand_values) < 17:
            self.dealer_hand.append(self.deck.pop())
            self.calculate_hand_values()

            card = self.dealer_hand[-1]
            self.dealer_image = (self.resize_cards(f'images/cards/{card}.png'))
            card = tk.Label(self.dealer_frame, image=self.dealer_image)
            card.image = self.dealer_image
            card.pack(pady=20, padx=15, side=tk.LEFT)

            self.update_display()
            self.check_victory()

        self.dealer_bust = self.calculate_hand_total(self.dealer_hand_values) > 21
        self.player_stand = True

        self.update_display()
        self.check_victory()

    def check_victory(self):
        """Checks the victory conditions."""
        if self.player_total > 21:
            self.player_bust = True
            self.end_game("Player busts! Dealer wins.")
        elif self.dealer_bust:
            self.end_game("Dealer busts! Player wins.")
        elif self.player_total == self.dealer_total == 21 and self.reset_table is False:
            self.end_game("It's a tie! Both have Blackjack!")
        elif self.player_total == 21 and self.reset_table is False:
            self.end_game("Player wins with Blackjack!")
        elif self.dealer_total == 21 and self.reset_table is False:
            self.end_game("Dealer wins with Blackjack!")
        elif self.player_total > self.dealer_total and self.player_stand is True:
            self.end_game("Player wins!")
        elif self.player_total < self.dealer_total and self.player_stand is True:
            self.end_game("Dealer wins!")
        elif self.player_total == self.dealer_total and self.player_stand is True and self.reset_table is False:
            self.end_game("Tie!")


"""Creates window, launches game, and runs loops the GUI."""
if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()

