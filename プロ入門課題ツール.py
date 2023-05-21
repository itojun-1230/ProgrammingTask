import tkinter as tk
from tkinter import messagebox
import random

# メインウィンドウ
root = tk.Tk()
root.title("プログラミング入門課題ツール")
width = 900
height = 900
root.geometry(f"{width}x{height}")
background = "white"
root.resizable(width=False, height=False)

text = ""
entries = [[],[]]
menu= []
flag = 0
empty = 0

def xscroll(tk,canvasFrame,canvas):
    # 水平方向のスクロールバーを作成
    x_scroll = tk.Scrollbar(canvasFrame,orient=tk.HORIZONTAL)
    x_scroll.grid(row=1, column=0,sticky=tk.W + tk.E)
    x_scroll.config(command=canvas.xview)
    canvas.config(xscrollcommand=x_scroll.set)
def yscroll(tk,canvasFrame,canvas):
    # 垂直方向のスクロールバーを作成
    y_scroll = tk.Scrollbar(canvasFrame,orient=tk.VERTICAL)
    y_scroll.grid(row=0, column=1,sticky=tk.N + tk.S)
    y_scroll.config(command=canvas.yview)
    canvas.config(yscrollcommand=y_scroll.set)
def click():
    global text,flag,empty
    if flag == 0:
        yscroll(tk,canvasFrame,canvas)
        text=textbox.get("1.0", "end").split("\n")
        sharp = [index for index,value in enumerate(text) if '#' in value]
        yoko = 10;tate = 10; max_yoko = 0
        for index,i in enumerate(text,0):
            if sharp[0] <= index <= sharp[-1]:
                if 'O' in i:
                    txt = ''
                    for ind,l in enumerate(i,0):
                        txt += l
                        try:
                            if (l == 'O' and i[ind+1] != 'O') or (l != 'O' and i[ind+1] == 'O'):
                                txt += "☭"
                        except:
                            pass
                    for l in txt.split("☭"):
                        texts = tk.Label(textFrame, text=l, bg=background, anchor='e', font=("メイリオ", "15"))
                        texts.bind("<MouseWheel>", wheel)
                        texts.lower()
                        texts.place(x=yoko,y=tate)
                        texts.update_idletasks()
                        if 'O' in l:
                            tcl = textFrame.register(EntryKey)
                            entry = tk.Entry(textFrame,validate='key',fg = "#9b9b9b" ,vcmd=(tcl, "%P","%W"), relief=tk.SOLID, font=("メイリオ",10))
                            entry.bind("<MouseWheel>", wheel)
                            entry.bind("<FocusIn>", EntryFocusIn)
                            entry.bind("<FocusOut>", EntryFocusOut)
                            entries[0].append(entry)
                            entries[1].append(len(l))
                            entries[0][-1].place(x=yoko, y=tate+2, width=texts.winfo_width(), height=28)
                            entry.insert(0,'O'*len(l))
                        yoko = yoko + texts.winfo_width()
                else:
                    texts = tk.Label(textFrame, text=i, bg=background, anchor='e', font=("メイリオ", "15"))
                    texts.bind("<MouseWheel>", wheel)
                    texts.lower()
                    texts.place(x=yoko,y=tate)
                
                tate += 30
                if max_yoko < yoko:
                    max_yoko = yoko
                yoko = 10
        empty = len(entries[0])
        canvas.config(scrollregion=(0, 0, max_yoko + 100, tate))
        
        menu.append(menu[0])    #サイドバーの変更
        menu[-1].config(text="スクリプト生成")
        menu[-1].place(x=65,y=120)
        menu.remove(menu[0])
        menu[0].config(height=14)
        menu.append(menu[0])
        menu[-1].place(x=10,y=200)
        menu.remove(menu[0])
        texts = tk.Label(SideFrame, text="●", fg="black", bg="#f0f8ff", anchor='e', font=("メイリオ", "15","bold"))
        menu.append(texts)
        menu[-1].place(x=10,y=50)
        texts = tk.Label(SideFrame, text="空欄数 :", fg="gray", bg="#f0f8ff", anchor='e', font=("メイリオ", "15","bold"))
        menu.append(texts)
        menu[-1].place(x=35,y=50)
        texts = tk.Label(SideFrame, text=empty, fg="#ff6600", bg="#f0f8ff", anchor='e', font=("メイリオ", "15","bold"))
        menu.append(texts)
        menu[-1].place(x=140,y=50)
        
        textbox.destroy()
        flag += 1
    elif flag == 1  and empty == 0:
        result = messagebox.askyesno("確認","クリップボードを上書きします\nよろしいですか？")
        if result == True:
            output = [i.get() for i in entries[0]]
            txt = ""
            for i in range(len(output)):
                txt += "document.getElementsByClassName('queryinput editable')["+str(i)+"].value ='" + output[i] +"';"
            txt += "document.getElementsByClassName('proceed')[0].click();"
            frame.clipboard_clear()
            frame.clipboard_append(txt)
    elif flag == 1  and empty != 0:
        result = messagebox.showerror("注意","空欄があります")


