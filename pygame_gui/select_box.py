import pygame


class OptionBox:
    def __init__(self, x, y, w, h, color, highlight_color, font, option_list, selected=0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

        # 新增属性：当前显示的选项起始索引 & 可见选项数量
        self.start_index = 0
        self.visible_count = 6

    def draw(self, surf):
        # 绘制当前选中项按钮
        pygame.draw.rect(surf, self.highlight_color if self.menu_active else self.color, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], True, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        # 如果下拉菜单开启则绘制部分选项
        if self.draw_menu:
            # 计算终止位置
            end_index = min(self.start_index + self.visible_count, len(self.option_list))
            for i, text in enumerate(self.option_list[self.start_index:end_index]):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                # 结合全局索引判断激活状态
                global_index = self.start_index + i
                pygame.draw.rect(
                    surf,
                    self.highlight_color if global_index == self.active_option else self.color,
                    rect)
                msg = self.font.render(text, True, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))
            # 绘制下拉选项外部边框
            outer_rect = (
                self.rect.x, self.rect.y + self.rect.height,
                self.rect.width, self.rect.height * (end_index - self.start_index))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        # 检查当前可见区域内的每个选项是否被鼠标选中
        self.active_option = -1
        end_index = min(self.start_index + self.visible_count, len(self.option_list))
        for i in range(self.start_index, end_index):
            rect = self.rect.copy()
            pos = i - self.start_index  # 计算下拉区域中的位置
            rect.y += (pos + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            # 当鼠标既不在主按钮上，又不在下拉选项区域时，隐藏下拉菜单
            self.draw_menu = False

        for event in event_list:
            # 鼠标点击事件
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标滚轮事件: 向上滚动（button 4）和向下滚动（button 5）
                if event.button == 4 and self.draw_menu:
                    if self.start_index > 0:
                        self.start_index -= 1
                elif event.button == 5 and self.draw_menu:
                    if self.start_index < len(self.option_list) - self.visible_count:
                        self.start_index += 1
                elif event.button == 1:
                    # 点击主按钮时，切换下拉菜单的显示状态
                    if self.menu_active:
                        self.draw_menu = not self.draw_menu
                    # 点击下拉菜单中的某个选项时，更新选项
                    elif self.draw_menu and self.active_option >= 0:
                        self.selected = self.active_option
                        self.draw_menu = False
                        return self.active_option
        return -1


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((640, 480))

    # 测试选项，超过3个
    option_list = ["option 1", "option 2", "option 3", "option 4", "option 5", "option 6", '1', '2', '3']
    list_box = OptionBox(
        40, 40, 160, 40, (150, 150, 150), (100, 200, 255),
        pygame.font.SysFont(None, 30), option_list)

    run = True
    while run:
        clock.tick(60)
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False

        selected_option = list_box.update(event_list)
        if selected_option >= 0:
            print("选中的索引:", selected_option)

        window.fill((255, 255, 255))
        list_box.draw(window)
        pygame.display.flip()

    pygame.quit()
    exit()