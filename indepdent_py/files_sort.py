from pathlib import Path


def list_files_sorted_by_time(directory):
    # 使用 Pathlib 获取目录中的所有文件
    files = [f for f in Path(directory).iterdir() if f.is_file()]

    if files:

        # 按照最后修改时间对文件进行排序
        files_sorted = sorted(files, key=lambda f: f.stat().st_mtime)

        return files_sorted
    else:
        return None


def clear_folder(directory):
    # 使用 Pathlib 获取目录中的所有文件
    files = [f for f in Path(directory).iterdir() if f.is_file()]

    files_num = len(files)

    if files_num > 1:
        # 按照最后修改时间对文件进行排序
        files_sorted = sorted(files, key=lambda f: f.stat().st_mtime)
        for file_name in files_sorted[:-1]:
            # 指定要删除的文件路径
            file_path = Path(file_name)
            file_path.unlink()

    elif files_num == 1:
        return None

    else:
        return None


if __name__ == "__main__":
    # 替换 'your_directory' 为你的实际目录路径
    directory_path = 'tmp_audio'
    clear_folder(directory_path)