def EntryKey(value,event):
    global empty
    if flag != 0:
        widget = textFrame.nametowidget(event)  #ウェジットを名前から抽出
        index = entries[0].index(widget)        #ウェジットからインデックス番号を抽出
        MaxCount = entries[1][index]            #最大文字数を抽出
        if MaxCount < len(value):
            return False
        elif MaxCount == len(value) and value != 'O'*MaxCount:
            widget.config(bg = "#ff7575")
            empty -= 1
        elif MaxCount != len(value) and widget["bg"] == "#ff7575":
            widget.config(bg = "#ffffff")
            empty += 1
        menu[-1]["text"] = empty
    
    return True
def EntryFocusIn(e):
    widget = e.widget
    index = entries[0].index(widget)        #ウェジットからインデックス番号を抽出
    MaxCount = entries[1][index]            #最大文字数を抽出
    if widget.get() == 'O'*MaxCount:
        widget.delete(0,tk.END)
        widget.config(fg="black")
def EntryFocusOut(e):
    widget = e.widget
    index = entries[0].index(widget)        #ウェジットからインデックス番号を抽出
    MaxCount = entries[1][index]            #最大文字数を抽出
    if len(widget.get()) == 0:
        widget.insert(0,'O'*MaxCount)
        widget.config(fg="#9b9b9b")
def wheel(event):
    wheel = int(event.delta * 0.02) * -1
    canvas.yview_scroll(wheel, "units")

#フレーム作成
frame = tk.Frame(root, width=width, height=height, bg=background)
frame.pack()
#ヘッダー用フレーム
headerFrame = tk.Frame(frame, width=width, height=95, bg="#2f5fff")
headerFrame.place(x=0,y=0)

#サイドバー用フレーム
SideSize = [200,400]
SideFrameRelief = tk.Frame(frame, width=SideSize[0]+6, height=SideSize[1]+6, bg="#2f5fff")
SideFrameRelief.place(x=680,y=110)
SideFrame = tk.Frame(SideFrameRelief, width=SideSize[0], height=SideSize[1], bg="#f0f8ff")
SideFrame.place(x=3,y=3)
button = tk.Button(SideFrame, text="確定", width=9, height=3, command=click)
menu.append(button)
menu[-1].place(x=65,y=20)
txt = tk.Text(SideFrame, relief=tk.SOLID, bd=1, width=25, height=20)
txt.insert(tk.END,"使い方:\n1.\n　プログラミング入門演習のレポートを開く\n2.\n　ctrl+Aで全選択し、コピーする\n3.\n　ここにペーストする\n4.\n　確定ボタンをクリック\n5.\n　空欄を埋める\n※これより下は未検証\n6.\n　スクリプト生成をクリック\n7.\n　プログラミング入門演習の小テストを開く\n8.\n　F12をクリックしコンソールを開く\n9.\n　スクリプトをペーストしてEnter")
txt.configure(state='disabled')
menu.append(txt)
menu[-1].place(x=10,y=110)
#キャンバス用フレーム
canvasFrame = tk.Frame(frame, width=500, height=500, bg=background, relief=tk.SOLID, bd=1)
canvasFrame.place(x=10,y=100)

#ヘッダーの作成
word = tk.Label(headerFrame, bg="#2f5fff", fg="white", font=("size",20), text="プログラミング入門課題ツール")
word.place(x=10,y=0)
word = tk.Label(headerFrame, bg="#2f5fff", fg="white", font=("size",15, "bold"), text="伊藤潤平")
word.place(x=width-85,y=70)

#キャンバス作成
canvas_x = 600
canvas_y = 700
canvas = tk.Canvas(canvasFrame, width=canvas_x, bg=background, height=canvas_y, scrollregion=(0, 0, 1500, 2000))
canvas.grid(row=0, column=0)
# キャンバス内のフレーム
textFrame = tk.Frame(canvas, bg=background, width=1500, height=99999)
canvas.create_window((0,0), window=textFrame, anchor=tk.NW)
#イベント
canvas.bind("<MouseWheel>", wheel)
textFrame.bind("<MouseWheel>", wheel)
#初期テキストボックス
textbox = tk.Text(textFrame,width=1000, height=100)
textbox.place(x=0,y=0)

xscroll(tk,canvasFrame,canvas)


# アプリケーションの開始
root.mainloop()
print("終了します...")