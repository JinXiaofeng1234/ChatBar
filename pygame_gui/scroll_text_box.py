import pygame
import os
from pygame.locals import *


class ScrollableTextBox:
    def __init__(self, x, y, w, h, color, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.font = font
        self.text = ''
        self.show_text = str()
        self.active = False
        self.text_offset = 0
        self.text_changed_flag = False
        self.cursor_flag = True
        self.pointer_clock_time = pygame.time.get_ticks()
        self.delete_timer = 0
        self.delete_interval = 100
        # 添加缓存的文本高度
        self._text_height = self.font.get_linesize()
        self.last_text_width = 0  # 添加这行来跟踪文本宽度变化
        self.user_input_flag = False
        self.reset_text_color = (128, 128, 128)

    def draw(self, surface):
        # 绘制文本框背景和边框
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (128, 128, 128) if not self.active else (0, 0, 0), self.rect, 2)

        # 计算可显示的文本宽度
        visible_width = self.rect.width - 10

        # 根据游标状态拼接文本
        self.show_text = f'{self.text}|' if self.cursor_flag and self.active else self.text

        # 渲染文本
        if self.show_text != '|':
            self.font.set_italic(False)
            full_text_surface = self.font.render(self.show_text, True, (0, 0, 0))
        else:
            self.font.set_italic(True)
            full_text_surface = self.font.render('请输入文本...', True, self.reset_text_color)

        total_width = full_text_surface.get_width()

        # 检查是否需要自动滚动
        if total_width > visible_width and total_width > self.last_text_width and self.user_input_flag:
            self.view_forward()
            self.user_input_flag = False
        self.last_text_width = total_width

        # 计算固定的垂直居中位置
        text_y = self.rect.y + (self.rect.height - self._text_height) // 2

        # 如果文本超出显示范围，进行裁剪后绘制
        if total_width > visible_width:
            clip_rect = pygame.Rect(self.rect.x + 5, self.rect.y, visible_width, self.rect.height)
            surface.set_clip(clip_rect)
            text_x = self.rect.x + 5 - self.text_offset
            surface.blit(full_text_surface, (text_x, text_y))
            surface.set_clip(None)
        else:
            surface.blit(full_text_surface, (self.rect.x + 5, text_y))

    def view_forward(self):
        # 计算实际需要的偏移量
        full_text_surface = self.font.render(self.show_text, True, (0, 0, 0))
        visible_width = self.rect.width - 10
        total_width = full_text_surface.get_width()

        if total_width > visible_width:
            # 确保文本末尾可见
            self.text_offset = max(0, total_width - visible_width)

    def handle_event(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 检查鼠标点击是否在文本框内
                if self.rect.collidepoint(event.pos):
                    self.active = True
                    pygame.key.set_text_input_rect((self.rect.x, self.rect.bottom, 0, 0))
                else:
                    self.active = False

                    # 处理鼠标滚轮调整文本水平偏移量
                if event.button == 4:  # 向上滚动
                    self.text_offset = max(0, self.text_offset - 20)
                elif event.button == 5:  # 向下滚动
                    full_text_surface = self.font.render(self.show_text, True, (0, 0, 0))
                    max_offset = max(0, full_text_surface.get_width() - (self.rect.width - 10))
                    self.text_offset = min(max_offset, self.text_offset + 20)

            # 修改这里的按键检测
            if event.type == pygame.KEYDOWN:  # 检测按键按下事件
                if event.key == pygame.K_LALT:  # 检测是否是左alt键
                    self.text = ''
                    self.text_changed_flag = True

            if self.active:
                if event.type == TEXTINPUT:
                    self.text += event.text
                    self.text_changed_flag = True
                    self.user_input_flag = True

        self.update()

    def update(self):
        time_now = pygame.time.get_ticks()
        self.text_changed_flag = False

        # 游标闪烁更新
        if time_now - self.pointer_clock_time >= 300:
            self.cursor_flag = not self.cursor_flag
            self.pointer_clock_time = time_now

        if self.active:
            # 通过 get_pressed 检查 Backspace 键是否被长按
            keys = pygame.key.get_pressed()
            if keys[pygame.K_BACKSPACE]:
                if time_now - self.delete_timer >= self.delete_interval:
                    if self.text:
                        self.text = self.text[:-1]
                        self.text_changed_flag = True
                        # 更新文本偏移量
                        text_width = self.font.render(self.text, True, (0, 0, 0)).get_width()
                        self.text_offset = min(self.text_offset, max(0, text_width - (self.rect.width - 10)))
                    self.delete_timer = time_now
            else:
                # 重置删除计时器以便下次立即生效
                self.delete_timer = time_now


if __name__ == "__main__":
    pygame.init()
    # 设置显示输入法候选框
    os.environ["SDL_IME_SHOW_UI"] = "1"
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((640, 480))

    # 初始化文本框
    text_box = ScrollableTextBox(
        40, 40, 400, 40,
        (255, 255, 255), pygame.font.SysFont("SimHei", 32)
    )

    # 启动文本输入
    pygame.key.start_text_input()

    run = True
    while run:
        event_ls = pygame.event.get()
        for event in event_ls:
            if event.type == pygame.QUIT:
                run = False
        text_box.handle_event(event_ls)

        window.fill((200, 200, 200))
        text_box.draw(window)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    exit()
