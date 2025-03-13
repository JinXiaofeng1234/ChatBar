# import pygame
# import sys
# import numpy as np
#
# pygame.init()
#
# # 设置屏幕
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption('字符后备字体渲染')
# matrix = np.full((24, 3), [255, 0, 0], dtype=np.uint8)
# np.set_printoptions(threshold=np.inf)  # 设置为打印所有元素
#
#
# def is_japanese_char(char):
#     japanese_ranges = [
#         # 平假名
#         (0x3040, 0x309F),
#         # 片假名
#         (0x30A0, 0x30FF),
#         # 日文汉字
#         (0x4E00, 0x9FFF),
#         # 日文符号
#         (0x3000, 0x303F)
#     ]
#
#     return any(start <= ord(char) <= end for start, end in japanese_ranges)
#
#
# def render_text_with_fallback(text, primary_font):
#     text_surface = pygame.Surface((800, 100), pygame.SRCALPHA)
#     current_x = 0
#
#     for char in text:
#         # 选择合适的字体
#         if 0x3200 <= ord(char) <= 0x32FF:
#             font = fallback_font[4]
#         elif '\u4e00' <= char <= '\u9fff' or 0000 <= ord(char) <= 0x007F:
#             font = primary_font
#         elif char.isalpha() and char.isascii():
#             font = fallback_font[0]
#         elif is_japanese_char(char):
#             font = fallback_font[1]
#         elif '\u0410' <= char <= '\u044F':
#             font = fallback_font[2]
#         elif 0x0370 <= ord(char) <= 0x03FF:
#             font = fallback_font[3]
#         else:
#             font = fallback_font[5]  # emoji字体
#
#         # 渲染单个字符
#         render = font.render(char, True, (255, 128, 12))
#         text_surface.blit(render, (current_x, 0))
#         current_x += render.get_width()
#
#     return text_surface
#
#
# # print(pygame.font.get_fonts())
# # 加载字体
# # 注意：请替换为你系统中实际存在的字体路径
# primary_font = pygame.font.SysFont('simhei', 24)
# fallback_font = [
#     pygame.font.SysFont('Arial', 24),
#     pygame.font.SysFont('MS Gothic', 24),
#     pygame.font.SysFont('Calibri', 24),
#     pygame.font.SysFont('cambriamath', 24),
#     pygame.font.Font('font/NotoSerifCJKsc-Medium.otf', 24),
#     pygame.font.SysFont('segoeuiemoji', 24)
# ]
#
# # 测试文本（包含各种可能需要后备字体的字符）
# text_content = "你好 🌟 Привет 漢 Γειά σου 🎉+-㊤㊥㊦㊧㊨㊒㊫"
#
# # 渲染文本
# text_surface = render_text_with_fallback(text_content, primary_font)
#
# # 主循环
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     screen.fill((0, 0, 0))
#     screen.blit(text_surface, (100, 100))
#     pygame.display.flip()
#
# pygame.quit()
# sys.exit()

# import pygame
# import sys
#
#
# class GameState:
#     GAME1 = 1
#     GAME2 = 2
#
#
# class GameManager:
#     def __init__(self):
#         pygame.init()
#         self.screen = pygame.display.set_mode((800, 600))
#         self.clock = pygame.time.Clock()
#         self.current_state = GameState.GAME1
#
#     def run(self):
#         while True:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()
#
#                     # 处理状态切换
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_1:
#                         self.current_state = GameState.GAME1
#                     elif event.key == pygame.K_2:
#                         self.current_state = GameState.GAME2
#
#                         # 根据当前状态渲染不同游戏
#             if self.current_state == GameState.GAME1:
#                 self.run_game1()
#             elif self.current_state == GameState.GAME2:
#                 self.run_game2()
#
#             pygame.display.flip()
#             self.clock.tick(60)
#
#     def run_game1(self):
#         # 游戏1的渲染逻辑
#         self.screen.fill((255, 0, 0))  # 红色背景示例
#         font = pygame.font.Font(None, 36)
#         text = font.render("Game 1 - Press 2 to switch", True, (255, 255, 255))
#         self.screen.blit(text, (200, 300))
#
#     def run_game2(self):
#         # 游戏2的渲染逻辑
#         self.screen.fill((0, 255, 0))  # 绿色背景示例
#         font = pygame.font.Font(None, 36)
#         text = font.render("Game 2 - Press 1 to switch", True, (255, 255, 255))
#         self.screen.blit(text, (200, 300))
#
#
# if __name__ == "__main__":
#     game_manager = GameManager()
#     game_manager.run()

