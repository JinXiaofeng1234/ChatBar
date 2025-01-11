import pygame
from select_box import OptionBox


class ScreenBoard:
    """
    一个简单的Pygame屏幕板，仅提供屏幕创建功能
    """

    def __init__(self, width, height, x=0, y=0):
        """
        初始化屏幕板

        Args:
            width (int): 屏幕宽度
            height (int): 屏幕高度
            x (int): board在主屏幕上的x坐标
            y (int): board在主屏幕上的y坐标
        """
        self.setting_ls = [0, 0, 0, 0, 0]
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.surface = pygame.Surface((width, height))
        self.surface.fill((200, 200, 200))

        # 初始化字体
        self.font = pygame.font.SysFont('SimHei', 30)
        # 绘制文本
        self.llm_label = self.font.render('大模型选择', True, (0, 0, 0))
        self.speech_gen_label = self.font.render('语音生成模型选择', True, (0, 0, 0))
        self.kb_label = self.font.render('知识库选择', True, (0, 0, 0))
        self.se_label = self.font.render('搜索引擎选择', True, (0, 0, 0))
        self.vm_label = self.font.render('视觉任务选择', True, (0, 0, 0))

        # 初始化下拉框 - 注意这里的坐标是相对于board的
        self.model_list = ["千问2.5-14b-128K", "文心一言4.0-128K", "通义千问Plus"]
        self.speech_model_list = ['睿声', 'Fish Audio']
        self.kb_list = ['问答数据库', "向量数据库"]
        self.search_engine_ls = ['kimi', '敬请期待']
        self.vision_mode_ls = ['根据提示词', 'OCR', '画面赏析', '场景识别', '人脸识别']
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

    def draw(self):
        self.surface.fill((200, 200, 200))  # 每次绘制前清空surface
        # 先绘制黑色边框
        pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, self.width, self.height), 2)  # 2是边框宽度

        self.surface.blit(self.llm_label, (121, 5))
        self.surface.blit(self.speech_gen_label, (82, 80))
        self.surface.blit(self.kb_label, (121, 155))
        self.surface.blit(self.se_label, (110, 228))
        self.surface.blit(self.vm_label, (110, 301))

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

        # 检查选项的碰撞
        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(adjusted_pos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
