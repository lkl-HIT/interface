# 项目名称：测试数据管理系统 GUI

## 1. 项目概述

本项目旨在使用 Python 3.4.4 和 Tkinter 库，**参照**提供的界面截图 (`GUI_group1` 文件夹) 作为**设计蓝本**，开发一个多界面的测试数据管理系统。目标是**使用 Tkinter 控件 (优先使用 ttk) 复刻截图中的布局、元素和视觉风格**，最终生成一个可以在 Windows XP 32位系统上运行的独立应用程序。

## 2. 技术要求

*   **编程语言**: Python 3.4.4 (严格遵守此版本以确保 Windows XP 兼容性)
*   **GUI 库**: Tkinter (优先使用 `tkinter.ttk` 以获得更好的视觉效果和主题支持，同时注意XP兼容性)
*   **目标平台**: Windows XP (32位)
*   **开发工具**: Cursor (利用 AI 辅助编程)
*   **绘图库**: Matplotlib (需选用 Python 3.4 兼容的版本，例如 `matplotlib==2.2.5`，用于实现截图中的图表)
*   **打包工具**: PyInstaller (需选用 Python 3.4 兼容的版本，例如 `3.2.1`)

## 3. 应用程序界面层级与结构

根据提供的截图，应用程序包含以下主要界面：

1.  **登录界面 (`登录界面.jpg`)**: 使用 Tkinter 控件构建。用户输入凭据进行登录。要求注释完整，便于后续增加识别登录名和密码等逻辑的代码。
2.  **主界面 (`主界面.jpg`)**: 使用 Tkinter 控件构建。**这是程序的核心操作界面，而非简单的导航页。** 布局包含：
    *   **顶部区域**: 左侧为三个数据显示框（荷载、强度、速率）及对应单位，右侧为"清零"按钮。
    *   **中心区域**: 左侧为带标题("实时数据显示")的 `matplotlib` 图表区（Y轴：kN，X轴：s），右侧为带标题("试验信息")的表单区域，用于显示/输入当前试验的详细参数。
    *   **底部按钮区域**: 包含 "开始试验", "续采试验", "数据查询", "丝杆上升", "丝杆下降" 按钮。
    *   **最底部状态栏**: 用于显示系统状态、联机状态、控制状态和错误提示。
    登录后默认显示此界面。要求完整按照截图进行控件布局，注释完整，接口详细，便于后续逻辑开发。
3.  **数据查询窗口 (`数据查询界面-万能机数据.jpg` 等)**: 
    *   通过主界面的 "数据查询" 按钮或菜单栏触发，**弹出一个独立的、可自由移动的 Toplevel 窗口**。
    *   此窗口内部使用 `ttk.Notebook` 实现标签页切换，包含三个标签页：
        *   **压力机数据**: 内容参照 `GUI_group1/压力机数据.jpg`。
        *   **万能机数据**: 内容参照 `GUI_group1/数据查询界面-万能机数据.jpg` (默认显示)。
        *   **见证取样试验**: 内容参照 `GUI_group1/见证取样试验界面.jpg`。
    *   每个标签页的内容由对应的 Python 文件 (`pressure_machine_screen.py` 等) 实现。
4.  **续采试验窗口 (`续采试验.jpg`)**: 
    *   通过主界面的 "续采试验" 按钮或菜单栏触发，**弹出一个独立的、可自由移动的 Toplevel 窗口**。
    *   用于列出未完成的试验（截图显示为压力机），包含筛选条件、试验列表、选中项的详细信息面板和小结果表。
    *   由 `continuous_sampling_window.py` 实现。

每个界面都应使用 Tkinter 控件 (如 Frame, Label, Entry, Button, Combobox, Treeview, matplotlib Canvas 等) 来实现其独立的布局和交互逻辑。

## 4. 使用 Cursor 进行开发的建议

### 4.1 模块化开发

*   **建议**: 将每个主要界面创建为独立的 Python 文件或类。
    *   `login_screen.py`
    *   `main_screen.py`
    *   `pressure_machine_screen.py`
    *   `universal_machine_screen.py`
    *   `sampling_test_screen.py`
    *   `continuous_sampling_window.py`
    *   `app.py` 作为主入口文件，负责管理和切换界面。
*   **Cursor 指令示例**: "请在 `login_screen.py` 文件中，参照 `登录界面.jpg` 截图，使用 ttk 控件 (Frame, Label, Entry, Button) 创建登录界面的布局。" 或 "请为 `pressure_machine_screen.py` 中的压力机界面添加 matplotlib 图表显示区域。"

### 4.2 布局管理

*   优先使用 `grid()` 布局管理器，因为它更适合构建类似截图中结构化的界面。`pack()` 可用于简单的行或列布局（如按钮栏），`place()` 慎用，主要用于需要精确定位或覆盖的少数情况。
*   使用 `ttk.Frame` 和 `ttk.LabelFrame` 来组织和分隔界面区域。
*   **Cursor 指令示例**: "请使用 `grid` 布局管理器，在 `pressure_machine_screen.py` 中创建顶部数据显示区、左侧图表区和右侧信息输入区。"

