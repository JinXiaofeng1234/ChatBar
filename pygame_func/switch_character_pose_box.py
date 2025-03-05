import pygame
import os
import random


class ImageTransitionBox:
    def __init__(self, x, y, image1_path, image2_path, once_flag,
                 image_path_ls=None, auto_motion_flag=False, motion_done_flag=False, image_change_time=5000):
        """
        初始化图像过渡效果管理器
        :param x: x坐标
        :param y: y坐标
        :param image1_path: 第一张图片路径
        :param image2_path: 第二张图片路径
        """
        self.image_path_ls = None
        self.auto_motion_flag = None
        self.current_index = None
        self.image_refresh_time = None
        self.motion_done_flag = None
        """
        初始化图像过渡效果管理器
        :param x: x坐标
        :param y: y坐标
        :param image1_path: 第一张图片路径
        :param image2_path: 第二张图片路径
        :param once_flag: 是否只执行一次过渡
        :param image_path_ls: 图片路径列表
        :param auto_motion_flag: 是否自动切换图片
        :param motion_done_flag: 是否完成自动切换
        """
        # 图片路径和图像对象
        self.image1_path = None
        self.image2_path = None
        self.img_first = None
        self.img_second = None

        # 过渡效果相关属性
        self.transition_duration = None
        self.transition_start_time = None
        self.image_change_time = image_change_time
        self.is_transitioning = None
        self.show_first = None
        self.current_first = None
        self.current_second = None

        # 位置和尺寸
        self.x = x
        self.y = y
        self.rect = None

        # 模式标志
        self.single_image_mode = None
        self.once_flag = None

        self.refresh_settings(x, y, image1_path, image2_path, once_flag,
                              image_path_ls, auto_motion_flag, motion_done_flag)

    def init_setting(self, x, y, image1_path, image2_path, once_flag):
        # 立绘变化模式设置
        self.once_flag = once_flag
        # 接收立绘路径
        self.image1_path = image1_path
        self.image2_path = image2_path

        # 检查图片文件是否存在
        if not self.image2_path:
            self.single_image_mode = True
        else:
            self.single_image_mode = False

        if not os.path.exists(self.image1_path):
            raise Exception("第一张图片路径不存在")

        # 加载第一张图片
        try:
            self.img_first = pygame.image.load(self.image1_path).convert_alpha()
        except Exception as e:
            print(f"Error loading first image: {e}")
            raise

        # 检查第二张图片
        if not os.path.exists(self.image2_path):
            self.single_image_mode = True
            self.img_second = None
        else:
            try:
                self.img_second = pygame.image.load(self.image2_path).convert_alpha()
                # 检查图片大小是否一致
                if self.img_first.get_width() != self.img_second.get_width():
                    raise Exception("导入的图片大小不一")
            except Exception as e:
                print(f"Error loading second image: {e}")
                self.single_image_mode = True
                self.img_second = None

        # 获取尺寸
        w = self.img_first.get_width()
        h = self.img_first.get_height()

        # 位置和大小
        self.rect = pygame.Rect(x, y, w, h)

        if not self.single_image_mode:
            # 过渡相关属性
            self.transition_duration = 1000
            self.is_transitioning = False
            self.transition_start_time = 0
            self.show_first = True

            # 缩放图片并创建副本
            self.img_first = pygame.transform.scale(self.img_first, (w, h))
            self.img_second = pygame.transform.scale(self.img_second, (w, h))
            self.current_first = self.img_first.copy()
            self.current_second = self.img_second.copy()
        else:
            # 单图片模式只需要缩放第一张图片, 如果是单图片模式，就不需要设置过渡相关的属性
            self.img_first = pygame.transform.scale(self.img_first, (w, h))
        self.start_transition()

    @staticmethod
    def ease_in_out_cubic(x):
        """缓动函数"""
        if x < 0.5:
            return 4 * x * x * x
        else:
            return 1 - pow(-2 * x + 2, 3) / 2

    def draw(self, surf):
        """
        绘制图像
        :param surf: pygame的显示表面
        """
        if self.single_image_mode:
            # 单图片模式直接绘制第一张图片
            surf.blit(self.img_first, self.rect)
            return

        current_time = pygame.time.get_ticks()

        if self.is_transitioning:
            progress = (current_time - self.transition_start_time) / self.transition_duration
            if progress >= 1:
                progress = 1
                self.is_transitioning = False

            eased_progress = self.ease_in_out_cubic(progress)

            if self.show_first:
                # 过渡到第一张图片
                surf.blit(self.img_first, self.rect)
                self.current_second.set_alpha(int(255 * (1 - eased_progress)))
                surf.blit(self.current_second, self.rect)
            else:
                # 过渡到第二张图片
                surf.blit(self.img_second, self.rect)
                self.current_first.set_alpha(int(255 * (1 - eased_progress)))
                surf.blit(self.current_first, self.rect)
        else:
            # 不在过渡状态时只显示当前图片
            if self.show_first:
                surf.blit(self.img_first, self.rect)
            else:
                surf.blit(self.img_second, self.rect)

    def update(self, event_list):
        """
        更新状态
        :param event_list: pygame事件列表
        :return: 是否发生了状态改变
        """
        if self.single_image_mode:
            return False

        if not self.once_flag:
            mpos = pygame.mouse.get_pos()

            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect.collidepoint(mpos) and not self.is_transitioning:
                        self.start_transition()
                        return True

        if self.auto_motion_flag:
            # print(1)
            # 每隔5秒更新图片
            if pygame.time.get_ticks() - self.image_refresh_time >= self.image_change_time:
                if not self.motion_done_flag:
                    # 更新索引
                    self.current_index += 1
                    self.image_refresh_time = pygame.time.get_ticks()

                    if self.current_index >= len(self.image_path_ls) - 1:
                        self.current_index = 0  # 循环回到开头
                        self.motion_done_flag = True  # 设置 motion_done_flag 为 True

                    self.multistage_transformation()

        return False

    def start_transition(self):
        """开始过渡动画"""
        if self.single_image_mode:
            return

        self.is_transitioning = True
        self.transition_start_time = pygame.time.get_ticks()
        self.show_first = not self.show_first
        self.current_first = self.img_first.copy()
        self.current_second = self.img_second.copy()

    def multistage_transformation(self):
        if self.is_transitioning or self.motion_done_flag:
            return  # 如果正在过渡，则不执行任何操作

        # 更新过渡框
        self.init_setting(
            self.x, self.y,
            self.image_path_ls[self.current_index],
            self.image_path_ls[self.current_index + 1],
            False)

    def refresh_settings(self, x, y, image1_path, image2_path, once_flag,
                         image_path_ls, auto_motion_flag, motion_done_flag):

        self.x = x
        self.y = y

        self.auto_motion_flag = auto_motion_flag
        self.motion_done_flag = motion_done_flag

        if image_path_ls:
            self.auto_motion_flag = True
            self.motion_done_flag = False
            if once_flag:
                raise Exception('单图片模式不可和连续切换模式同时启动')
        else:
            self.auto_motion_flag = False

        # 刷新和索引管理
        self.image_refresh_time = pygame.time.get_ticks()
        self.current_index = 0
        self.image_path_ls = image_path_ls

        if self.image_path_ls:
            if once_flag == auto_motion_flag == True:
                raise Exception('单图片模式不可和连续切换模式同时启动')

            # 如果图片路径列表只有两张图片，则禁用自动切换
            if len(self.image_path_ls) == 2:
                self.auto_motion_flag = False

            image_num = random.randint(2, 5)
            path_ls = random.sample(self.image_path_ls, image_num)
            # print(len(path_ls))
            self.image_path_ls = [image1_path, image2_path] + path_ls
            # print(self.image_path_ls)

        # 初始化设置
        self.init_setting(x, y, image1_path, image2_path, once_flag)
        return self.image_path_ls