# import pygame
# import sys
# import yaml
#
#
# class Game1:
#     def __init__(self):
#         self.screen = pygame.display.set_mode((800, 600))
#         self.switch_to_game2 = False
#
#     def handle_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
#                 self.switch_to_game2 = True
#
#     def update(self):
#         self.screen.fill((255, 0, 0))
#         font = pygame.font.Font(None, 36)
#         text = font.render("Game 1 - Press 2 to switch", True, (255, 255, 255))
#         self.screen.blit(text, (200, 300))
#
#
# class Game2:
#     def __init__(self):
#         self.screen = pygame.display.set_mode((800, 600))
#         self.switch_to_game1 = False
#
#     def handle_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
#                 self.switch_to_game1 = True
#
#     def update(self):
#         self.screen.fill((0, 255, 0))
#         font = pygame.font.Font(None, 36)
#         text = font.render("Game 2 - Press 1 to switch", True, (255, 255, 255))
#         self.screen.blit(text, (200, 300))
#
#
# def main():
#     pygame.init()
#     pygame.display.set_caption("Game Switcher")
#     clock = pygame.time.Clock()
#
#     current_game = Game1()
#
#     while True:
#         current_game.handle_events()
#         current_game.update()
#         pygame.display.flip()
#         clock.tick(60)
#
#         # 检查是否需要切换游戏
#         if isinstance(current_game, Game1) and current_game.switch_to_game2:
#             current_game = Game2()
#         elif isinstance(current_game, Game2) and current_game.switch_to_game1:
#             current_game = Game1()
#
#
# if __name__ == "__main__":
#     main()

# import pygame
#
#
# class ImageTransitionBox:
#     def __init__(self, x, y, w, h, image1_path, image2_path):
#         """
#         初始化图像过渡效果管理器
#         :param x: x坐标
#         :param y: y坐标
#         :param w: 宽度
#         :param h: 高度
#         :param image1_path: 第一张图片路径
#         :param image2_path: 第二张图片路径
#         """
#         # 位置和大小
#         self.rect = pygame.Rect(x, y, w, h)
#
#         # 过渡相关属性
#         self.transition_duration = 1000
#         self.is_transitioning = False
#         self.transition_start_time = 0
#         self.show_first = True
#
#         # 加载图片
#         try:
#             self.img_first = pygame.image.load(image1_path).convert_alpha()
#             self.img_second = pygame.image.load(image2_path).convert_alpha()
#             # 缩放图片以适应指定大小
#             self.img_first = pygame.transform.scale(self.img_first, (w, h))
#             self.img_second = pygame.transform.scale(self.img_second, (w, h))
#             self.current_first = self.img_first.copy()
#             self.current_second = self.img_second.copy()
#         except Exception as e:
#             print(f"Error loading images: {e}")
#             raise
#
#     @staticmethod
#     def ease_in_out_cubic(x):
#         """缓动函数"""
#         if x < 0.5:
#             return 4 * x * x * x
#         else:
#             return 1 - pow(-2 * x + 2, 3) / 2
#
#     def draw(self, surf):
#         """
#         绘制图像
#         :param surf: pygame的显示表面
#         """
#         current_time = pygame.time.get_ticks()
#
#         if self.is_transitioning:
#             progress = (current_time - self.transition_start_time) / self.transition_duration
#             if progress >= 1:
#                 progress = 1
#                 self.is_transitioning = False
#
#             eased_progress = self.ease_in_out_cubic(progress)
#
#             if self.show_first:
#                 # 过渡到第一张图片
#                 surf.blit(self.img_first, self.rect)
#                 self.current_second.set_alpha(int(255 * (1 - eased_progress)))
#                 surf.blit(self.current_second, self.rect)
#             else:
#                 # 过渡到第二张图片
#                 surf.blit(self.img_second, self.rect)
#                 self.current_first.set_alpha(int(255 * (1 - eased_progress)))
#                 surf.blit(self.current_first, self.rect)
#         else:
#             # 不在过渡状态时只显示当前图片
#             if self.show_first:
#                 surf.blit(self.img_first, self.rect)
#             else:
#                 surf.blit(self.img_second, self.rect)
#
#     def update(self, event_list):
#         """
#         更新状态
#         :param event_list: pygame事件列表
#         :return: 是否发生了状态改变
#         """
#         mpos = pygame.mouse.get_pos()
#
#         for event in event_list:
#             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 if self.rect.collidepoint(mpos) and not self.is_transitioning:
#                     self.start_transition()
#                     return True
#         return False
#
#     def start_transition(self):
#         """开始过渡动画"""
#         self.is_transitioning = True
#         self.transition_start_time = pygame.time.get_ticks()
#         self.show_first = not self.show_first
#         self.current_first = self.img_first.copy()
#         self.current_second = self.img_second.copy()
#
#     # 使用示例
#
#
# if __name__ == "__main__":
#     pygame.init()
#     clock = pygame.time.Clock()
#     window = pygame.display.set_mode((800, 1000))
#
#     # 创建图片过渡框
#     try:
#         transition_box = ImageTransitionBox(
#             100, 100, 748, 1641,
#             r"role_cards\朝武芳乃\portrait\!!-\芳乃a_0_1863_1934.png",
#             r"role_cards\朝武芳乃\portrait\!!~\芳乃a_0_1862_1944.png"
#         )
#     except Exception as e:
#         print(f"Failed to create transition box: {e}")
#         pygame.quit()
#         exit()
#
#     running = True
#     while running:
#         clock.tick(60)
#         event_list = pygame.event.get()
#
#         for event in event_list:
#             if event.type == pygame.QUIT:
#                 running = False
#
#                 # 更新过渡框状态
#         transition_box.update(event_list)
#
#         # 绘制
#         window.fill((128, 128, 128))
#         transition_box.draw(window)
#         pygame.display.flip()
#
#     pygame.quit()
#     exit()