### 4.3 控件选用与样式

*   **优先使用 `ttk` 控件** (`ttk.Label`, `ttk.Entry`, `ttk.Button`, `ttk.Combobox`, `ttk.Treeview`, `ttk.Radiobutton`, `ttk.Checkbutton`)，因为它们支持主题，视觉效果更好，尤其是在旧版 Windows 上。
*   使用 `ttk.Style` 来定制控件的外观（背景色、前景色、字体），以尽可能接近截图的风格。注意 Windows XP 对样式的支持可能有限。
*   对于图表，使用 `matplotlib` 库，并将其 Canvas 嵌入到 Tkinter 窗口中 (`matplotlib.backends.backend_tkagg.FigureCanvasTkAgg`)。
*   **Cursor 指令示例**: "请在 `pressure_machine_screen.py` 中创建一个 ttk.Treeview 用于显示数据。" 或 "请使用 ttk.Style 将 `login_screen.py` 中登录按钮的字体设置为'微软雅黑 10'。" (字体需系统支持)

### 4.4 兼容性优先

*   **严格遵守 Python 3.4.4 语法**: 禁止使用 f-strings (用 `.format()`)，注意库的兼容版本。
*   **测试**: 由于目标是 Windows XP，开发过程中最好能在接近的环境（或虚拟机）中不时测试界面显示效果和功能。
*   **Cursor 指令示例**: "请确保这段代码在 Python 3.4.4 下可以运行。" 或 "请帮我查找 `matplotlib` 2.2.x 版本中绘制网格线的函数。"

### 4.5 逐步实现与测试

*   按界面层级顺序开发：登录 -> 主界面 -> 各功能子界面。
*   先布局，再实现交互逻辑。
*   **Cursor 指令示例**: "我们已经完成了 `pressure_machine_screen.py` 的基本布局，现在请为'开始试验'按钮添加一个占位符命令函数。"

### 4.6 交互逻辑与接口

*   为所有交互控件（按钮、菜单项等）定义清晰的命令函数（即使是占位符）。
*   在类或模块之间设计清晰的接口，例如，登录成功后如何通知主应用切换界面，主界面如何调用子界面的加载数据方法等。
*   **Cursor 指令示例**: "请在 `LoginScreen` 类中添加一个 `login_success_callback` 参数，并在登录成功时调用它。" 或 "请在 `PressureMachineScreen` 中添加一个 `load_data(test_id)` 方法的框架。"

## 5. 建议的文件结构

```
/project_root
|-- app.py                   # 主应用程序入口，窗口和菜单管理器
|-- login_screen.py          # 登录界面 (Tkinter控件实现)
|-- main_screen.py           # 核心操作主界面 (Tkinter + Matplotlib 实现)
|-- data_query_window.py     # 数据查询 Toplevel 窗口 (含 ttk.Notebook)
|-- pressure_machine_screen.py # 压力机数据 *标签页内容* (Tkinter控件实现)
|-- universal_machine_screen.py # 万能机数据 *标签页内容* (Tkinter控件实现)
|-- sampling_test_screen.py   # 见证取样试验 *标签页内容* (Tkinter控件实现)
|-- continuous_sampling_window.py # 续采试验 Toplevel 窗口
|-- components/              # (可选) 可复用的UI组件
|   |-- __init__.py
|   |-- custom_widgets.py
|-- utils/                   # (可选) 实用工具函数
|   |-- __init__.py
|   |-- helpers.py
|-- assets/                  # (可选) 存放图标等资源 (如果需要)
|-- requirements.txt         # 项目依赖 (matplotlib, pyinstaller)
|-- README.md                # 本文件
|-- project_structure.txt    # 项目结构说明
|-- GUI_group1/              # 存放界面设计参考截图
|   |-- 登录界面.jpg
|   |-- ... (其他截图)
```

## 6. 依赖项

*   Python 3.4.4
*   Tkinter (Python 内建)
*   matplotlib (用于绘图，安装兼容版本 `matplotlib==2.2.5`)
*   PyInstaller (用于打包，安装兼容版本 `pyinstaller==3.2.1`)

*(请在 `requirements.txt` 文件中手动记录这些依赖及其版本)*

## 7. 后续步骤建议

1.  **环境搭建**: (已完成)
2.  **修正登录界面**: (已完成)
3.  **实现主界面**: (已完成基础布局)
4.  **创建数据查询窗口**: (已完成)
5.  **修改各数据屏幕**: (已完成框架调整)
6.  **链接数据查询功能**: (已完成)
7.  **实现子界面内容**: 
    *   **实现万能机数据查询界面 (`universal_machine_screen.py`)**: (已完成)
    *   **实现压力机数据查询界面 (`pressure_machine_screen.py`)**: (已完成)
    *   **实现见证取样试验界面 (`sampling_test_screen.py`)**: (已完成)
    *   **实现续采试验窗口 (`continuous_sampling_window.py`)**: 根据截图填充控件和布局。(刚完成)

再次感谢您的指正！ 