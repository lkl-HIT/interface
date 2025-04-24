# 登录界面代码
import tkinter as tk
from tkinter import ttk
# from PIL import Image, ImageTk # 不再需要 Pillow

class LoginScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller # 用于调用 App 类的方法，例如切换界面
        self.parent = parent
        
        # 设置整体 Frame 样式 (可选，用于模拟背景色等)
        style = ttk.Style()
        # 注意：背景色等样式在 Windows XP + Tkinter 上的效果可能有限
        style.configure('LoginScreen.TFrame', background='#ECECEC') # 示例浅灰色背景
        self.configure(style='LoginScreen.TFrame')
        
        # --- 使用 Grid 布局来定位控件 --- 
        # 使中心列可伸展，将登录框推到中间
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        # 使包含登录框的行上下也有空间
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # --- 登录表单容器 Frame --- 
        # 使用 LabelFrame 可以添加边框和标题 (可选)
        login_frame = ttk.LabelFrame(self, text="用户登录", padding=(20, 10))
        # 将登录框放置在中间的单元格
        login_frame.grid(row=1, column=1, sticky="nsew") 

        # --- 登录名 --- 
        username_label = ttk.Label(login_frame, text="登录名:")
        # 使用 grid 在 login_frame 内部布局
        username_label.grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.username_entry = ttk.Entry(login_frame, width=25) # 调整宽度
        self.username_entry.grid(row=0, column=1, padx=5, pady=10)

        # --- 密  码 --- 
        password_label = ttk.Label(login_frame, text="密  码:")
        password_label.grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.password_entry = ttk.Entry(login_frame, show="*", width=25) # 调整宽度
        self.password_entry.grid(row=1, column=1, padx=5, pady=10)

        # --- 按钮容器 Frame --- 
        button_frame = ttk.Frame(login_frame)
        # 让按钮容器跨越两列，并在下方显示
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        login_button = ttk.Button(button_frame, text="登录", command=self.login, width=10)
        # 使用 pack 在 button_frame 内部布局按钮
        login_button.pack(side=tk.LEFT, padx=10)
        
        cancel_button = ttk.Button(button_frame, text="取消", command=self.cancel_login, width=10)
        cancel_button.pack(side=tk.LEFT, padx=10)
        
        # --- 让 login_frame 内部的列也能适当伸展 --- 
        login_frame.columnconfigure(1, weight=1)
        
        # --- 设置焦点到用户名输入框 --- 
        self.username_entry.focus_set()

    def login(self):
        """处理登录逻辑"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        print("登录尝试: 用户名=", username, "密码=", password) # 调试信息
        
        # --- 在此添加实际的登录验证逻辑 --- 
        # 例如: 检查用户名和密码是否正确
        # if username == "admin" and password == "password":
        if True: # 临时：总是认为登录成功
            print("登录成功")
            # 验证成功后，切换到主界面
            self.controller.show_frame("MainScreen") # 取消注释以启用跳转
        # else:
        #     print("登录失败")
        #     # 可以显示错误消息
        #     from tkinter import messagebox
        #     messagebox.showerror("登录失败", "用户名或密码错误")
        #     # 清空密码框并重新设置焦点
        #     self.password_entry.delete(0, tk.END)
        #     self.password_entry.focus_set()

    def cancel_login(self):
        """处理取消登录操作，例如关闭程序"""
        print("取消登录，关闭程序")
        self.controller.destroy() # 直接关闭整个应用程序

# --- 用于独立测试 LoginScreen 的代码 --- 
if __name__ == '__main__':
    # 创建一个模拟的 App 控制器用于测试
    class MockController(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("登录界面测试")
            # 可以设置一个初始大小
            self.geometry("400x250") 
            self.resizable(False, False) # 登录界面通常固定大小
            # 让窗口内容随窗口缩放 (虽然这里不允许缩放)
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
        
        def show_frame(self, page_name):
            print("控制器请求切换到:", page_name)
            # 在测试模式下，切换时可以简单打印信息或关闭
            if page_name == "MainScreen":
                print("模拟切换到主界面成功！")
                self.destroy() # 测试成功后关闭

        def destroy(self):
            print("模拟控制器关闭")
            super().destroy()
            
    controller = MockController()
    # 将 MockController 作为 parent 和 controller 传递
    login_screen = LoginScreen(controller, controller) 
    # 使用 grid 并让其填充整个窗口
    login_screen.grid(row=0, column=0, sticky="nsew") 
    controller.mainloop() 