# 使用示例
if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((800, 1000))
    transition_box = None
    path_ls = [f'../role_cards/朝武芳乃/portrait/+/{file}'
               for file in os.listdir(rf'../role_cards/朝武芳乃\portrait/+/')]

    # 创建图片过渡框
    try:
        transition_box = ImageTransitionBox(
            100, 100,
            r"..\role_cards\朝武芳乃\portrait\!!-\芳乃a_0_1863_1934.png",
            r"..\role_cards\朝武芳乃\portrait\!!-\芳乃a_0_1862_1934.png",
            once_flag=True)
    except Exception as e:
        print(f"Failed to create transition box: {e}")
        pygame.quit()
        exit()

    running = True

    while running:
        clock.tick(60)
        event_list = pygame.event.get()

        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
            # 检测鼠标右键按下事件
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                # transition_box.image_change_time = 5000
                # 右键点击时的处理
                print("右键被点击")
                if not transition_box.is_transitioning:
                    a = transition_box.refresh_settings(100, 100,
                                                        r"..\role_cards\朝武芳乃\portrait\!!-\芳乃a_0_1863_1934.png",
                                                        r"..\role_cards\朝武芳乃\portrait\!!-\芳乃a_0_1862_1934.png",
                                                        image_path_ls=path_ls, once_flag=False,
                                                        auto_motion_flag=False, motion_done_flag=False)
                    print(a)
            # 捕获鼠标中键（滚轮）点击事件
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                print("鼠标滚轮被点击")
                if not transition_box.is_transitioning:
                    transition_box.init_setting(100, 100,
                                                r"..\role_cards\朝武芳乃\portrait\!!-\芳乃a_0_1863_1934.png",
                                                r"..\role_cards\朝武芳乃\portrait\!!-\芳乃a_0_1862_1934.png",
                                                once_flag=False)

        # 更新过渡框状态
        transition_box.update(event_list)

        # 绘制
        window.fill((128, 128, 128))
        transition_box.draw(window)
        pygame.display.flip()

    pygame.quit()
    exit()
