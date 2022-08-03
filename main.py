import tkinter as tk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('cel7 Art Editor')
        self.root.geometry('550x600')
        self.root.resizable(False, False)
        self.root.configure(background='#505050')
        self.colors = ["#000000", "#F7F7E7", "#F70C67", "#FD9819", "#E7D50D", "#A1E119", "#44BCFF", "#AA8BFF", "#F9ACB0",
                        "#AD3045", "#34956E", "#254469", "#7D8E9A", "#C3BFAF", "#76725E", "#3C3B2E"]
        self.art = [[1 for x in range(7)] for y in range(7)]
        
        self.color = 1
        self.pallet_canvas = tk.Canvas(self.root, bg='#ffffff')
        self.pallet_canvas.place(x=25, y=25, width=400, height=100)

        self.art_canvas = tk.Canvas(self.root, bg='#ffffff')
        self.art_canvas.place(x=65, y=135, width=420, height=420)
        self.art_canvas.bind('<Button-1>', self.draw)

        self.preview_canvas = tk.Canvas(self.root, bg='#ffffff')
        self.preview_canvas.place(x=440, y=25, width=100, height=100)

        self.draw_pallet()
        self.draw_art_canvas()

        #save button
        self.save_button = tk.Button(self.root, text='Save', command=self.save)
        self.save_button.place(x=150, y=560, width=100, height=35)

        #clear button
        self.clear_button = tk.Button(self.root, text='Clear', command=self.clear)
        self.clear_button.place(x=300, y=560, width=100, height=35)
    
    def clear(self):
        self.art = [[1 for x in range(7)] for y in range(7)]
        self.draw_art_canvas()
        self.draw_preview()
    
    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        valueScaled = float(value - leftMin) / float(leftSpan)
        return rightMin + (valueScaled * rightSpan)

    def draw_pallet(self):
        for y in range(0, 100, 50):
            for x in range(0, 400, 50):
                self.pallet_canvas.create_rectangle(x, y, x+50, y+50, fill=self.colors[int((y/50*8)+x/50)])
        
        ccp = [self.color%8*50, int(self.color/8)*50]
        self.pallet_canvas.create_rectangle(ccp[0], ccp[1], ccp[0]+50, ccp[1]+50, outline='#000000', width=2)

        self.pallet_canvas.bind('<Button-1>', self.set_color)

    def set_color(self, event):
        self.color = int(event.x/50) + int(event.y/50)*8
        self.draw_pallet()
        self.draw_preview()

    def draw_art_canvas(self):
        for y in range(7):
            for x in range(7):
                if self.art[y][x] == 1:
                    self.art_canvas.create_rectangle(x*60+1, y*60+1, x*60+60, y*60+60, fill="#ffffff")
                else:
                    self.art_canvas.create_rectangle(x*60+1, y*60+1, x*60+60, y*60+60, fill="#191919")
                self.art_canvas.create_rectangle(x*60, y*60, x*60+60, y*60+60, outline="#000000", width=0.5)
    
    def draw(self, event):
        x = int(event.x/60)
        y = int(event.y/60)
        current = self.art[y][x]
        if current == 0:
            self.art[y][x] = 1
        else:
            self.art[y][x] = 0
        self.draw_art_canvas()
        self.draw_preview()

    def draw_preview(self):
        width = self.translate(1, 0, 7, 0, 100)
        for y in range(7):
            for x in range(7):
                x_ = self.translate(x, 0, 7, 0, 100)
                y_ = self.translate(y, 0, 7, 0, 100)
                if self.art[y][x] == 1:
                    self.preview_canvas.create_rectangle(x_, y_, x_+width, y_+width, fill=self.colors[self.color])
                else:
                    self.preview_canvas.create_rectangle(x_, y_, x_+width, y_+width, fill="#191919")
                self.preview_canvas.create_rectangle(x_, y_, x_+width, y_+width, outline=self.colors[self.color], width=0.5)

    def save(self):
        second_window = tk.Toplevel(self.root)
        second_window.title('cel7 Art Editor')
        second_window.geometry('450x300')
        second_window.resizable(False, False)
        second_window.configure(background='#505050')
        second_window.focus_force()

        text_box = tk.Text(second_window, bg='#ffffff', fg='#000000', font=('Arial', 12))
        text_box.place(x=25, y=25, width=400, height=200)
        art = ""
        for y in range(7):
            for x in range(7):
                art += str(self.art[y][x]) + " "
            art += '\n'
        text_box.insert(tk.END, art)
        text_box.configure(state='disabled')
        button = tk.Button(second_window, text='Copy to Clipboard', command=lambda: self.copy_to_clip(art))
        button.place(x=165, y=250, width=150, height=25)


    def copy_to_clip(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()