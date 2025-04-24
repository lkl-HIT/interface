# 主应用程序入口
import tkinter as tk
from tkinter import ttk

# 导入各个界面模块
from login_screen import LoginScreen 
from main_screen import MainScreen
# 不再直接管理这些，它们是 DataQueryWindow 的一部分
# from pressure_machine_screen import PressureMachineScreen
# from universal_machine_screen import UniversalMachineScreen
# from sampling_test_screen import SamplingTestScreen
# from continuous_sampling_screen import ContinuousSamplingScreen # 移除旧的 Frame 类导入

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("测试数据管理系统")
        
        # --- 创建主菜单栏 --- 
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        self.create_menus() # 调用菜单创建方法
        
        # --- 使窗口大小可调整 --- 
        # 让根窗口的行列可伸展，这样内部的 Frame 也能正确伸展
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # --- 容器，用于堆叠不同的界面 Frame --- 
        container = ttk.Frame(self)
        # 使用 grid 布局管理器允许容器随窗口缩放
        container.grid(row=0, column=0, sticky="nsew") 
        # 让容器内部的行列也可伸展，确保 Frame 能填满容器
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # --- 初始化并存储*直接管理*的界面 --- 
        self.pages_to_load = (
            LoginScreen, 
            MainScreen, 
            # PressureMachineScreen, # 移除
            # UniversalMachineScreen, # 移除
            # SamplingTestScreen, # 移除
            # ContinuousSamplingScreen # 确认移除
        )
        
        for F in self.pages_to_load:
            page_name = F.__name__
            # 将 self (App 实例) 传递给每个界面作为 controller
            frame = F(parent=container, controller=self) 
            self.frames[page_name] = frame
            # 使用 grid 布局所有 frame，初始不可见，通过 tkraise() 显示
            frame.grid(row=0, column=0, sticky="nsew")

        # --- 启动时显示登录界面 --- 
        self.show_frame("LoginScreen")

    def create_menus(self):
        """在 App 层面创建主菜单栏结构"""
        # 文件菜单
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="打开", command=self.file_open) # 示例
        file_menu.add_command(label="保存", command=self.file_save) # 示例
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.quit_app)

        # --- 修改数据查询菜单命令 --- 
        data_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="数据查询", menu=data_menu)
        # 命令现在调用 MainScreen 实例的方法来打开 Toplevel 窗口
        # 注意: 需要确保 self.frames['MainScreen'] 已经创建
        data_menu.add_command(label="打开查询窗口", 
                              command=self.open_main_screen_data_query) # 使用新方法
        # data_menu.add_command(label="压力机数据", 
        #                       command=lambda: self.frames['MainScreen'].open_data_query_window()) # 旧方式，直接调用
        # data_menu.add_command(label="万能机数据", ...)
        # data_menu.add_command(label="见证取样", ...)
        # (子菜单项可能不再需要，或者它们可以聚焦到 Toplevel 窗口的特定标签页)

        # --- 修改续采试验菜单命令 (确认调用 MainScreen 方法) --- 
        continue_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="续采试验", menu=continue_menu)
        continue_menu.add_command(label="开始续采", 
                                  command=self.open_main_screen_continuous_sampling) # 确认调用此方法

        # 系统管理菜单 (示例)
        system_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="系统管理", menu=system_menu)
        system_menu.add_command(label="用户管理", command=self.manage_users) 
        system_menu.add_command(label="参数设置", command=self.system_settings)

        # 帮助菜单 (示例)
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)

    def show_frame(self, page_name):
        '''显示指定名称的 Frame，并调整窗口属性和菜单'''
        if page_name not in self.frames:
            print("错误：尝试显示未知的 Frame:", page_name)
            return
            
        frame = self.frames[page_name]
        
        # --- 根据目标界面调整窗口大小和可调整性 --- 
        if page_name == "LoginScreen":
            # 登录界面固定大小
            self.update_idletasks() # 确保组件尺寸计算准确
            req_width = frame.winfo_reqwidth()
            req_height = frame.winfo_reqheight()
            # 稍微给点边距，防止控件挤在一起
            self.geometry("{}x{}".format(req_width + 20, req_height + 20))
            self.resizable(False, False)
            # 隐藏菜单栏
            self.config(menu=tk.Menu(self)) # 设置一个空菜单实例来隐藏
        elif page_name == "MainScreen":
            # 主界面较大且可调整大小
            self.geometry("1000x700") 
            self.resizable(True, True)
            # 恢复主界面的菜单栏 (假设 MainScreen 会设置它)
            if hasattr(self.frames['MainScreen'], 'menu_bar'):
                self.config(menu=self.frames['MainScreen'].menu_bar)
        else:
            # 其他功能界面，设置为较大尺寸且可调整
            # （可以为特定界面设置不同的大小）
            self.geometry("1000x700") 
            self.resizable(True, True)
            # 确保显示主菜单栏
            self.config(menu=self.menu_bar)

        # 将请求的 Frame 提升到最前面显示
        frame.tkraise()

    # --- 菜单命令的占位符 (部分移至 App 类) --- 
    def file_open(self):
        print("命令：文件 -> 打开")
        # TODO: 实现文件打开逻辑

    def file_save(self):
        print("命令：文件 -> 保存")
        # TODO: 实现文件保存逻辑

    def quit_app(self):
        print("命令：退出应用程序")
        self.destroy()

    def manage_users(self):
        print("命令：系统管理 -> 用户管理")
        # TODO: 实现用户管理功能 (可能需要新界面)

    def system_settings(self):
        print("命令：系统管理 -> 参数设置")
        # TODO: 实现参数设置功能 (可能需要新界面)

    def show_about(self):
        print("命令：帮助 -> 关于")
        from tkinter import messagebox
        messagebox.showinfo("关于", "测试数据管理系统 v1.0\n基于 Python/Tkinter")

    def open_main_screen_data_query(self):
        """菜单命令：调用 MainScreen 打开数据查询窗口"""
        if 'MainScreen' in self.frames and self.frames['MainScreen'].winfo_ismapped():
             self.frames['MainScreen'].open_data_query_window()
        else:
            print("错误：主界面尚未显示，无法打开数据查询窗口")
            # 或者可以先显示主界面: self.show_frame('MainScreen') 然后再调用
            
    def open_main_screen_continuous_sampling(self):
        """菜单命令：调用 MainScreen 打开续采试验窗口"""
        if 'MainScreen' in self.frames and self.frames['MainScreen'].winfo_ismapped():
            self.frames['MainScreen'].open_continuous_sampling()
        else:
            print("错误：主界面尚未显示，无法打开续采试验窗口")

# --- 应用程序启动 --- 
if __name__ == "__main__":
    app = App()
    app.mainloop() 