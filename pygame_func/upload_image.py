import tkinter as tk
from tkinter import filedialog
import threading
import queue


class ImageUploader:
    def __init__(self):
        # 创建一个线程安全的队列来传递文件路径
        self.file_path_queue = queue.Queue()

    def upload_image(self):
        # 创建Tkinter的主窗口并隐藏
        root = tk.Tk()
        root.withdraw()

        # 定义允许的文件类型
        file_types = [
            ('图片文件', '*.png *.jpg *.jpeg *.gif *.bmp *.webp'),
            ('PNG文件', '*.png'),
            ('JPEG文件', '*.jpg *.jpeg'),
            ('GIF文件', '*.gif'),
            ('所有文件', '*.*')
        ]

        # 弹出选择文件对话框，并限定文件类型
        try:
            file_path = filedialog.askopenfilename(
                title="请选择一个图片文件",
                filetypes=file_types
            )

            # 将文件路径放入队列
            if file_path:
                self.file_path_queue.put(file_path)
            else:
                self.file_path_queue.put(None)
        except Exception as e:
            print(f"文件选择出错: {e}")
            self.file_path_queue.put(None)
        finally:
            # 确保窗口关闭
            root.destroy()

    def get_image_path(self, timeout=10):
        """
        获取图片路径的方法，带有超时机制

        :param timeout: 等待的最大秒数
        :return: 文件路径或None
        """
        # 启动文件选择线程
        thread = threading.Thread(target=self.upload_image, daemon=True)
        thread.start()

        # 等待队列中的结果，带超时
        try:
            file_path = self.file_path_queue.get(timeout=timeout)
            return file_path
        except queue.Empty:
            print("文件选择超时")
            return None


if __name__ == "__main__":
    # upload_image_threading()
    pass
