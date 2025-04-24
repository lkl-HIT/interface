# 万能机数据标签页内容
import tkinter as tk
from tkinter import ttk
# 可能需要导入 tkinter.font 用于更精确的字体控制

class UniversalMachineScreen(ttk.Frame):
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

        # 试验类型
        ttk.Label(filter_frame, text="试验类型:").pack(side=tk.LEFT, padx=(0, 2))
        test_type_combo = ttk.Combobox(filter_frame, values=["全部"], width=10) # 示例值
        test_type_combo.set("全部")
        test_type_combo.pack(side=tk.LEFT, padx=(0, 10))

        # 试验编号
        ttk.Label(filter_frame, text="试验编号:").pack(side=tk.LEFT, padx=(0, 2))
        self.test_id_entry = ttk.Entry(filter_frame, width=15)
        self.test_id_entry.pack(side=tk.LEFT, padx=(0, 10))

        # 日期范围 (使用 Entry 模拟)
        ttk.Label(filter_frame, text="从").pack(side=tk.LEFT, padx=(10, 2))
        self.date_from_entry = ttk.Entry(filter_frame, width=12)
        self.date_from_entry.insert(0, "2025年 3月19日") # 示例日期
        self.date_from_entry.pack(side=tk.LEFT, padx=(0, 5))
        # TODO: 添加日历图标按钮 (需要 tkcalendar 或自定义)
        
        ttk.Label(filter_frame, text="到").pack(side=tk.LEFT, padx=(5, 2))
        self.date_to_entry = ttk.Entry(filter_frame, width=12)
        self.date_to_entry.insert(0, "2025年 4月19日") # 示例日期
        self.date_to_entry.pack(side=tk.LEFT, padx=(0, 10))
        # TODO: 添加日历图标按钮

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

        # 定义列
        columns = ('sample_id', 'project_part', 'grade', 'nominal_dia', 
                   'operator', 'test_date', 'details')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        # 设置列标题
        self.tree.heading('sample_id', text='样品编号')
        self.tree.heading('project_part', text='工程部位')
        self.tree.heading('grade', text='牌号')
        self.tree.heading('nominal_dia', text='公称直径')
        self.tree.heading('operator', text='操作人员')
        self.tree.heading('test_date', text='试验日期')
        self.tree.heading('details', text='详情')

        # 设置列宽 (根据截图大致调整)
        self.tree.column('sample_id', width=120)
        self.tree.column('project_part', width=150)
        self.tree.column('grade', width=80)
        self.tree.column('nominal_dia', width=80, anchor='center')
        self.tree.column('operator', width=80, anchor='center')
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

        # 添加示例数据 (可选)
        self.insert_sample_data()

    def create_action_area(self):
        """创建底部的操作按钮区域"""
        action_frame = ttk.Frame(self, padding="5 5 5 5")
        action_frame.grid(row=2, column=0, sticky="ew")

        select_all_button = ttk.Button(action_frame, text="全选", command=self.select_all)
        select_all_button.pack(side=tk.LEFT, padx=(0, 10))

        upload_button = ttk.Button(action_frame, text="上传", command=self.upload_selected)
        upload_button.pack(side=tk.LEFT)

    # --- 占位符命令 --- 
    def query_data(self):
        print("命令: 查询数据")
        # TODO: 实现基于筛选条件查询数据的逻辑
        # 1. 获取所有筛选条件的值
        test_type = "全部" # 从 Combobox 获取
        test_id = self.test_id_entry.get()
        date_from = self.date_from_entry.get()
        date_to = self.date_to_entry.get()
        upload_status = self.upload_status_var.get()
        print("查询条件:", test_type, test_id, date_from, date_to, upload_status)
        # 2. 清空 Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        # 3. 查询数据库或数据源
        # 4. 将查询结果插入 Treeview (调用 self.tree.insert)
        self.insert_sample_data() # 临时重新插入示例数据

    def select_all(self):
        print("命令: 全选")
        # TODO: 实现选中 Treeview 中所有行的逻辑
        # for item in self.tree.get_children():
        #     self.tree.selection_add(item)

    def upload_selected(self):
        print("命令: 上传选中项")
        selected_items = self.tree.selection()
        print("选中的项目:", selected_items)
        # TODO: 实现上传选中数据的逻辑
        # for item_id in selected_items:
        #     item_data = self.tree.item(item_id, 'values')
        #     print("上传数据:", item_data)

    def insert_sample_data(self):
        """向 Treeview 中插入示例数据"""
        sample_data = [
            ('SN001', '桥梁A段', 'HRB400', '16', '张三', '2025-04-10', '查看'),
            ('SN002', '隧道B段', 'HRB500', '20', '李四', '2025-04-11', '查看'),
            ('SN003', '路基C段', 'HPB300', '8', '王五', '2025-04-12', '查看')
        ]
        for item in sample_data:
            # '' 表示插入顶级项目， tk.END 表示插入到末尾
            # iid 可以不指定，Treeview 会自动生成
            self.tree.insert('', tk.END, values=item)

# --- 不再需要独立测试代码 --- 