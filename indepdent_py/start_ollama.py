import subprocess


def start_ollama():
    # 定义命令
    command = 'Start-Process "C:\\Users\\Cara  al sol\\AppData\\Local\\Programs\\Ollama\\ollama app.exe"'

    try:
        # 使用PowerShell执行命令
        subprocess.Popen(["powershell", "-Command", command],)
        print("应用程序已启动")

    except Exception as e:
        print("发生错误:", str(e))

    print("Python 脚本执行完毕")
