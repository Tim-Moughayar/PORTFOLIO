# How to Run:
Enter into IDE terminal to clone repository and run program:
```
git clone https://github.com/Tim-Moughayar/PORTFOLIO/Blackjack_Card_Game.git
cd PORTFOLIO/Blackjack_Card_Game
python blackjack_card_game.py           
```

## How to play:

**Objective:** The main objective of blackjack is to beat the dealer's hand without going over 21.
<br/>

**Card Values:** Number cards (2-10) are worth their face value. Face cards (Jack, Queen, King) are each worth 10 points. Aces can be worth either 1 or 11 points, depending on which value benefits the player the most without busting (going over 21).
<br/>

**Gameplay:** The game begins with each player and the dealer receiving two cards face-up.
<br/>

**Player's Turn:** Players have several options during their turn:
  * **Hit:** Take another card from the dealer. Players can hit as many times as they want until they decide to stand or bust.
  * **Stand:** Refuse additional cards and keep the current hand.

**Dealer's Turn:** Once all players have finished their turns, the dealer reveals their hole card. The dealer must hit until their hand reaches a total of 17 or higher. If the dealer's hand exceeds 21, they bust and all remaining players win.
  * **Winning:** There are several possible outcomes:
  * **Natural Blackjack:** If a player's first two cards are an ace and a 10-value card (10, Jack, Queen, King), they have a "natural" blackjack and typically win one and a half times their bet unless the dealer also has a blackjack, in which case it's a push (tie).
  * **Beating the Dealer:** If the player's hand total is higher than the dealer's without exceeding 21, the player wins.
  * **Push:** If the player's hand and the dealer's hand have the same total, it's a push.
  * **Bust:** If the player's hand total exceeds 21, they bust and lose regardless of the dealer's hand.

<br/>

## Don't have Python or GIT?
**Install Python:**
- Python 3.12.2: https://www.python.org/downloads/release/python-3122/

<br/>

**Install Git:**
- Mac: install [Homebrew](http://mxcl.github.com/homebrew/) first, then `brew install git`.
- Windows or Linux: see [Installing Git](http://git-scm.com/book/en/Getting-Started-Installing-Git) from the _Pro Git_ book.

<br/>

## How to Remove:
> [!WARNING]  
> If you want to try the other projects in the portfolio, change the directory.

<br/>

When your done viewing the projects, you can remove the repo using these commands:
```
cd..
cd..
rm -Recurse -Force PORTFOLIO
```

