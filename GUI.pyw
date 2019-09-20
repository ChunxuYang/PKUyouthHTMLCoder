import tkinter as tk
mainWindow = tk.Tk()
mainWindow.title("北大青年自动排版工具")
mainWindow.geometry("800x600+400+100")
text = "北大青年"
b = tk.Label(mainWindow, text=text).pack()
b = tk.Button(mainWindow, text="close", command=mainWindow.quit()).pack()






mainWindow.mainloop()
