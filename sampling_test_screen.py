# 见证取样试验标签页内容
import tkinter as tk
from tkinter import ttk

class SamplingTestScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # --- 配置主框架 Grid --- 
        self.rowconfigure(1, weight=1) # 让 Treeview 区域可伸展
        self.columnconfigure(0, weight=1) # 让内容宽度可伸展
        
        # --- 创建界面区域 --- 
        self.create_filter_area()
        self.create_treeview_area()
        self.create_action_area()

    def create_filter_area(self):
        """创建顶部的查询条件区域"""
        filter_frame = ttk.Frame(self, padding="5 5 5 5")
        filter_frame.grid(row=0, column=0, sticky="ew")

        # 试件编号
        ttk.Label(filter_frame, text="试件编号:").pack(side=tk.LEFT, padx=(0, 2))
        self.specimen_id_entry = ttk.Entry(filter_frame, width=15)
        self.specimen_id_entry.pack(side=tk.LEFT, padx=(0, 10))

        # 待试验 (复选框)
        self.pending_test_var = tk.BooleanVar()
        pending_check = ttk.Checkbutton(filter_frame, text="待试验", 
                                        variable=self.pending_test_var)
        pending_check.pack(side=tk.LEFT, padx=(5, 10))

        # 日期范围 (使用 Entry 模拟)
        ttk.Label(filter_frame, text="从").pack(side=tk.LEFT, padx=(10, 2))
        self.date_from_entry = ttk.Entry(filter_frame, width=12)
        self.date_from_entry.insert(0, "2017年 1月 1日") # 截图示例日期
        self.date_from_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Label(filter_frame, text="到").pack(side=tk.LEFT, padx=(5, 2))
        self.date_to_entry = ttk.Entry(filter_frame, width=12)
        self.date_to_entry.insert(0, "2025年 4月19日") # 截图示例日期
        self.date_to_entry.pack(side=tk.LEFT, padx=(0, 10))

        # 上传状态 (Radiobutton)
        self.upload_status_var = tk.StringVar(value="未上传")
        rb_not_uploaded = ttk.Radiobutton(filter_frame, text="未上传", 
                                          variable=self.upload_status_var, value="未上传")
        rb_not_uploaded.pack(side=tk.LEFT, padx=(10, 5))
        rb_uploaded = ttk.Radiobutton(filter_frame, text="已上传", 
                                      variable=self.upload_status_var, value="已上传")
        rb_uploaded.pack(side=tk.LEFT, padx=(0, 10))

        # 查询按钮
        query_button = ttk.Button(filter_frame, text="查询", command=self.query_data)
        query_button.pack(side=tk.LEFT, padx=5)

    def create_treeview_area(self):
        """创建中间的数据显示 Treeview"""
        tree_frame = ttk.Frame(self)
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # --- 定义列 (根据见证取样截图调整) --- 
        columns = ('specimen_id', 'specimen_size', 'load', 'strength', 'test_date')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        # --- 设置列标题 --- 
        self.tree.heading('specimen_id', text='试件编号')
        self.tree.heading('specimen_size', text='试件尺寸')
        self.tree.heading('load', text='荷载')
        self.tree.heading('strength', text='强度')
        self.tree.heading('test_date', text='试验日期')

        # --- 设置列宽和对齐 (根据截图大致调整) --- 
        self.tree.column('specimen_id', width=180)
        self.tree.column('specimen_size', width=120, anchor='center')
        self.tree.column('load', width=100, anchor='center')
        self.tree.column('strength', width=100, anchor='center')
        self.tree.column('test_date', width=120, anchor='center')

        # 添加滚动条
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # 布局 Treeview 和滚动条
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # 添加示例数据
        self.insert_sample_data()

    def create_action_area(self):
        """创建底部的操作按钮区域 (与前两个标签页相同)"""
        action_frame = ttk.Frame(self, padding="5 5 5 5")
        action_frame.grid(row=2, column=0, sticky="ew")

        select_all_button = ttk.Button(action_frame, text="全选", command=self.select_all)
        select_all_button.pack(side=tk.LEFT, padx=(0, 10))

        upload_button = ttk.Button(action_frame, text="上传", command=self.upload_selected)
        upload_button.pack(side=tk.LEFT)

    # --- 占位符命令 --- 
    def query_data(self):
        print("命令: 查询见证取样数据")
        specimen_id = self.specimen_id_entry.get()
        pending_test = self.pending_test_var.get()
        date_from = self.date_from_entry.get()
        date_to = self.date_to_entry.get()
        upload_status = self.upload_status_var.get()
        print("查询条件:", specimen_id, pending_test, date_from, date_to, upload_status)
        for i in self.tree.get_children():
            self.tree.delete(i)
        # TODO: 查询见证取样数据源
        self.insert_sample_data() # 临时

    def select_all(self):
        print("命令: 全选见证取样数据")
        # for item in self.tree.get_children():
        #     self.tree.selection_add(item)

    def upload_selected(self):
        print("命令: 上传选中的见证取样数据")
        selected_items = self.tree.selection()
        print("选中的项目:", selected_items)
        # for item_id in selected_items:
        #     item_data = self.tree.item(item_id, 'values')
        #     print("上传数据:", item_data)

    def insert_sample_data(self):
        """向 Treeview 中插入见证取样示例数据"""
        # 需要根据实际数据格式调整
        sample_data = [
            ('JZQY-001', '150x150x150', '250.5', '33.4', '2025-04-15'),
            ('JZQY-002', '100x100x100', '180.2', '45.1', '2025-04-16'),
            ('JZQY-003', '150x150x150', '265.8', '35.4', '2025-04-17')
        ]
        for item in sample_data:
            self.tree.insert('', tk.END, values=item)

# --- 不再需要独立测试代码 --- 