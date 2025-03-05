import pygame
import math
import time
import sys


class CLOCK:
    def __init__(self, x, y, clock_img_path):  # 添加x, y参数来设置位置
        # 设置窗口大小和标题
        self.WIDTH, self.HEIGHT = 200, 200
        self.x = x  # 存储x坐标
        self.y = y  # 存储y坐标
        self.CENTER = (self.x + self.WIDTH // 2, self.y + self.HEIGHT // 2)  # 中心点根据位置计算
        self.RADIUS = 90

        # 定义颜色
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLACK = (0, 0, 0)
        self.HOUR_COLOR = (0, 0, 0)
        self.MINUTE_COLOR = (50, 50, 50)
        self.SECOND_COLOR = (255, 0, 0)

        # 添加表盘图片路径
        clock_dial_path = clock_img_path

        # 加载表盘图片
        try:
            self.clock_dial = pygame.image.load(clock_dial_path).convert_alpha()
            print("表盘图片加载成功")
        except pygame.error as e:
            print(f"无法加载表盘图片: {e}")
            pygame.quit()
            sys.exit()

            # 缩放表盘图片以适应窗口大小
        self.clock_dial = pygame.transform.scale(self.clock_dial, (self.WIDTH, self.HEIGHT))
        self.clock_dial_rect = self.clock_dial.get_rect()
        self.clock_dial_rect.x = self.x  # 设置表盘位置x
        self.clock_dial_rect.y = self.y  # 设置表盘位置y

    def draw(self, surface):  # 修改为接收surface参数
        # 绘制表盘
        surface.blit(self.clock_dial, self.clock_dial_rect)

        # 获取当前时间
        current_time = time.localtime()
        hours = current_time.tm_hour % 12
        minutes = current_time.tm_min
        seconds = current_time.tm_sec

        # 计算角度
        hour_angle = (hours + minutes / 60) * 30  # 每小时30度
        minute_angle = (minutes + seconds / 60) * 6  # 每分钟6度
        second_angle = seconds * 6  # 每秒6度

        # 绘制时针
        hour_length = self.RADIUS * 0.5
        hour_end_x = self.CENTER[0] + hour_length * math.sin(math.radians(hour_angle))
        hour_end_y = self.CENTER[1] - hour_length * math.cos(math.radians(hour_angle))
        pygame.draw.aaline(surface, self.HOUR_COLOR, self.CENTER, (hour_end_x, hour_end_y), 4)

        # 绘制分针
        minute_length = self.RADIUS * 0.75
        minute_end_x = self.CENTER[0] + minute_length * math.sin(math.radians(minute_angle))
        minute_end_y = self.CENTER[1] - minute_length * math.cos(math.radians(minute_angle))
        pygame.draw.aaline(surface, self.MINUTE_COLOR, self.CENTER, (minute_end_x, minute_end_y), 2)

        # 绘制秒针
        second_length = self.RADIUS - 20
        second_end_x = self.CENTER[0] + second_length * math.sin(math.radians(second_angle))
        second_end_y = self.CENTER[1] - second_length * math.cos(math.radians(second_angle))
        pygame.draw.aaline(surface, self.SECOND_COLOR, self.CENTER, (second_end_x, second_end_y), 1)

        # 绘制中心圆点
        pygame.draw.circle(surface, self.BLACK, self.CENTER, 5)

    def update(self, event_list):
        # 如果需要处理事件可以在这里添加
        pass

    # 测试代码


if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Clock Widget Demo")

    # 创建时钟控件，位置在(220, 140)
    clock = CLOCK(220, 140, '../imgs/icon/clock.png')

    running = True
    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False

                # 更新时钟
        clock.update(event_list)

        # 绘制
        window.fill((240, 240, 240))  # 灰白色背景
        clock.draw(window)
        pygame.display.flip()

        # 控制帧率
        pygame.time.Clock().tick(60)

    pygame.quit()