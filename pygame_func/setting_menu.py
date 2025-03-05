import pygame
from select_box import OptionBox


class ScreenBoard:
    """
    一个简单的Pygame屏幕板，仅提供屏幕创建功能
    """

    def __init__(self, width, height, text_dic, x=0, y=0):
        """
        初始化屏幕板

        Args:
            width (int): 屏幕宽度
            height (int): 屏幕高度
            x (int): board在主屏幕上的x坐标
            y (int): board在主屏幕上的y坐标
        """
        menu_options_ls = text_dic['menu_options_ls']
        self.setting_ls = [0] * len(menu_options_ls)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.surface = pygame.Surface((width, height))
        self.surface.fill((200, 200, 200))

        # 初始化字体
        self.font = pygame.font.SysFont('SimHei', 30)
        # 绘制文本
        self.llm_label = self.font.render(menu_options_ls[0], True, (0, 0, 0))
        self.speech_gen_label = self.font.render(menu_options_ls[1], True, (0, 0, 0))
        self.kb_label = self.font.render(menu_options_ls[2], True, (0, 0, 0))
        self.se_label = self.font.render(menu_options_ls[3], True, (0, 0, 0))
        self.vm_label = self.font.render(menu_options_ls[4], True, (0, 0, 0))
        self.animation_label = self.font.render(menu_options_ls[5], True, (0, 0, 0))

        # 初始化下拉框 - 注意这里的坐标是相对于board的
        self.model_list = text_dic["model_list"]
        self.speech_model_list = text_dic["speech_model_list"]
        self.kb_list = text_dic["kb_list"]
        self.search_engine_ls = text_dic["search_engine_ls"]
        self.vision_mode_ls = text_dic["vision_mode_ls"]
        self.animation_ls = text_dic["animation_ls"]
        # 创建下拉框时加入偏移量
        self.model_select_box = AdjustedOptionBox(
            75, 36, 250, 40, (150, 150, 150),
            (100, 200, 255), pygame.font.SysFont('SimHei', 30),
            self.model_list, self.x, self.y)
        self.speech_select_box = AdjustedOptionBox(
            75, 110, 250, 40, (150, 150, 150),
            (100, 200, 255), pygame.font.SysFont('SimHei', 30),
            self.speech_model_list, self.x, self.y)
        self.kb_select_box = AdjustedOptionBox(
            75, 184, 250, 40, (150, 150, 150),
            (100, 200, 255), pygame.font.SysFont('SimHei', 30),
            self.kb_list, self.x, self.y)
        self.search_engine_select_box = AdjustedOptionBox(
            75, 258, 250, 40, (150, 150, 150),
            (100, 200, 255), pygame.font.SysFont('SimHei', 30),
            self.search_engine_ls, self.x, self.y)
        self.vision_mode_select_box = AdjustedOptionBox(
            75, 332, 250, 40, (150, 150, 150),
            (100, 200, 255), pygame.font.SysFont('SimHei', 30),
            self.vision_mode_ls, self.x, self.y)
        self.animation_ls_select_box = AdjustedOptionBox(
            75, 406, 250, 40, (150, 150, 150),
            (100, 200, 255), pygame.font.SysFont('SimHei', 30),
            self.animation_ls, self.x, self.y)

    def draw(self):
        self.surface.fill((200, 200, 200))  # 每次绘制前清空surface
        # 先绘制黑色边框
        pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, self.width, self.height), 2)  # 2是边框宽度

        self.surface.blit(self.llm_label, (121, 5))
        self.surface.blit(self.speech_gen_label, (82, 80))
        self.surface.blit(self.kb_label, (121, 155))
        self.surface.blit(self.se_label, (110, 228))
        self.surface.blit(self.vm_label, (110, 301))
        self.surface.blit(self.animation_label, (82, 374))

        self.animation_ls_select_box.draw(self.surface)
        self.vision_mode_select_box.draw(self.surface)
        self.search_engine_select_box.draw(self.surface)
        self.kb_select_box.draw(self.surface)
        self.speech_select_box.draw(self.surface)
        self.model_select_box.draw(self.surface)

    def update(self, event_list):
        llm_select_index = self.model_select_box.update(event_list)
        sgm_select_index = self.speech_select_box.update(event_list)
        kb_select_index = self.kb_select_box.update(event_list)
        se_select_index = self.search_engine_select_box.update(event_list)
        vm_select_index = self.vision_mode_select_box.update(event_list)
        am_select_index = self.animation_ls_select_box.update(event_list)
        if llm_select_index >= 0:
            self.setting_ls[0] = llm_select_index
        if sgm_select_index >= 0:
            self.setting_ls[1] = sgm_select_index
        if kb_select_index >= 0:
            self.setting_ls[2] = kb_select_index
        if se_select_index >= 0:
            self.setting_ls[3] = se_select_index
        if vm_select_index >= 0:
            self.setting_ls[4] = vm_select_index
        if am_select_index >= 0:
            self.setting_ls[5] = am_select_index
        return self.setting_ls


class AdjustedOptionBox(OptionBox):
    def __init__(self, x, y, w, h, color, highlight_color, font, option_list, offset_x=0, offset_y=0, selected=0):
        super().__init__(x, y, w, h, color, highlight_color, font, option_list, selected)
        self.offset_x = offset_x
        self.offset_y = offset_y

    def update(self, event_list):
        # 获取全局鼠标位置并调整为相对位置
        mpos = pygame.mouse.get_pos()
        adjusted_pos = (mpos[0] - self.offset_x, mpos[1] - self.offset_y)

        # 检查主下拉框的碰撞
        self.menu_active = self.rect.collidepoint(adjusted_pos)

        # 检查当前可见区域内的选项碰撞
        self.active_option = -1
        if self.draw_menu:
            end_index = min(self.start_index + self.visible_count, len(self.option_list))
            for i in range(self.start_index, end_index):
                rect = self.rect.copy()
                pos = i - self.start_index  # 计算在可见区域中的相对位置
                rect.y += (pos + 1) * self.rect.height
                if rect.collidepoint(adjusted_pos):
                    self.active_option = i
                    break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 处理鼠标滚轮事件
                if event.button == 4 and self.draw_menu:  # 向上滚动
                    if self.start_index > 0:
                        self.start_index -= 1
                elif event.button == 5 and self.draw_menu:  # 向下滚动
                    if self.start_index < len(self.option_list) - self.visible_count:
                        self.start_index += 1
                elif event.button == 1:  # 鼠标左键点击
                    if self.menu_active:
                        self.draw_menu = not self.draw_menu
                    elif self.draw_menu and self.active_option >= 0:
                        self.selected = self.active_option
                        self.draw_menu = False
                        return self.active_option
        return -1


# 示例使用
if __name__ == "__main__":
    pygame.init()

    # 创建主屏幕
    main_screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Main Window")

    # 创建board，设置位置为(200, 150)
    board = ScreenBoard(400, 580, 0, 0)

    setting_ls = []

    # 简单的主循环
    running = True
    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False

        # 填充主屏幕背景为白色
        main_screen.fill((255, 255, 255))

        # 更新和绘制board
        current_setting_ls = board.update(event_list)
        if current_setting_ls is not None:
            if setting_ls != current_setting_ls:
                setting_ls = current_setting_ls.copy()
                print(setting_ls)
        board.draw()

        # 将board绘制到主屏幕上
        main_screen.blit(board.surface, (board.x, board.y))

        pygame.display.flip()

    pygame.quit()
