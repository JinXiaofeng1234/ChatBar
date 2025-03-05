import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import queue
from typing import List, Dict


class TextInputter:
    def __init__(self, conversation_history: List[Dict], initialize_flag: bool, agent):
        self.text_queue = queue.Queue()
        self.root = None
        self.sin_ls = ['0', '+', '!+', '!!+', '-', '!-', '!!-', '~', '!~', '!!~']
        self.window_closed = False  # 添加标志来追踪窗口状态
        if not initialize_flag:
            self.default_txt = conversation_history[-1]["content"]
        else:
            self.default_txt = conversation_history[-4]['content']
        self.favorability = agent.favorability
        self.trust_value = agent.trust_value
        self.relationship_index = agent.relationship_index

    def main_window(self):
        self.root = tk.Tk()
        self.root.title("恋爱速通大师")
        self.root.geometry("775x350+500+140")

        self.root.resizable(0, 0)

        # 添加窗口关闭事件处理
        def on_closing():
            self.window_closed = True
            self.text_queue.put(None)  # 在队列中放入None表示窗口被关闭
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_closing)

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # 关系部分
        relationship_label = tk.Label(main_frame, text='关系:')
        relationship_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        relationship_select_box = ttk.Combobox(main_frame)
        relationship_select_box['value'] = ["陌生人", "熟人", "朋友", "暧昧", "恋人", "未婚夫妇", "夫妻"]
        relationship_select_box.current(self.relationship_index)
        relationship_select_box.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # 好感度部分
        favor_label = tk.Label(main_frame, text="好感度:")
        favor_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        favor_entry = tk.Entry(main_frame)
        favor_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # 信任度部分
        trust_label = tk.Label(main_frame, text="信任度:")
        trust_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        trust_entry = tk.Entry(main_frame)
        trust_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # 大模型回复修改部分
        llm_response_label = tk.Label(main_frame, text='大模型回复内容:')
        llm_response_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        text_area = tk.Text(main_frame, height=10)
        text_area.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # 插入默认文本
        if self.default_txt:
            text_area.insert('1.0', self.default_txt)
        if self.favorability:
            favor_entry.insert(0, self.favorability)
        if self.trust_value:
            trust_entry.insert(0, self.trust_value)

        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=4, padx=10, pady=10, sticky="ew")

        def clear_text():
            text_area.delete('1.0', tk.END)

        def confirm_change():
            content = text_area.get('1.0', tk.END).strip()
            favor = favor_entry.get()
            trust = trust_entry.get()
            relationship_index = relationship_select_box.current()
            # 检查内容是否为空以及信任度和好感度是否为有效整数
            try:
                trust_val = int(trust)
                favor_val = int(favor)
            except ValueError:
                messagebox.showwarning("警告", "请输入有效的信任度和好感度整数值")
                return

            if content and isinstance(trust_val, int) and isinstance(favor_val, int):
                if -100 <= eval(trust) <= 100 and -100 <= eval(favor) <= 100:
                    if any([self.default_txt != content, self.relationship_index != relationship_index,
                            self.favorability != eval(favor), self.trust_value != eval(trust)]):
                        if format_check(content):
                            self.text_queue.put([relationship_index, content, int(favor), int(trust)])
                            self.root.destroy()
                        else:
                            messagebox.showwarning("警告", "格式不正确")
                    else:
                        messagebox.showwarning("警告", "请做出至少一项修改")
                else:
                    messagebox.showwarning("警告", "信任度和好感度值均不可超过-100或100")
            else:
                messagebox.showwarning("警告", "输入内容非法")

        def format_check(content):
            content_split_ls = content.split(' ')
            if len(content_split_ls) == 2 and content_split_ls[0] in self.sin_ls:
                return True
            else:
                return False

        tk.Button(btn_frame, text="清空", width=10, command=clear_text).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="确认", width=10, command=confirm_change).pack(side=tk.RIGHT)

        self.root.mainloop()

    def get_changes(self):
        thread = threading.Thread(target=self.main_window, daemon=True)
        thread.start()

        try:
            text_content = self.text_queue.get(timeout=300)  # 添加超时时间，比如300秒
            if text_content is None:  # 检查是否是因为窗口关闭而返回
                return None
            return text_content
        except queue.Empty:
            if hasattr(self, 'root') and self.root:
                self.root.destroy()
            return None
        except Exception as e:
            print(f"发生错误: {e}")
            if hasattr(self, 'root') and self.root:
                self.root.destroy()
            return None


if __name__ == "__main__":
    conversation_history = [  # 最外层是列表 List
        {"content": "消息1"},  # 里面的元素都是字典 Dict
        {"content": "消息2"},
        {"content": "+ 123"}
    ]
    text_inputter = TextInputter(conversation_history=conversation_history, initialize_flag=True, agent=None)
    result = text_inputter.get_changes()
    if result:
        print(f"输入的文本是：{result}")
    else:
        print("没有输入文本或操作被取消")
