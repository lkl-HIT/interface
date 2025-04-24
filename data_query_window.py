# 数据查询 Toplevel 窗口
import tkinter as tk
from tkinter import ttk

# 导入各个标签页的内容类
from pressure_machine_screen import PressureMachineScreen
from universal_machine_screen import UniversalMachineScreen
from sampling_test_screen import SamplingTestScreen

class DataQueryWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.title("数据查询")
        # 设置窗口初始大小和位置 (可以根据内容调整)
        self.geometry("900x600+150+150") # 宽度x高度+左上角x+左上角y
        self.minsize(600, 400) # 设置最小尺寸

        # --- 创建 Notebook (标签页控件) --- 
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- 创建并添加标签页 --- 
        # 1. 万能机数据 (默认显示)
        self.universal_frame = ttk.Frame(self.notebook) # 为每个标签页创建一个 Frame
        self.notebook.add(self.universal_frame, text=" 万能机数据 ") # 加空格让标签好看些
        universal_screen = UniversalMachineScreen(self.universal_frame)
        universal_screen.pack(fill=tk.BOTH, expand=True) # 让内容填满标签页 Frame

        # 2. 压力机数据
        self.pressure_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pressure_frame, text=" 压力机数据 ")
        pressure_screen = PressureMachineScreen(self.pressure_frame)
        pressure_screen.pack(fill=tk.BOTH, expand=True)

        # 3. 见证取样试验
        self.sampling_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.sampling_frame, text=" 见证取样试验 ")
        sampling_screen = SamplingTestScreen(self.sampling_frame)
        sampling_screen.pack(fill=tk.BOTH, expand=True)

        # --- 可以添加其他通用控件，例如底部的关闭按钮 --- 
        close_button = ttk.Button(self, text="关闭", command=self.destroy)
        close_button.pack(pady=5)
        
        # --- 提升窗口到最前 --- 
        self.lift()
        self.focus_set() # 设置焦点

# --- 用于独立测试 DataQueryWindow 的代码 --- 
if __name__ == '__main__':
    # 创建一个模拟的父窗口 (通常是 App 或 MainScreen)
    root = tk.Tk()
    root.title("主窗口 (测试用)")
    root.geometry("200x100")

    def open_query():
        query_win = DataQueryWindow(root)
    
    open_button = ttk.Button(root, text="打开数据查询窗口", command=open_query)
    open_button.pack(pady=20)
    
    root.mainloop() 