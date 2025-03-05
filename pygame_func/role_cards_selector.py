import tkinter as tk
from tkinter import filedialog
import threading
import queue


class FolderSelector:
    def __init__(self):
        # 创建一个线程安全的队列来传递文件夹路径
        self.folder_path_queue = queue.Queue()

    def select_folder(self, init_path):
        # 创建Tkinter的主窗口并隐藏
        root = tk.Tk()
        root.withdraw()

        # 弹出选择文件夹对话框
        try:
            folder_path = filedialog.askdirectory(
                title="请选择一个文件夹", initialdir=init_path
            )

            # 将文件夹路径放入队列
            if folder_path:
                self.folder_path_queue.put(folder_path)
            else:
                self.folder_path_queue.put(None)
        except Exception as e:
            print(f"文件夹选择出错: {e}")
            self.folder_path_queue.put(None)
        finally:
            # 确保窗口关闭
            root.destroy()

    def get_folder_path(self, folder_path, timeout=10):
        """
        获取文件夹路径的方法，带有超时机制

        :param folder_path: 初始化文件查询路径
        :param timeout: 等待的最大秒数
        :return: 文件夹路径或None
        """
        # 启动文件夹选择线程
        thread = threading.Thread(target=self.select_folder, daemon=True, args=(folder_path,))
        thread.start()

        # 等待队列中的结果，带超时
        try:
            folder_path = self.folder_path_queue.get(timeout=timeout)
            if folder_path:
                index = folder_path.find("role_cards")
                extracted = folder_path[index:]
                return f'{extracted}/'
            else:
                return None
        except queue.Empty:
            print("文件夹选择超时")
            return None


if __name__ == "__main__":
    # 使用示例
    selector = FolderSelector()
    folder_path = selector.get_folder_path('../role_cards')
    if folder_path:
        print(f"选择的文件夹路径: {folder_path}")
    else:
        print("未选择文件夹或选择被取消")