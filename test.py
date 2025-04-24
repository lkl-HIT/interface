import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class ConcreteTestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("在线压值监测系统")
        self.root.geometry("1000x700")
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建顶部数据显示区域
        self.create_top_display()
        
        # 创建中间部分（图表和测试信息）
        self.create_middle_section()
        
        # 创建底部按钮区域
        self.create_bottom_buttons()

    def create_top_display(self):
        top_frame = ttk.Frame(self.main_frame)
        top_frame.pack(fill=tk.X, pady=5)
        
        # 创建三个数据显示框
        displays = [("荷载", "0.00"), ("AID", "0.00"), ("位移", "0.00")]
        for i, (label, value) in enumerate(displays):
            frame = ttk.Frame(top_frame)
            frame.pack(side=tk.LEFT, padx=10)
            
            ttk.Label(frame, text=label).pack()
            value_label = ttk.Label(frame, text=value, 
                                  background="blue", foreground="white",
                                  width=10, anchor="center")
            value_label.pack(pady=2)
        
        # 清零按钮
        ttk.Button(top_frame, text="清零").pack(side=tk.RIGHT, padx=10)

    def create_middle_section(self):
        middle_frame = ttk.Frame(self.main_frame)
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建图表区域
        self.create_plot(middle_frame)
        
        # 创建右侧测试信息区域
        self.create_test_info(middle_frame)

    def create_plot(self, parent):
        plot_frame = ttk.LabelFrame(parent, text="实时数据显示")
        plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.grid(True)
        ax.set_xlim(0, 30)
        ax.set_ylim(0, 100)
        
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_test_info(self, parent):
        info_frame = ttk.LabelFrame(parent, text="试验信息")
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        # 测试信息输入字段
        fields = [
            ("试验类型:", "承托板强度-抗压试验"),
            ("样品编号:", ""),
            ("工程部位:", ""),
            ("强度等级:", "C15"),
            ("试体尺寸(mm):", "150×150×150"),
            ("支座间跨度(mm):", "500"),
            ("试件龄期(天):", "28"),
            ("试件个数:", "3"),
            ("试验速度(kN/S):", ""),
            ("执行标准:", "JTG 3420-2020"),
        ]
        
        for label, default in fields:
            row = ttk.Frame(info_frame)
            row.pack(fill=tk.X, pady=2)
            ttk.Label(row, text=label).pack(side=tk.LEFT)
            if default:
                combo = ttk.Combobox(row, width=20, values=[default])
                combo.set(default)
                combo.pack(side=tk.RIGHT)
            else:
                ttk.Entry(row, width=20).pack(side=tk.RIGHT)
        
        # 是否监测曲线选项
        curve_frame = ttk.Frame(info_frame)
        curve_frame.pack(fill=tk.X, pady=5)
        ttk.Label(curve_frame, text="是否监测曲线:").pack(side=tk.LEFT)
        ttk.Radiobutton(curve_frame, text="是").pack(side=tk.LEFT)
        ttk.Radiobutton(curve_frame, text="否").pack(side=tk.LEFT)


    def create_bottom_buttons(self):
        bottom_frame = ttk.Frame(self.main_frame)
        bottom_frame.pack(fill=tk.X, pady=5)
        
        buttons = ["开始试验", "终止试验", "数据审核", "结件上升", "结件下降"]
        for text in buttons:
            ttk.Button(bottom_frame, text=text).pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConcreteTestGUI(root)
    root.mainloop()
