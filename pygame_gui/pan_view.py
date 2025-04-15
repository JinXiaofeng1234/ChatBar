import pygame
import sys


class PanView:
    def __init__(self, x, y, width, height, image_path):
        """
        大图拖动查看控件

        参数:
            x, y: 控件在窗口中的位置
            width, height: 控件的宽高（可视区域大小）
            image_path: 图片路径
        """
        self.rect = pygame.Rect(x, y, width, height)

        # 加载图片
        try:
            self.original_image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            print(f"无法加载图片: {image_path}")
            sys.exit(1)

            # 获取图片尺寸
        self.image_width, self.image_height = self.original_image.get_size()

        # 视图位置（图片在可视区域中的偏移量）
        self.view_x, self.view_y = 0, 0

        self.last_click_pos = None  # Will store (screen_x, screen_y, image_x, image_y)

        # 拖动相关变量
        self.dragging = False
        self.drag_start_x, self.drag_start_y = 0, 0
        self.start_view_x, self.start_view_y = 0, 0

        # 限制拖动范围
        self.max_view_x = max(0, self.image_width - self.rect.width)
        self.max_view_y = max(0, self.image_height - self.rect.height)

        # 创建边框
        self.border_color = (100, 100, 100)
        self.active = False  # 鼠标是否在控件上

    def update(self, event_list):
        """
        更新控件状态

        参数:
            event_list: pygame事件列表
        """
        mpos = pygame.mouse.get_pos()
        self.active = self.rect.collidepoint(mpos)

        for event in event_list:
            # 鼠标按下开始拖动
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.active:  # 左键在控件区域内
                    # Store click position
                    screen_x, screen_y = mpos

                    # Calculate image coordinates (adding view offset)
                    image_x = screen_x - self.rect.x + self.view_x
                    image_y = screen_y - self.rect.y + self.view_y

                    # Store both screen and image coordinates
                    self.last_click_pos = (screen_x, screen_y, image_x, image_y)
                    print(f"Click at: Screen({screen_x}, {screen_y}), Image({image_x}, {image_y})")
                    self.dragging = True
                    self.drag_start_x, self.drag_start_y = mpos
                    self.start_view_x, self.start_view_y = self.view_x, self.view_y

                # 鼠标滚轮缩放（可选功能）
                elif event.button == 4 and self.active:  # 滚轮向上
                    self.view_y = max(0, self.view_y - 20)
                elif event.button == 5 and self.active:  # 滚轮向下
                    self.view_y = min(self.max_view_y, self.view_y + 20)

            # 鼠标移动时更新视图位置
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    # 计算鼠标移动距离
                    dx = mpos[0] - self.drag_start_x
                    dy = mpos[1] - self.drag_start_y

                    # 更新视图位置（方向相反）
                    self.view_x = self.start_view_x - dx
                    self.view_y = self.start_view_y - dy

                    # 边界检查
                    self.view_x = max(0, min(self.view_x, self.max_view_x))
                    self.view_y = max(0, min(self.view_y, self.max_view_y))

            # 鼠标释放结束拖动
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False

    def draw(self, surface):
        """
        绘制控件

        参数:
            surface: 要绘制到的表面
        """
        # 创建一个临时surface用于绘制可视区域
        view_surface = pygame.Surface((self.rect.width, self.rect.height))

        # 计算要绘制的图片区域
        visible_area = pygame.Rect(self.view_x, self.view_y, self.rect.width, self.rect.height)

        # 将可见区域绘制到临时surface上
        view_surface.blit(self.original_image, (0, 0), visible_area)

        # 将临时surface绘制到主surface上
        surface.blit(view_surface, self.rect.topleft)


if __name__ == "__main__":
    pygame.init()
    window_width, window_height = 1024, 860
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("图片浏览器")

    # 创建PanView实例，使用整个窗口
    pan_view = PanView(0, 0, window_width, window_height, "../role_cards/樱井惠/bg/beach/evening_light_on.png")

    running = True
    clock = pygame.time.Clock()

    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False

                # 更新控件
        pan_view.update(event_list)

        # 绘制
        window.fill((0, 0, 0))
        pan_view.draw(window)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()