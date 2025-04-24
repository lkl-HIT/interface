# 主界面代码 (核心操作界面)
import tkinter as tk
from tkinter import ttk

# 导入数据查询窗口类
from data_query_window import DataQueryWindow
# 导入续采试验窗口类
from continuous_sampling_window import ContinuousSamplingWindow

# 导入 matplotlib 相关库
# 注意：确保已安装 matplotlib==2.2.5
try:
    import matplotlib
    matplotlib.use('TkAgg') # 明确指定 Tkinter 后端
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    print("错误：matplotlib 未安装或版本不兼容 (需要 matplotlib==2.2.5)")
    MATPLOTLIB_AVAILABLE = False

class MainScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller 
        self.parent = parent
        self.data_query_win = None # 初始化查询窗口引用
        self.cont_sampling_win = None # 添加续采窗口引用
        
        # --- 配置主框架的 Grid 布局 --- 
        self.rowconfigure(1, weight=1) # 让中间行 (图表和信息区) 占据主要空间
        self.columnconfigure(0, weight=1) # 让左列 (图表) 可伸展
        self.columnconfigure(1, weight=0) # 右列 (信息区) 固定宽度
        
        # --- 创建界面区域 --- 
        self.create_top_display_area()
        self.create_center_area()
        self.create_bottom_button_area()
        self.create_status_bar()

    def create_top_display_area(self):
        """创建顶部数据显示区和清零按钮"""
        top_frame = ttk.Frame(self, padding=(10, 5))
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        style = ttk.Style()
        
        # --- 标志位，记录自定义样式是否成功定义 --- 
        use_custom_display_lf_style = False
        use_custom_display_label_style = False
        use_custom_unit_label_style = False

        # --- 尝试定义并配置自定义样式 --- 
        try:
            # LabelFrame 样式
            style.layout('DataDisplay.TLabelFrame', style.layout('TLabelFrame'))
            # 成功定义布局后，再配置选项
            style.configure('DataDisplay.TLabelFrame', background='lightgrey') 
            use_custom_display_lf_style = True # 标记成功
            
            # 数据 Label 样式
            style.layout('DataDisplay.TLabel', style.layout('TLabel'))
            style.configure('DataDisplay.TLabel', 
                            background='blue', foreground='white', 
                            font=('Arial', 12, 'bold'), anchor='center', padding=(5, 2))
            use_custom_display_label_style = True # 标记成功

            # 单位 Label 样式
            style.layout('Unit.TLabel', style.layout('TLabel'))
            style.configure('Unit.TLabel', background='lightgrey', foreground='black')
            use_custom_unit_label_style = True # 标记成功
            
        except tk.TclError as e:
            # 如果布局失败，打印警告，标志位保持 False
            print("警告：设置 ttk 布局或样式时出错: {}. 将使用默认样式。".format(e))

        # --- 创建控件，根据标志位决定是否使用自定义样式 --- 
        displays = [("荷载", "kN"), ("强度", "MPa"), ("速率", "kN/s")]
        self.data_labels = {} 

        for i, (name, unit) in enumerate(displays):
            # 创建 LabelFrame
            lf_kwargs = {"text": name}
            if use_custom_display_lf_style:
                lf_kwargs["style"] = 'DataDisplay.TLabelFrame'
            frame = ttk.LabelFrame(top_frame, **lf_kwargs)
            frame.pack(side=tk.LEFT, padx=10)
            
            # 创建数值 Label
            value_label_kwargs = {"text": "0.00", "width": 8}
            if use_custom_display_label_style:
                value_label_kwargs["style"] = 'DataDisplay.TLabel'
            else:
                 # 备用：如果自定义样式失败，尝试手动配置基本外观
                 value_label_kwargs["background"] = 'blue'
                 value_label_kwargs["foreground"] = 'white'
                 value_label_kwargs["font"] = ('Arial', 12, 'bold')
                 value_label_kwargs["anchor"] = 'center'
                 value_label_kwargs["padding"] = (5,2)
            value_label = ttk.Label(frame, **value_label_kwargs)
            value_label.pack(side=tk.LEFT)
            self.data_labels[name] = value_label
            
            # 创建单位 Label
            unit_label_kwargs = {"text": unit}
            if use_custom_unit_label_style:
                unit_label_kwargs["style"] = 'Unit.TLabel'
            else:
                # 备用：手动配置
                unit_label_kwargs["background"] = 'lightgrey' # 可能无效，取决于系统主题
                unit_label_kwargs["foreground"] = 'black'
            unit_label = ttk.Label(frame, **unit_label_kwargs)
            unit_label.pack(side=tk.LEFT, padx=5)
            
        # 清零按钮 (通常不需要特殊样式)
        zero_button = ttk.Button(top_frame, text="清零", command=self.zero_data)
        zero_button.pack(side=tk.RIGHT, padx=20)

    def create_center_area(self):
        """创建中间的图表区和试验信息区"""
        center_frame = ttk.Frame(self, padding=(0, 5))
        center_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        center_frame.rowconfigure(0, weight=1)
        center_frame.columnconfigure(0, weight=1) # 图表区可伸展
        center_frame.columnconfigure(1, weight=0) # 信息区固定宽度

        # 创建图表区
        self.create_plot_area(center_frame)
        # 创建试验信息区
        self.create_test_info_area(center_frame)

    def create_plot_area(self, parent):
        """创建左侧的 Matplotlib 图表区"""
        plot_frame = ttk.LabelFrame(parent, text="实时数据显示") # LabelFrame 的标题可以显示中文
        plot_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=5)
        plot_frame.rowconfigure(0, weight=1)
        plot_frame.columnconfigure(0, weight=1)
        
        if MATPLOTLIB_AVAILABLE:
            # --- 设置 Matplotlib 支持中文 --- 
            try:
                # 尝试设置中文字体，SimHei 在很多 Windows 系统上可用
                matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei'] 
                # 解决更改字体后负号显示为方块的问题
                matplotlib.rcParams['axes.unicode_minus'] = False 
            except Exception as e:
                print("警告：设置 Matplotlib 中文字体失败: {}".format(e))
            
            fig = Figure(figsize=(6, 4)) 
            self.ax = fig.add_subplot(111)
            # --- 现在设置中文标题和标签 --- 
            self.ax.set_title("实时数据显示") # Matplotlib 内部标题
            self.ax.set_xlabel("时间(s)") # 修改为中文和英文单位
            self.ax.set_ylabel("力值(kN)") # 修改为中文和英文单位
            self.ax.grid(True)
            self.ax.set_xlim(0, 30) 
            self.ax.set_ylim(0, 100) 
            
            self.canvas = FigureCanvasTkAgg(fig, master=plot_frame)
            canvas_widget = self.canvas.get_tk_widget()
            canvas_widget.grid(row=0, column=0, sticky="nsew")
            self.canvas.draw() 
        else:
            fallback_label = ttk.Label(plot_frame, text="Matplotlib 图表加载失败", foreground="red")
            fallback_label.grid(row=0, column=0, padx=20, pady=20)

    def create_test_info_area(self, parent):
        """创建右侧的试验信息表单"""
        info_frame = ttk.LabelFrame(parent, text="试验信息", width=300) # 尝试固定宽度
        info_frame.grid(row=0, column=1, sticky="ns", padx=(5, 10), pady=5)
        info_frame.grid_propagate(False) # 防止子控件撑开宽度
        
        # 使用内部 Frame 来容纳信息字段，方便滚动（如果需要）
        inner_frame = ttk.Frame(info_frame, padding=5)
        inner_frame.pack(fill=tk.BOTH, expand=True)

        # 试验信息字段 (参照截图)
        fields = {
            "试验类型:": "水泥混凝土抗压试验",
            "样品编号:": "",
            "工程部位:": "",
            "强度等级:": "C15",
            "试件尺寸(mm):": "150×150×150",
            "支座间跨度(mm):": "300", # 截图显示300
            "试件龄期(天):": "28",
            "试件块数:": "3", # 截图显示3
            "加载速度(kN/S):": "9", # 截图显示9
            "执行标准:": "JTG 3420-2020"
        }
        self.info_entries = {} # 存储 Entry 或 Label 以便读写

        row_num = 0
        for label_text, default_value in fields.items():
            lbl = ttk.Label(inner_frame, text=label_text)
            lbl.grid(row=row_num, column=0, sticky="w", padx=5, pady=3)
            
            # 对于某些字段可能用 Combobox 或只读 Label
            if label_text in ["试验类型:", "强度等级:", "试件尺寸(mm):", "执行标准:"]:
                # 使用 Combobox 模拟下拉选择或固定文本
                combo = ttk.Combobox(inner_frame, width=20, values=[default_value])
                combo.set(default_value)
                combo.grid(row=row_num, column=1, sticky="ew", padx=5, pady=3)
                self.info_entries[label_text] = combo
            else:
                entry = ttk.Entry(inner_frame, width=20)
                entry.insert(0, default_value)
                entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=3)
                self.info_entries[label_text] = entry
            row_num += 1
            
        # 获取按钮
        get_button = ttk.Button(inner_frame, text="获取", width=5, command=self.get_sample_info)
        get_button.grid(row=1, column=2, padx=5, pady=3) # 放在样品编号旁边

        # 是否监理见证 (单选按钮)
        supervision_frame = ttk.Frame(inner_frame)
        supervision_frame.grid(row=row_num, column=0, columnspan=3, sticky="w", pady=5)
        ttk.Label(supervision_frame, text="是否监理见证:").pack(side=tk.LEFT, padx=5)
        self.supervision_var = tk.StringVar(value="是") # 默认选是
        rb_yes = ttk.Radiobutton(supervision_frame, text="是", variable=self.supervision_var, value="是")
        rb_yes.pack(side=tk.LEFT)
        rb_no = ttk.Radiobutton(supervision_frame, text="否", variable=self.supervision_var, value="否")
        rb_no.pack(side=tk.LEFT, padx=5)
        row_num += 1
        
        # 结果显示列表 (使用 Treeview)
        result_frame = ttk.Frame(inner_frame)
        result_frame.grid(row=row_num, column=0, columnspan=3, sticky="nsew", pady=(10, 0))
        result_frame.rowconfigure(0, weight=1)
        result_frame.columnconfigure(0, weight=1)
        
        columns = ("#0", "force", "strength")
        self.result_tree = ttk.Treeview(result_frame, columns=columns[1:], show="headings", height=5)
        self.result_tree.heading("force", text="力值(kN)")
        self.result_tree.heading("strength", text="强度(MPa)")
        self.result_tree.column("force", width=80, anchor="center")
        self.result_tree.column("strength", width=80, anchor="center")
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        
        self.result_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # 让结果列表区域可以扩展
        inner_frame.rowconfigure(row_num, weight=1)
        inner_frame.columnconfigure(1, weight=1) # 让输入/下拉框列可扩展

    def create_bottom_button_area(self):
        """创建底部的操作按钮区域"""
        button_frame = ttk.Frame(self, padding=(10, 5))
        button_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        
        buttons = [
            ("开始试验", self.start_test),
            ("续采试验", self.open_continuous_sampling),
            ("数据查询", self.open_data_query_window),
            ("丝杆上升", self.screw_up),
            ("丝杆下降", self.screw_down)
        ]
        
        button_inner_frame = ttk.Frame(button_frame)
        button_inner_frame.pack() 

        for text, command in buttons:
            button = ttk.Button(button_inner_frame, text=text, command=command, width=12)
            button.pack(side=tk.LEFT, padx=10, pady=5)

    def create_status_bar(self):
        """创建最底部的状态栏"""
        status_frame = ttk.Frame(self, relief=tk.SUNKEN, padding=2)
        status_frame.grid(row=3, column=0, columnspan=2, sticky="ew")
        
        status_items = ["系统状态:", "联机状态:", "控制状态:", "错误提示:"]
        self.status_labels = {} 
        
        for i, item_text in enumerate(status_items):
            ttk.Label(status_frame, text=item_text).pack(side=tk.LEFT, padx=(10 if i == 0 else 20, 0))
            status_label = ttk.Label(status_frame, text="--", width=15, anchor="w")
            status_label.pack(side=tk.LEFT)
            self.status_labels[item_text.split(':')[0]] = status_label # 存储 Label
            if item_text == "错误提示:":
                 status_label.config(width=40) # 给错误提示更宽的空间

    # --- 按钮和操作的占位符命令 --- 
    def zero_data(self):
        print("命令: 清零数据")
        for label in self.data_labels.values():
            label.config(text="0.00")
        # TODO: 可能还需要清零图表和内部状态

    def get_sample_info(self):
        print("命令: 获取样品信息")
        # TODO: 实现获取样品信息的逻辑, 可能需要与硬件或数据库交互
        sample_id = self.info_entries["样品编号:"].get()
        print("获取编号:", sample_id)

    def start_test(self):
        print("命令: 开始试验")
        # TODO: 实现开始试验的逻辑 (更新状态栏, 控制硬件, 更新图表等)
        self.status_labels["系统状态"].config(text="试验进行中")
        self.status_labels["控制状态"].config(text="自动控制")

    def screw_up(self):
        print("命令: 丝杆上升")
        # TODO: 实现控制丝杆上升的逻辑
        self.status_labels["控制状态"].config(text="手动上升")

    def screw_down(self):
        print("命令: 丝杆下降")
        # TODO: 实现控制丝杆下降的逻辑
        self.status_labels["控制状态"].config(text="手动下降")
        
    def open_data_query_window(self):
        """打开数据查询 Toplevel 窗口 (如果尚未打开)"""
        if self.data_query_win is None or not self.data_query_win.winfo_exists():
            # 如果窗口不存在或已被销毁，则创建一个新的
            self.data_query_win = DataQueryWindow(self) # parent 可以是 self (MainScreen)
            print("数据查询窗口已创建")
        else:
            # 如果窗口已存在，则将其提到最前面
            self.data_query_win.lift()
            self.data_query_win.focus_set()
            print("数据查询窗口已存在，提到最前")
            
    def open_continuous_sampling(self):
        """打开续采试验 Toplevel 窗口 (如果尚未打开)"""
        if self.cont_sampling_win is None or not self.cont_sampling_win.winfo_exists():
            self.cont_sampling_win = ContinuousSamplingWindow(self) 
            print("续采试验窗口已创建")
        else:
            self.cont_sampling_win.lift()
            self.cont_sampling_win.focus_set()
            print("续采试验窗口已存在，提到最前")

    # --- 其他辅助方法 (例如更新图表, 更新状态等) --- 
    def update_plot(self, x_data, y_data):
        """示例：更新图表数据"""
        if MATPLOTLIB_AVAILABLE:
            self.ax.clear() # 清除旧图
            self.ax.plot(x_data, y_data)
            self.ax.set_title("实时数据显示")
            self.ax.set_xlabel("单位(s)")
            self.ax.set_ylabel("单位(kN)")
            self.ax.grid(True)
            # 可能需要重新设置坐标轴范围
            # self.ax.set_xlim(...) 
            # self.ax.set_ylim(...)
            self.canvas.draw()
        else:
            print("无法更新图表: Matplotlib 不可用")

    def update_status(self, system="--", connection="--", control="--", error="--"):
         """更新状态栏信息"""
         self.status_labels["系统状态"].config(text=system)
         self.status_labels["联机状态"].config(text=connection)
         self.status_labels["控制状态"].config(text=control)
         self.status_labels["错误提示"].config(text=error)

# --- 用于独立测试 MainScreen 的代码 --- 
if __name__ == '__main__':
    # 创建一个模拟的 App 控制器用于测试
    class MockController(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("主界面测试")
            self.geometry("1000x750") # 匹配 App 中的大小
             # --- 创建模拟菜单栏 (因为独立测试没有 App 的菜单) --- 
            self.menu_bar = tk.Menu(self)
            self.config(menu=self.menu_bar)
            help_menu = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label="帮助", menu=help_menu)
            help_menu.add_command(label="关于 (Test)", 
                                  command=lambda: print("独立测试中的关于"))
                                  
            # 让窗口内容随窗口缩放 
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
        
        def show_frame(self, page_name):
            print("控制器请求切换到子界面:", page_name)
            # 可以弹出一个简单窗口模拟切换
            from tkinter import messagebox
            messagebox.showinfo("导航测试", "请求切换到: {}".format(page_name))

        def destroy(self):
            print("控制器请求关闭程序")
            super().destroy()
            
    controller = MockController()
    main_screen = MainScreen(controller, controller)
    main_screen.grid(row=0, column=0, sticky="nsew") # 使用 grid 替换 pack
    controller.mainloop() 