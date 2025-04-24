# 续采试验 Toplevel 窗口
import tkinter as tk
from tkinter import ttk

class ContinuousSamplingWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.title("未完成试验列表-压力机")
        self.geometry("950x550+200+200") # 调整大小和位置
        self.minsize(700, 400)

        # --- 主布局：使用 PanedWindow 分割左右区域 --- 
        # PanedWindow 允许用户拖动调整左右比例
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- 创建左侧框架 (筛选和列表) --- 
        left_frame = ttk.Frame(self.paned_window, width=550) # 初始宽度
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)
        self.paned_window.add(left_frame, weight=2) # 左侧占比稍大

        self.create_left_filter_area(left_frame)
        self.create_left_treeview_area(left_frame)

        # --- 创建右侧框架 (详情) --- 
        right_frame = ttk.Frame(self.paned_window, width=350) # 初始宽度
        right_frame.rowconfigure(0, weight=1) # 让内容区可伸展
        right_frame.columnconfigure(0, weight=1)
        self.paned_window.add(right_frame, weight=1)

        self.create_right_details_area(right_frame)
        
        # --- 提升窗口 --- 
        self.lift()
        self.focus_set()

    def create_left_filter_area(self, parent):
        """创建左侧顶部的筛选区域"""
        filter_frame = ttk.Frame(parent, padding="5 5 5 5")
        filter_frame.grid(row=0, column=0, sticky="ew")

        ttk.Label(filter_frame, text="试件编号:").pack(side=tk.LEFT, padx=(0, 2))
        self.specimen_id_entry = ttk.Entry(filter_frame, width=20)
        self.specimen_id_entry.pack(side=tk.LEFT, padx=(0, 10))

        query_button = ttk.Button(filter_frame, text="查询", command=self.query_incomplete_tests)
        query_button.pack(side=tk.LEFT, padx=5)

    def create_left_treeview_area(self, parent):
        """创建左侧的未完成试验列表 Treeview"""
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        columns = ('sample_id', 'sample_name', 'project_part', 'count', 'test_time')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        self.tree.heading('sample_id', text='样品编号')
        self.tree.heading('sample_name', text='样品名称') # 截图似乎没有这列，但通常会有
        self.tree.heading('project_part', text='工程部位')
        self.tree.heading('count', text='试件数量')
        self.tree.heading('test_time', text='实验时间')

        self.tree.column('sample_id', width=150)
        self.tree.column('sample_name', width=100)
        self.tree.column('project_part', width=200)
        self.tree.column('count', width=60, anchor='center')
        self.tree.column('test_time', width=120, anchor='center')

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # --- 绑定选择事件 --- 
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.insert_sample_data()

    def create_right_details_area(self, parent):
        """创建右侧的试验信息详情区域"""
        details_labelframe = ttk.LabelFrame(parent, text="试验信息")
        details_labelframe.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        details_labelframe.columnconfigure(1, weight=1)

        # --- 试验信息字段 (只读) --- 
        info_fields = [
            "试验类型:", "样品编号:", "工程部位:", "强度等级:",
            "试件尺寸(mm):", "试件龄期(天):", "试件数量:", "执行标准:"
        ]
        self.detail_labels = {}
        for i, label_text in enumerate(info_fields):
            ttk.Label(details_labelframe, text=label_text).grid(row=i, column=0, sticky="w", padx=5, pady=3)
            value_label = ttk.Label(details_labelframe, text="---", anchor="w", relief=tk.GROOVE, padding=(2,1))
            value_label.grid(row=i, column=1, sticky="ew", padx=5, pady=3)
            self.detail_labels[label_text] = value_label
            
        # --- 小结果表 --- 
        result_frame = ttk.Frame(details_labelframe, padding=(0, 10))
        result_frame.grid(row=len(info_fields), column=0, columnspan=2, sticky="ew", pady=10)
        result_frame.columnconfigure(0, weight=1)
        
        result_columns = ("#0", "force", "strength")
        self.result_tree = ttk.Treeview(result_frame, columns=result_columns[1:], 
                                        show="headings", height=3) # 显示少量数据
        self.result_tree.heading("force", text="力值(kN)")
        self.result_tree.heading("strength", text="强度(MPa)")
        self.result_tree.column("force", width=80, anchor="center")
        self.result_tree.column("strength", width=80, anchor="center")
        self.result_tree.grid(row=0, column=0, sticky="ew")
        # (可选) 添加滚动条，如果预期行数多

        # --- 确定按钮 --- 
        confirm_button = ttk.Button(parent, text="确定", command=self.confirm_selection)
        confirm_button.grid(row=1, column=0, sticky="e", padx=10, pady=10)

    # --- 事件处理和占位符命令 --- 
    def query_incomplete_tests(self):
        print("命令: 查询未完成试验")
        specimen_id = self.specimen_id_entry.get()
        print("查询编号:", specimen_id)
        for i in self.tree.get_children():
            self.tree.delete(i)
        # TODO: 查询实际未完成试验数据
        self.insert_sample_data()
        self.clear_details() # 清空右侧详情

    def on_tree_select(self, event):
        """当 Treeview 中的选择项改变时触发"""
        selected_items = self.tree.selection()
        if selected_items:
            item_id = selected_items[0] # 只处理单选
            item_data = self.tree.item(item_id, 'values')
            print("选中项:", item_id, item_data)
            # TODO: 根据选中的 item_id 或 item_data 查询详细信息
            # 更新右侧详情面板
            self.update_details(item_data) 
        else:
            self.clear_details()

    def update_details(self, data):
        """用查询到的数据更新右侧详情面板 (示例)"""
        # 注意：data 的索引需要匹配 Treeview 的列顺序
        # 这里用假数据填充
        self.detail_labels["试验类型:"].config(text="水泥混凝土抗压试验")
        self.detail_labels["样品编号:"].config(text=data[0]) # sample_id
        self.detail_labels["工程部位:"].config(text=data[2]) # project_part
        self.detail_labels["强度等级:"].config(text="C30") # 假数据
        self.detail_labels["试件尺寸(mm):"].config(text="150x150x150") # 假数据
        self.detail_labels["试件龄期(天):"].config(text="28") # 假数据
        self.detail_labels["试件数量:"].config(text=data[3]) # count
        self.detail_labels["执行标准:"].config(text="GB/T 50081") # 假数据
        
        # 更新小结果表 (假数据)
        for i in self.result_tree.get_children():
            self.result_tree.delete(i)
        self.result_tree.insert('', tk.END, values=("150.1", "33.4"))
        self.result_tree.insert('', tk.END, values=("152.3", "33.8"))

    def clear_details(self):
         """清空右侧详情面板和小结果表"""
         for label in self.detail_labels.values():
             label.config(text="---")
         for i in self.result_tree.get_children():
            self.result_tree.delete(i)

    def confirm_selection(self):
        """处理确定按钮点击事件"""
        selected_items = self.tree.selection()
        if selected_items:
            item_id = selected_items[0]
            item_data = self.tree.item(item_id, 'values')
            print("确定选择:", item_data)
            # TODO: 实现将选中的试验信息传递回主界面或其他逻辑
            # 例如，可以将信息存到父级 (MainScreen) 或调用父级的方法
            # if hasattr(self.parent, 'load_test_info'):
            #     self.parent.load_test_info(item_data) 
            self.destroy() # 关闭窗口
        else:
            print("未选择任何试验")
            # 可以显示提示
            from tkinter import messagebox
            messagebox.showwarning("提示", "请先选择一个未完成的试验！")

    def insert_sample_data(self):
        """向左侧 Treeview 插入示例数据"""
        sample_data = [
            ('YP-202504-JQD-ZBLJ1-030', '样品A', '张家庄大桥右幅1-6、2-7...', '6', '2025/4/19 10:47'),
            ('YP-202504-JQD-ZBLJ1-031', '样品B', '孟家沟大桥左幅11-6...', '3', '2025/4/20 09:30'),
        ]
        for item in sample_data:
            self.tree.insert('', tk.END, values=item)

# --- 用于独立测试 ContinuousSamplingWindow 的代码 --- 
if __name__ == '__main__':
    root = tk.Tk()
    root.title("主窗口 (测试用)")
    root.geometry("200x100")

    def open_cont_sampling():
        cont_win = ContinuousSamplingWindow(root)
    
    open_button = ttk.Button(root, text="打开续采试验窗口", command=open_cont_sampling)
    open_button.pack(pady=20)
    
    root.mainloop() 