#  Tic Tac Toe (AI Edition)

A modern, glowing **Tic Tac Toe** game built with Python and Tkinter, featuring:
- Intelligent AI (using the **Minimax Algorithm** with Alpha-Beta pruning)
- Smooth glowing UI animations  
- Sound effects for moves, wins, and draws  
- Auto-restart and "Play Again" prompt  
- Clean dark UI design

---

## 🧠 Features

✅ **AI Opponent**
- Uses the Minimax algorithm for strategic decision-making.
- The AI displays how many moves it analyzed before making its turn.

✅ **Modern Interface**
- Smooth glowing animations.
- Clean dark theme.
- Interactive buttons with highlight effects.

✅ **Sound Effects**
- Move, win, lose, and draw all have unique sound tones.
- Works on Windows, macOS, and Linux.

✅ **Game Control**
- Restart or end the game anytime.
- Automatic new round after each result.

---

## 🧩 How to Run

### 1. Clone or Download this Repository
```bash
git clone https://github.com/your-username/glow-tictactoe.git
cd glow-tictactoe
````

### 2. Install Required Dependencies

This project only uses standard Python libraries — **no external dependencies** required.
However, ensure `tkinter` is installed:

#### On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3-tk -y
```

#### On Windows:

Tkinter comes pre-installed with Python.

---

### 3. Run the Game

```bash
python3 tictactoe.py
```

---

## 🕹️ How to Play

* You play as **X**, and the AI plays as **O**.
* Click on a cell to make your move.
* The AI will “think” for a moment before making its move.
* After each round:

  * A message appears (Win, Lose, or Draw).
  * The game automatically restarts.
* You can also click **🔁 Restart** to start immediately.
* To exit, click **❌ End Game** or close the window.

---

## ⚙️ Technical Details

* **Language:** Python 3.10+
* **GUI Library:** Tkinter
* **AI Algorithm:** Minimax with Alpha-Beta pruning
* **Audio:** Procedurally generated `.wav` tones (no external files)
* **Platform Compatibility:** Linux, Windows, macOS

---

## 🧩 Folder Structure

```
.
├── game.py     # Main game script
├── README.md        # Documentation
```

Temporary sound files are auto-generated and cleaned up when the game exits.

---

## 🏆 Example Output

When AI plays:

```
🤖 Bot analyzed 213 moves...
```

When you win:

```
🎉 You won this round!
```

When game ends:

```
💻 Bot wins this one!
⚖️ It's a draw!
```



## 📜 License

This project is open-source and free to use under the [MIT License](LICENSE).

---

