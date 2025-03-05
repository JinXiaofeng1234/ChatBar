import os
import glob


def remove_old_files(folder_path):
    # 获取文件夹下的所有文件路径
    files = glob.glob(os.path.join(folder_path, '*'))

    # 按照修改时间排序文件列表，最新的文件在最后
    files.sort(key=os.path.getmtime)

    # 保留最新的一个文件，删除其他文件
    for file in files[:-1]:
        try:
            os.remove(file)
            print(f"Removed: {file}")
        except Exception as e:
            print(f"Error removing {file}: {e}")

        # 使用示例


if __name__ == "__main__":
    folder_path = '/path/to/your/folder'
    remove_old_files(folder_path)