# import threading
# import queue
# import tkinter as tk
# import pygame
#
#
# # 共享对象管理器 (可以是字典、列表或类等)
# class SharedObject:
#     def __init__(self):
#         self.value = 0  # 一个简单的整数作为共享对象
#         self.lock = threading.Lock()  # 线程锁，确保线程安全
#
#     def update_value(self, delta):
#         with self.lock:
#             self.value += delta  # 更新值
#
#     def get_value(self):
#         with self.lock:
#             return self.value  # 读取值
#
#
# # Pygame 窗口线程
# def run_pygame(shared_object, command_queue):
#     pygame.init()
#     screen = pygame.display.set_mode((400, 300))
#     pygame.display.set_caption("Pygame Window")
#
#     font = pygame.font.Font(None, 36)
#     running = True
#
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.KEYDOWN:
#                 # Pygame 中按键改变共享对象
#                 if event.key == pygame.K_UP:
#                     shared_object.update_value(1)  # 按上箭头增加值
#                 elif event.key == pygame.K_DOWN:
#                     shared_object.update_value(-1)  # 按下箭头减少值
#
#         # 绘制共享对象的值
#         screen.fill((0, 0, 0))
#         value_text = font.render(f"Value: {shared_object.get_value()}", True, (255, 255, 255))
#         screen.blit(value_text, (100, 130))
#         pygame.display.flip()
#
#         # 检查是否要退出
#         try:
#             command = command_queue.get_nowait()
#             if command == "QUIT":
#                 running = False
#         except queue.Empty:
#             pass
#
#     pygame.quit()
#
#
# # Tkinter 窗口线程
# def run_tkinter(shared_object, command_queue):
#     def increase_value():
#         shared_object.update_value(1)  # 增加值
#
#     def decrease_value():
#         shared_object.update_value(-1)  # 减少值
#
#     def close_app():
#         command_queue.put("QUIT")  # 通知 pygame 退出
#         root.destroy()  # 关闭 Tkinter 窗口
#
#     root = tk.Tk()
#     root.title("Tkinter Window")
#     root.geometry("300x200")
#
#     label = tk.Label(root, text="Control the Shared Value")
#     label.pack(pady=10)
#
#     inc_button = tk.Button(root, text="Increase", command=increase_value)
#     inc_button.pack(pady=5)
#
#     dec_button = tk.Button(root, text="Decrease", command=decrease_value)
#     dec_button.pack(pady=5)
#
#     quit_button = tk.Button(root, text="Quit", command=close_app)
#     quit_button.pack(pady=5)
#
#     # 实时显示共享对象值
#     def update_label():
#         current_value = shared_object.get_value()
#         value_label.config(text=f"Value: {current_value}")
#         root.after(100, update_label)  # 每 100ms 更新一次
#
#     value_label = tk.Label(root, text="Value: 0", font=("Arial", 14))
#     value_label.pack(pady=10)
#
#     update_label()  # 启动实时更新
#     root.mainloop()
#
#
# # 主线程：创建共享对象并启动两个子线程
# if __name__ == "__main__":
#     shared_object = SharedObject()  # 创建共享对象
#     command_queue = queue.Queue()  # 用于线程间的命令通信
#
#     pygame_thread = threading.Thread(target=run_pygame, args=(shared_object, command_queue))
#     tkinter_thread = threading.Thread(target=run_tkinter, args=(shared_object, command_queue))
#
#     pygame_thread.start()
#     tkinter_thread.start()
#
#     pygame_thread.join()
#      tkinter_thread.join()

