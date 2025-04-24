# 压力机数据标签页内容
import tkinter as tk
from tkinter import ttk
# import matplotlib # 稍后用于绘图
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PressureMachineScreen(ttk.Frame):
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
        """创建顶部的查询条件区域 (与万能机界面类似)"""
        filter_frame = ttk.Frame(self, padding="5 5 5 5")
        filter_frame.grid(row=0, column=0, sticky="ew")

        # 试验类型
        ttk.Label(filter_frame, text="试验类型:").pack(side=tk.LEFT, padx=(0, 2))
        test_type_combo = ttk.Combobox(filter_frame, values=["全部"], width=10) # 示例值
        test_type_combo.set("全部")
        test_type_combo.pack(side=tk.LEFT, padx=(0, 10))

        # 样品编号
        ttk.Label(filter_frame, text="样品编号:").pack(side=tk.LEFT, padx=(0, 2))
        self.test_id_entry = ttk.Entry(filter_frame, width=15)
        self.test_id_entry.pack(side=tk.LEFT, padx=(0, 10))

        # 日期范围 (使用 Entry 模拟)
        ttk.Label(filter_frame, text="从").pack(side=tk.LEFT, padx=(10, 2))
        self.date_from_entry = ttk.Entry(filter_frame, width=12)
        self.date_from_entry.insert(0, "2025年 3月19日") # 示例日期
        self.date_from_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Label(filter_frame, text="到").pack(side=tk.LEFT, padx=(5, 2))
        self.date_to_entry = ttk.Entry(filter_frame, width=12)
        self.date_to_entry.insert(0, "2025年 4月19日") # 示例日期
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
        tree_frame.columnconfigure(0, weight=1) # 让 Treeview 列可伸展

        # --- 定义列 (根据压力机截图调整) --- 
        # 注意：Treeview 本身不直接支持复选框列。我们将忽略它，通过行选择处理。
        columns = ('sample_id', 'project_part', 'specimen_size', 'strength_grade', 
                   'age', 'test_date', 'details')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        # --- 设置列标题 --- 
        self.tree.heading('sample_id', text='样品编号')
        self.tree.heading('project_part', text='工程部位')
        self.tree.heading('specimen_size', text='试件尺寸')
        self.tree.heading('strength_grade', text='强度等级')
        self.tree.heading('age', text='龄期')
        self.tree.heading('test_date', text='试验日期')
        self.tree.heading('details', text='详情')

        # --- 设置列宽和对齐 (根据截图大致调整) --- 
        self.tree.column('sample_id', width=180)
        self.tree.column('project_part', width=250)
        self.tree.column('specimen_size', width=100, anchor='center')
        self.tree.column('strength_grade', width=80, anchor='center')
        self.tree.column('age', width=50, anchor='center')
        self.tree.column('test_date', width=100, anchor='center')
        self.tree.column('details', width=60, anchor='center')

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
        """创建底部的操作按钮区域 (与万能机界面相同)"""
        action_frame = ttk.Frame(self, padding="5 5 5 5")
        action_frame.grid(row=2, column=0, sticky="ew")

        select_all_button = ttk.Button(action_frame, text="全选", command=self.select_all)
        select_all_button.pack(side=tk.LEFT, padx=(0, 10))

        upload_button = ttk.Button(action_frame, text="上传", command=self.upload_selected)
        upload_button.pack(side=tk.LEFT)

    # --- 占位符命令 --- 
    def query_data(self):
        print("命令: 查询压力机数据")
        test_type = "全部" 
        test_id = self.test_id_entry.get()
        date_from = self.date_from_entry.get()
        date_to = self.date_to_entry.get()
        upload_status = self.upload_status_var.get()
        print("查询条件:", test_type, test_id, date_from, date_to, upload_status)
        for i in self.tree.get_children():
            self.tree.delete(i)
        # TODO: 查询压力机数据源
        self.insert_sample_data() # 临时

    def select_all(self):
        print("命令: 全选压力机数据")
        # for item in self.tree.get_children():
        #     self.tree.selection_add(item)

    def upload_selected(self):
        print("命令: 上传选中的压力机数据")
        selected_items = self.tree.selection()
        print("选中的项目:", selected_items)
        # for item_id in selected_items:
        #     item_data = self.tree.item(item_id, 'values')
        #     print("上传数据:", item_data)

    def insert_sample_data(self):
        """向 Treeview 中插入压力机示例数据"""
        # 根据截图输入一些示例数据
        sample_data = [
            ('YP-202504-JQD-ZBLJ1-030', '孟家沟大桥左幅11-6/11-5右幅11-T梁乳孔', '40×40×160', 'M50', '3', '2025/4/19', '详情'),
            ('YP-202504-JQD-ZBLJ1-029', '郭家庄G匝道桥14-10/10-3/14-8T梁孔道压浆', '40×40', 'M50', '3', '2025/4/19', '详情'),
            ('YP-202504-JQD-ZBLJ1-028', '郭家庄G匝道桥14-10/10-3/14-8T梁孔道压浆', '40×40×160', 'M50', '3', '2025/4/19', '详情'),
            ('YP-202504-JQD-ZBLJ1-030', '张家庄大桥左幅1-6、2-7T梁孔道压浆', '40×40×160', 'M50', '3', '2025/4/18', '详情'),
            # ... 添加更多数据 ...
        ]
        for item in sample_data:
            self.tree.insert('', tk.END, values=item)

# --- 不再需要独立测试代码 --- 
# if __name__ == '__main__':
#     class MockController(tk.Tk):
#         ...
#     controller = MockController()
#     pressure_screen = PressureMachineScreen(controller, controller)
#     pressure_screen.pack(fill="both", expand=True)
#     root.mainloop() 