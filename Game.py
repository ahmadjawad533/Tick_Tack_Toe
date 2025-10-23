import tkinter as tk
from tkinter import messagebox
import math, time, platform, os, shutil, tempfile, wave, struct, subprocess

SOUND_FILES = {}

def synthesize_tone(path, freq=440.0, duration=0.18, volume=0.5):
    rate = 44100
    n = int(rate * duration)
    amp = int(32767 * volume)
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        for i in range(n):
            val = amp * math.sin(2 * math.pi * freq * (i / rate))
            wf.writeframesraw(struct.pack('<h', int(val)))

def prepare_sounds(tmpdir):
    tones = {
        'move': (880.0, 0.12, 0.4),
        'win': (880.0, 0.28, 0.6),
        'lose': (220.0, 0.28, 0.6),
        'draw': (440.0, 0.22, 0.5),
    }
    paths = {}
    for name, (f, d, v) in tones.items():
        path = os.path.join(tmpdir, f"{name}.wav")
        synthesize_tone(path, f, d, v)
        paths[name] = path
    return paths

def play_sound(event):
    path = SOUND_FILES.get(event)
    if not path: return
    sys = platform.system()
    if sys == "Windows":
        try:
            import winsound
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            return
        except: pass
    else:
        for cmd in ["paplay", "aplay", "afplay"]:
            if shutil.which(cmd):
                subprocess.Popen([cmd, path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return

TMPDIR = tempfile.mkdtemp(prefix="tictactoe_")
SOUND_FILES = prepare_sounds(TMPDIR)

def check_winner(b, p):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b2,c in wins:
        if b[a]==b[b2]==b[c]==p:
            return (a,b2,c)
    return None

def is_full(b): return ' ' not in b

def minimax(b, depth, is_max, a, beta):
    global move_counter
    move_counter += 1
    if check_winner(b,'O'): return 1
    if check_winner(b,'X'): return -1
    if is_full(b): return 0
    if is_max:
        best = -math.inf
        for i in range(9):
            if b[i]==' ':
                b[i]='O'
                val = minimax(b, depth+1, False, a, beta)
                b[i]=' '
                best = max(best, val)
                a = max(a, best)
                if beta <= a: break
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i]==' ':
                b[i]='X'
                val = minimax(b, depth+1, True, a, beta)
                b[i]=' '
                best = min(best, val)
                beta = min(beta, best)
                if beta <= a: break
        return best

root = tk.Tk()
root.title("✨ Glow Tic Tac Toe ✨")
root.geometry("460x600")
root.config(bg="#0F2027")
root.resizable(False, False)

board = [' ']*9
scores = {"You":0,"Bot":0,"Draw":0}
move_counter = 0

def glow(btn, c1, c2, steps=10, delay=20):
    def step(n=0):
        if n>steps: return
        r1,g1,b1=root.winfo_rgb(c1)
        r2,g2,b2=root.winfo_rgb(c2)
        r=int(r1+(r2-r1)*n/steps)>>8
        g=int(g1+(g2-g1)*n/steps)>>8
        b=int(b1+(b2-b1)*n/steps)>>8
        btn.config(bg=f"#{r:02x}{g:02x}{b:02x}")
        root.after(delay, lambda: step(n+1))
    step()

def ai_turn():
    global move_counter
    move_counter=0
    best=-math.inf
    move=None
    for i in range(9):
        if board[i]==' ':
            board[i]='O'
            val=minimax(board,0,False,-math.inf,math.inf)
            board[i]=' '
            if val>best:
                best=val;move=i
    info.config(text=f"🤖 Bot analyzed {move_counter} moves...")
    root.after(600, lambda: finish_ai(move))

def finish_ai(i):
    if board[i]!=' ': return
    board[i]='O'
    buttons[i].config(text='O',state='disabled',disabledforeground='#00FFAA')
    glow(buttons[i],"#222","#00FFAA")
    play_sound('move')
    check_state()

def player_turn(i):
    if board[i]!=' ':
        return
    board[i]='X'
    buttons[i].config(text='X',state='disabled',disabledforeground='#FF6AA2')
    glow(buttons[i],"#222","#FF6AA2")
    play_sound('move')
    root.after(300, lambda: after_player())

def after_player():
    if check_state(): return
    info.config(text="🤖 Bot is thinking...")
    root.after(400, ai_turn)

def highlight(cells):
    for i in cells: glow(buttons[i],"#333","#FFD700",steps=12)

def check_state():
    global scores
    wx=check_winner(board,'X')
    if wx:
        highlight(wx)
        play_sound('win')
        scores["You"]+=1
        update_score()
        root.after(700, lambda: messagebox.showinfo("Win!","🎉 You won this round!"))
        root.after(1000, restart)
        return True
    wo=check_winner(board,'O')
    if wo:
        highlight(wo)
        play_sound('lose')
        scores["Bot"]+=1
        update_score()
        root.after(700, lambda: messagebox.showinfo("Lost","💻 Bot wins this one!"))
        root.after(1000, restart)
        return True
    if is_full(board):
        play_sound('draw')
        scores["Draw"]+=1
        update_score()
        root.after(600, lambda: messagebox.showinfo("Draw","⚖️ It's a draw!"))
        root.after(900, restart)
        return True
    return False

def restart():
    global board
    board=[' ']*9
    for b in buttons: b.config(text=' ',bg='#222',state='normal')
    info.config(text="Your turn (X)")
    ask_continue()

def ask_continue():
    if messagebox.askquestion("Play again?","Do you want to continue playing?")=='no':
        end_game()

def update_score():
    score.config(text=f"🏆 You: {scores['You']}   🤖 Bot: {scores['Bot']}   ⚖️ Draws: {scores['Draw']}")

def end_game():
    try: shutil.rmtree(TMPDIR)
    except: pass
    root.destroy()

title=tk.Label(root,text="✨ Glow Tic Tac Toe ✨",font=("Helvetica",22,"bold"),fg="#00FFAA",bg="#0F2027")
title.pack(pady=14)

sub=tk.Label(root,text="Play against the Smart Bot",font=("Helvetica",11),fg="#CCCCCC",bg="#0F2027")
sub.pack()

grid=tk.Frame(root,bg="#0F2027")
grid.pack(pady=18)

buttons=[]
for i in range(9):
    b=tk.Button(grid,text=' ',font=("Helvetica",26,"bold"),width=4,height=2,bg='#222',fg='white',
                activebackground='#333',relief='flat',command=lambda i=i:player_turn(i))
    b.grid(row=i//3,column=i%3,padx=8,pady=8)
    buttons.append(b)

info=tk.Label(root,text="Your turn (X)",font=("Helvetica",13),fg="#EEEEEE",bg="#0F2027")
info.pack(pady=8)

score=tk.Label(root,text="🏆 You: 0   🤖 Bot: 0   ⚖️ Draws: 0",font=("Helvetica",13,"bold"),fg="#FFD700",bg="#0F2027")
score.pack(pady=6)

frame=tk.Frame(root,bg="#0F2027")
frame.pack(pady=12)

tk.Button(frame,text="🔁 Restart",font=("Helvetica",11,"bold"),bg="#00ADB5",fg="white",width=10,command=restart).grid(row=0,column=0,padx=8)
tk.Button(frame,text="❌ End Game",font=("Helvetica",11,"bold"),bg="#FF2E63",fg="white",width=10,command=end_game).grid(row=0,column=1,padx=8)

def on_close(): end_game()
root.protocol("WM_DELETE_WINDOW", on_close)

update_score()
root.mainloop()
