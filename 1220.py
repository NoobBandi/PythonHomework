import matplotlib
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')

def load_data_from_txt(file_path):
    values = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for index, line in enumerate(file):
                line = line.strip()
                if line:
                    try:
                        value = float(line)
                        values.append(value)
                    except ValueError:
                        print(f'警告: 第 {index + 1} 行不是數值，已跳過。')
        return values
    except Exception as e:
        messagebox.showerror('錯誤', f'讀取檔案失敗: {e}')
        return None
    
def genrate_time_labels(data_length, interval_ms=1):
    return [i * interval_ms for i in range(data_length)]

def plot_data(time_labels, values, frame):
    if not time_labels or not values:
        messagebox.showwarning('警告', '無資料可繪製。')
        return
    
    for widget in frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(time_labels, values, marker='o', linestyle='-', color='blue', label='數據')
    ax.set_xlabel('時間 (ms)')
    ax.set_ylabel('數值')
    ax.set_title('資料視覺化 (每筆間隔 1ms)')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()

def select_file(entry_widget):
    file_path = filedialog.askopenfilename(title='選擇 .txt 檔案', filetypes=[('Text files', '*.txt')])
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)

def main():
    root = tk.Tk()
    root.title('資料視覺化 (固定間隔 1ms)')
    root.geometry('900x600')

    frame_top = tk.Frame(root, padx=10, pady=10)
    frame_top.pack(fill=tk.X)

    tk.Label(frame_top, text='選擇 .txt 檔案:').pack(side=tk.LEFT, padx=5)
    entry_file = tk.Entry(frame_top, width=50)
    entry_file.pack(side=tk.LEFT, padx=5)
    btn_browser = tk.Button(frame_top, text='瀏覽', command=lambda: select_file(entry_file))
    btn_browser.pack(side=tk.LEFT, padx=5)

    frame_plot = tk.Frame(root, padx=10, pady=10, relief=tk.SUNKEN, bd=2)
    frame_plot.pack(fill=tk.BOTH, expand=True)

    def load_and_plot():
        file_path = entry_file.get().strip()
        if not file_path:
            messagebox.showwarning('警告', '請選擇一個檔案。')
            return
        
        if not os.path.exists(file_path):
            messagebox.showwarning('警告', '檔案不存在。')
            return
        
        values = load_data_from_txt(file_path)
        if values:
            time_labels = genrate_time_labels(len(values), interval_ms=1)
            plot_data(time_labels, values, frame_plot)
        else:
            messagebox.showwarning('警告', '無法讀取資料。')

    btn_plot = tk.Button(frame_top, text='繪製圖表', command=load_and_plot)
    btn_plot.pack(side=tk.RIGHT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()