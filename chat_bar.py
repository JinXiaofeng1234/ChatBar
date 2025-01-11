import pygame
import sys
import os
from llm_api_request import chat_with_model
from start_ollama import start_ollama
from ChatBar.prompt_reader import read_txt, read_json, save_memory_json, \
    save_conversation_history, save_json
from music_player import MusicPlayer
from get_voice import play_voice_async, play_sound_async
from files_sort import list_files_sorted_by_time
from langchain import search_answer, read_data, history_token_calculate, single_line_token_calculate
from vector_retrieval import KnowledgeBase
from text_line_feed_split import TextLineFeed
import random
from speech_recognition import voice_recognition, close_stream
from web_search import WebScarp
from setting_menu import ScreenBoard
import character_image_clipping
from npc import IntelligentAgent
import copy
from upload_image import ImageUploader
from select_box import OptionBox
from confirm_time import get_current_time_period
from daily_task_creator import create_daily_schedule, get_date
from clock import CLOCK
import pyperclip
from role_cards_selector import FolderSelector


class DialogWindow:
    def __init__(self):
        # === 颜色常量 ===
        self.RED = None
        self.BLACK = None
        self.DARK_GRAY = None
        self.GRAY = None
        self.WHITE = None

        # === UI图标资源 ===
        self.tick_icon = None
        self.music_icon = None
        self.disabled_icon = None
        self.music_disabled_icon = None
        self.setting_icon = None
        self.role_switch_icon = None
        self.switch_role_button = None
        self.setting_image_transformed = None
        self.music_image_transformed = None
        self.image_upload_image_transformed = None
        self.speech_icon_image_transformed = None
        self.switch_image_transformed = None

        # === UI按钮元素 ===
        self.room_select_box = None
        self.speech_recognition_button = None
        self.net_work_adapt_button = None
        self.database_adapt_button = None
        self.image_upload_button = None
        self.setting_button = None
        self.music_button = None
        self.min_button = None
        self.close_button = None
        self.send_button = None
        self.send_button_font = None
        self.send_disable_flag = None
        self.send_button_clicked = None

        # === UI文本和字体 ===
        self.status_bar_font = None
        self.label_font = None
        self.character_name_font = None
        self.text_surface = None
        self.text_rect = None
        self.show_text = None
        self.character_name_text_rect = None
        self.character_name_text_surface = None

        # === UI布局和状态 ===
        self.WIDTH = None
        self.HEIGHT = None
        self.screen = None
        self.background = None
        self.status_bar = None
        self.status_bar_rect = None
        self.setting_menu = None
        self.input_box = None
        self.img_size = None
        self.image = None
        self.image_size = None

        # === 房间相关 ===
        self.room_name_ls = None
        self.room_ls = None

        # === 时钟和计时器 ===
        self.clock = None
        self.clock_widget = None
        self.pointer_clock_time = None
        self.time_period_now = None
        self.button_press_time = None
        self.button_press_duration = None
        self.delete_interval = None
        self.delete_timer = None

        # === 输入控制 ===
        self.backspace_pressed = None
        self.cursor_flag = None

        # === 模型配置 ===
        self.model_list = None
        self.speech_gen_model_list = None
        self.vision_mode = None

        # === LLM 相关 ===
        self.llm_response_text = None
        self.llm_response_text_filtered = None
        self.llm_response_text_analysis_flag = False
        self.llm_process_flag = None
        self.token_num = None
        self.token_num_save_flag = True
        self.response_text_length = None
        self.out_put_rules = None

        # === 角色状态相关 ===
        self.character_statu_dic = None
        self.character_name_text = None
        self.character_image = None
        self.character_image_path = None
        self.avatar = None
        self.agent = None
        self.relationship = None
        self.relationship_dict = None
        self.favorability_bonus_multiplier = None

        # === 状态显示元素 ===
        self.trust_value_text_rect = None
        self.trust_value_text_surface = None
        self.favorability_text_rect = None
        self.favorability_text_surface = None
        self.relationship_text_rect = None
        self.relationship_text_surface = None
        self.change_btn_flag = None

        # === 对话和输入相关 ===
        self.conversation_history = None
        self.conversation_history_original_length = None
        self.standard_conversation_history = None
        self.prompt = None
        self.prompt_index = None
        self.user_text = None
        self.filtered_index_ls = None

        # === 调度和时间相关 ===
        self.schedule_dic = None
        self.daily_schedule_dic = None
        self.event_list = None
        self.time_check_point = 0

        # === 系统标志位 ===
        self.refresh_status_flag = None
        self.refresh_dialogue_flag = None
        self.data_base_able_flag = False
        self.net_work_able_flag = False
        self.music_stop_flag = False
        self.menu_able_flag = False
        self.microphone_able_flag = None
        self.jieba_search_kw_flag = True

        # === 文件和路径 ===
        self.role_cards_path = None
        self.upload_image_file_path = None

        # === 配置和设置 ===
        self.setting_ls = [0, 0, 0, 0, 0]
        self.current_select_speech_gen_model_index = 0
        self.selected_option_index = 0
        self.sound_text = None

        # === 数据和存储 ===
        self.data = None
        self.v_kb = None
        self.latest_saving = None
        self.music_player = None

        # === 语音合成音色相关 ===
        self.recho_role_key = None
        self.fish_role_key = None
        self.role_key_ls = None

        # === 环境设置 ===
        os.environ["SDL_IME_SHOW_UI"] = "1"

        pygame.init()

        self.role_cards_path = 'role_cards/樱井惠/'
        self.role_init()
        self.game_init()

    def game_init(self):
        # 设置窗口尺寸
        self.WIDTH, self.HEIGHT = 1024, 860
        self.screen = pygame.display.set_mode((1024, 860), pygame.NOFRAME)
        pygame.display.set_caption("AI伙伴")

        # 加载时钟
        self.clock_widget = CLOCK(825, 79, 'imgs/icon/clock.png')

        # 获取时间段
        self.time_period_now = get_current_time_period()['description'][0]

        """ 导入图片 """
        self.tick_icon = pygame.image.load("imgs/icon/tick_icon.png")
        self.music_icon = pygame.image.load('imgs/icon/music_icon.png')
        self.disabled_icon = pygame.image.load('imgs/icon/red_line_icon.png')
        self.music_disabled_icon = pygame.image.load('imgs/icon/music_stop_icon.png')
        self.setting_icon = pygame.image.load('imgs/icon/setting_icon.png')
        self.role_switch_icon = pygame.image.load('imgs/icon/role_switch_icon.png')
        # 加载语音识别icon
        speech_icon_image = pygame.image.load("imgs/icon/sound_icon.png")
        # 加载图像上传按钮
        image_upload_image = pygame.image.load('imgs/icon/image_outline_icon.png')
        # 加载背景图
        self.room_name_ls = ['门厅', '餐厅', '客厅', '女生卧室', '房东卧室', '女性洗浴间', '男性洗浴间']
        self.room_ls = ['doorroom', 'dinning_room', 'living_room', 'npc_bedroom', 'player_bedroom',
                        'washroom', 'washroom']
        self.background = pygame.image.load(f'imgs/black_room/doorroom/{self.time_period_now}.png')

        # 初始化音频
        pygame.mixer.init()

        # 初始化背景音乐
        bgm_list = [fr'bgm\{music}' for music in os.listdir('bgm') if music.endswith('.mp3')]

        # 导入视觉任务提示词字典
        self.vision_mode = read_json('vision_mode/vision_mode.json')["vision_dict"]

        # 定义按钮颜色刷新机制
        self.button_press_time = 0
        self.button_press_duration = 200  # 按钮按下持续时间（毫秒）
        self.send_button_clicked = False
        self.send_disable_flag = False

        # 定义颜色
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (150, 150, 150)
        self.BLACK = (0, 0, 0)
        self.RED = (0, 0, 255)

        # 定义对话框刷新标记
        self.refresh_dialogue_flag = False

        # 初始化下拉框
        self.model_list = ["千问2.5-14b-128K", "文心一言4.0-128K", "通义千问Plus"]
        self.speech_gen_model_list = ['recho', 'fish']
        self.setting_menu = ScreenBoard(400, 580, 312, 140)  # 基活菜单

        # 文本输入框设置
        self.input_box = pygame.Rect(int(self.WIDTH * 0.072), int(self.HEIGHT * 0.918),
                                     int(self.WIDTH * 0.745), int(self.HEIGHT * 0.053))

        # 设置字体
        self.label_font = pygame.font.SysFont('SimHei', 24)
        self.send_button_font = pygame.font.SysFont('SimHei', 32)

        self.character_name_font = pygame.font.SysFont('SimHei', 32)
        self.character_name_font.set_italic(True)
        self.status_bar_font = pygame.font.SysFont('SimHei', 20)

        # 设定人物状态栏
        self.create_status()

        self.refresh_status()

        self.status_bar_rect = self.status_bar.get_rect(center=(int(self.WIDTH * 0.217), int(self.HEIGHT * 0.116)))
        # 创建半透明图片
        self.image_size = (int(self.WIDTH * 0.859), int(self.HEIGHT * 0.330))
        self.image = pygame.Surface(self.image_size, pygame.SRCALPHA)
        self.image.fill((100, 100, 100, 128))  # 灰色，半透明

        self.draw_character_name()  # 绘制人物名字

        # 发送按钮
        self.send_button = pygame.Rect(int(self.WIDTH * 0.831), int(self.HEIGHT * 0.912),
                                       int(self.WIDTH * 0.097), int(self.HEIGHT * 0.066))
        # 关闭按钮
        self.close_button = pygame.Rect(int(self.WIDTH * 0.952), 0,
                                        int(self.WIDTH * 0.049), int(self.HEIGHT * 0.058))

        # 最小化按钮
        self.min_button = pygame.Rect(int(self.WIDTH * 0.902), 0,
                                      int(self.WIDTH * 0.049), int(self.HEIGHT * 0.058))
        # 音乐播放按钮
        self.music_button = pygame.Rect(int(self.WIDTH * 0.854), 0,
                                        int(self.WIDTH * 0.049), int(self.HEIGHT * 0.058))

        # 设置按钮
        self.setting_button = pygame.Rect(824, 0, 50, 50)

        # 角色切换按钮
        self.switch_role_button = pygame.Rect(774, 0, 50, 50)

        # 图像识别按钮
        self.image_upload_button = pygame.Rect(int(self.WIDTH * 0.027), int(self.HEIGHT * 0.917),
                                               int(self.WIDTH * 0.041), int(self.HEIGHT * 0.055))

        # 语音识别按钮
        self.speech_recognition_button = pygame.Rect(int(self.WIDTH * 0.931), int(self.HEIGHT * 0.912),
                                                     int(self.WIDTH * 0.041), int(self.HEIGHT * 0.066))
        # 场景选择按钮
        self.room_select_box = OptionBox(
            72, 430, 160, 50, (150, 150, 150), (100, 200, 255), pygame.font.SysFont('simhei', 30),
            self.room_name_ls)

        # 知识库启用按钮
        self.database_adapt_button = pygame.Rect(int(self.WIDTH * 0.736), int(self.HEIGHT * 0.497),
                                                 int(self.WIDTH * 0.097), int(self.HEIGHT * 0.066))

        # 网络启用按钮
        self.net_work_adapt_button = pygame.Rect(int(self.WIDTH * 0.834), int(self.HEIGHT * 0.497),
                                                 int(self.WIDTH * 0.097), int(self.HEIGHT * 0.066))

        # 调整图片大小以适应rect
        self.speech_icon_image_transformed = pygame.transform.scale(speech_icon_image,
                                                                    (self.speech_recognition_button.width,
                                                                     self.speech_recognition_button.height))
        self.image_upload_image_transformed = pygame.transform.scale(image_upload_image,
                                                                     (self.image_upload_button.width,
                                                                      self.image_upload_button.height))
        self.music_image_transformed = pygame.transform.scale(self.music_icon,
                                                              (self.music_button.width,
                                                               self.music_button.height))
        self.setting_image_transformed = pygame.transform.scale(self.setting_icon,
                                                                (self.setting_button.width,
                                                                 self.setting_button.height))
        self.switch_image_transformed = pygame.transform.scale(self.role_switch_icon,
                                                               (self.switch_role_button.width,
                                                                self.switch_role_button.height))

        # 光标设置
        self.clock = pygame.time.Clock()
        self.pointer_clock_time = 0
        self.cursor_flag = False
        self.show_text = ''

        # 删除设置
        self.backspace_pressed = False

        # 控制删除速度的计时器
        self.delete_timer = 0
        self.delete_interval = 100  # 毫秒

        # 初始化音乐播放器
        self.music_player = MusicPlayer(bgm_list)  # 替换为你的音乐文件路径
        self.music_player.start()  # 启动播放音乐
        play_sound_async(self.role_cards_path)  # 播放欢迎语句

    def create_status(self):
        self.img_size = (int(self.WIDTH * 0.293), int(self.HEIGHT * 0.149))
        self.status_bar = pygame.Surface(self.img_size, pygame.SRCALPHA)
        self.status_bar.fill((100, 100, 100, 128))  # 灰色，半透明
        self.status_bar.blit(self.avatar, (0, 0))

    def draw_character_name(self):
        self.character_name_text_surface = self.character_name_font.render(f'〖{self.character_name_text}〗:',
                                                                           True, (255, 255, 255))
        self.character_name_text_rect = self.character_name_text_surface.get_rect(center=(75, 25))
        self.text_surface = self.label_font.render(f'『{self.llm_response_text}』', True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(self.image_size[0] // 2, self.image_size[1] // 2))
        # 将文字绘制到图片上
        self.image.blit(self.text_surface, self.text_rect)
        self.image.blit(self.character_name_text_surface, self.character_name_text_rect)

    def role_init(self):
        self.agent = IntelligentAgent(0, 0, 0, 0, 0, 0, 0, 0)
        self.agent.name = self.role_cards_path.split('/')[-2]
        self.character_name_text = self.agent.name
        # 加载语音文字
        self.sound_text = read_json(f'{self.role_cards_path}example_sound/sound_text.json')['txt']
        self.recho_role_key = read_json(f'{self.role_cards_path}example_sound/sound_text.json')["recho_role_key"]
        self.fish_role_key = read_json(f'{self.role_cards_path}example_sound/sound_text.json')["fish_role_key"]
        self.role_key_ls = [self.recho_role_key, self.fish_role_key]
        # 加载头像
        self.avatar = pygame.image.load(f'{self.role_cards_path}avatar/avatar.png')
        # 载入向量化数据库
        self.data = read_data(f'{self.role_cards_path}character_info/qa_info.json')
        self.v_kb = KnowledgeBase(f'{self.role_cards_path}character_info/kb.txt', 1)
        # 读入日程字典
        self.daily_schedule_dic = read_json(f'{self.role_cards_path}actions.json')
        # 初始化对话历史
        self.conversation_history = list()
        # 设定用户回复
        self.user_text = ''
        # 加载人物状态机
        portrait_path = f'{self.role_cards_path}portrait'
        # print(os.listdir(f'{portrait_path}/0'))
        self.character_statu_dic = {'0': [f'{portrait_path}/0/{file}' for file in os.listdir(f'{portrait_path}/0')],
                                    '+': [f'{portrait_path}/+/{file}' for file in os.listdir(f'{portrait_path}/+')],
                                    '!+': [f'{portrait_path}/!+/{file}'
                                           for file in os.listdir(f'{portrait_path}/!+')],
                                    '!!+': [f'{portrait_path}/!!+/{file}'
                                            for file in os.listdir(f'{portrait_path}/!!+')],
                                    '-': [f'{portrait_path}/-/{file}' for file in os.listdir(f'{portrait_path}/-')],
                                    '!-': [f'{portrait_path}/!-/{file}'
                                           for file in os.listdir(f'{portrait_path}/!-')],
                                    '!!-': [f'{portrait_path}/!!-/{file}'
                                            for file in os.listdir(f'{portrait_path}/!!-')],
                                    '~': [f'{portrait_path}/~/{file}' for file in os.listdir(f'{portrait_path}/~')],
                                    '!~': [f'{portrait_path}/!~/{file}'
                                           for file in os.listdir(f'{portrait_path}/!~')],
                                    '!!~': [f'{portrait_path}/!!~/{file}'
                                            for file in os.listdir(f'{portrait_path}/!!~')]
                                    }
        # self.character_image = pygame.image.load("imgs/nahida.png")
        # 检查存档
        memory_ls = list_files_sorted_by_time(rf'{self.role_cards_path}saving')
        # 导入输出规则和提示词
        self.out_put_rules = read_txt(f'{self.role_cards_path}prompt/output_rules.txt')
        self.prompt = read_txt(f'{self.role_cards_path}prompt/special_role_player_prompt.txt')
        if not memory_ls:
            self.conversation_history.append({"role": "system", "content": self.prompt})
            self.conversation_history.append({"role": "system", "content": self.out_put_rules})
            llm_response_text = read_json(f'{self.role_cards_path}opening_statement.json')['Opening statement']
            self.conversation_history.append({"role": "assistant", "content": llm_response_text})
            self.llm_response_text = llm_response_text
        elif len(memory_ls) == 1:
            self.latest_saving = read_json(memory_ls[0])
            self.conversation_history = self.latest_saving["memory"]
            self.llm_response_text = self.conversation_history[-1]['content']
        else:
            self.latest_saving = read_json(memory_ls[-1])
            self.conversation_history = self.latest_saving["memory"]
            self.llm_response_text = self.conversation_history[-1]['content']
        schedule_tuple = None
        if self.latest_saving:
            if self.latest_saving["date"] != str(get_date()):  # 引入日程计划
                schedule_tuple = create_daily_schedule(data_dic=self.daily_schedule_dic, daily_flag=False)
            elif self.latest_saving["daily_schedule_dic"]:
                schedule_tuple = create_daily_schedule(data_dic=self.daily_schedule_dic, daily_flag=True,
                                                       dic_schedule=self.latest_saving["daily_schedule_dic"])
        else:
            schedule_tuple = create_daily_schedule(data_dic=self.daily_schedule_dic, daily_flag=False)
        self.schedule_dic = schedule_tuple[0]
        schedule_string = schedule_tuple[1]
        # 移除原来的提示词和输出规则
        self.remove_old_prompt()
        # 移动提示词和输出规则
        self.conversation_history.append({"role": "system", "content": self.prompt})
        self.conversation_history.append({"role": "system", "content": self.out_put_rules})
        self.conversation_history.append({"role": "system", "content": schedule_string})
        # print(self.conversation_history)
        self.conversation_history_original_length = len(self.conversation_history)
        self.prompt_index = self.conversation_history_original_length - 3  # 定位提示词索引值
        # 计算上下文token总数
        if 'token_num.json' in os.listdir(self.role_cards_path):
            # print(1)
            self.token_num = read_json(f'{self.role_cards_path}token_num.json')["token_num"]
            self.token_num += single_line_token_calculate(schedule_string)
        else:
            self.token_num = history_token_calculate(self.conversation_history)
        if self.llm_response_text:
            self.response_text_length = len(self.llm_response_text)
            self.refresh_dialogue_flag = True
        # 定义人物关系字典
        self.relationship_dict = {0: '陌生人', 1: '熟人', 2: '朋友', 3: '暧昧', 4: '恋人', 5: '未婚夫妇', 6: '夫妻'}
        if self.latest_saving:
            self.agent.relationship_index = self.latest_saving["relationship_index"]
            self.agent.favorability = self.latest_saving["favorability"]
            self.agent.trust_value = self.latest_saving['trust_value']
        else:
            self.agent.relationship_index = 0
            self.agent.favorability = 0
        self.relationship = self.relationship_dict[self.agent.relationship_index]
        self.character_img_and_relationship_change()
        # 设定人物立绘图片和信任度
        if not self.character_image:
            if self.latest_saving:
                self.character_image = pygame.image.load(self.latest_saving["character_img"])

            else:
                # print(random.sample(self.character_statu_dic['0'], 1))
                self.character_image = character_image_clipping.crop_image(
                    random.sample(self.character_statu_dic['0'], 1)[0], 864)
        # 设定角色卡人物名字
        if not self.character_name_text:
            if self.latest_saving:
                self.character_name_text = self.latest_saving['name']
            else:
                self.character_name_text = '智能体'

    def switch_role(self):
        role_cards_path = FolderSelector().get_folder_path('role_cards')
        if role_cards_path and self.role_cards_path != role_cards_path:
            self.role_cards_path = role_cards_path
            self.latest_saving = None  # 清空此前角色存档
            self.character_image = None  # 清空过往角色立绘
            self.standard_conversation_history = None  # 清空备份聊天记录
            self.token_num = None  # 清空token计数
            self.role_init()  # 初始化人物卡
            self.create_status()
            self.refresh_status()  # 刷新人物关系状态栏
            self.draw_character_name()
            play_sound_async(self.role_cards_path)  # 播放欢迎语句

    def remove_old_prompt(self):
        self.filtered_index_ls = list()
        for index, item_dic in enumerate(self.conversation_history):
            if item_dic["role"] == 'system':
                if item_dic["content"] == self.prompt or item_dic["content"] == self.out_put_rules:
                    self.filtered_index_ls.append(index)
        self.conversation_history = [item_dic for index, item_dic in enumerate(self.conversation_history)
                                     if index not in self.filtered_index_ls]

    def draw_button(self, bg_color, btn, font, text, text_color, offset_x, offset_y, icon_flag=False, icon_img=None):
        pygame.draw.rect(self.screen, bg_color, btn)
        close_btn_text = font.render(text, True, text_color)
        self.screen.blit(close_btn_text, (btn.x + offset_x, btn.y + offset_y))
        if icon_flag:
            icon_image_transformed = pygame.transform.scale(icon_img, (btn.width,
                                                                       btn.height))
            self.screen.blit(icon_image_transformed, btn)

    def refresh_status(self):
        self.status_bar.fill((100, 100, 100, 128), (128, 0, 172, 128))  # 灰色，半透明

        self.relationship_text_surface = self.status_bar_font.render(f'关系:{self.relationship}',
                                                                     True, (255, 255, 255))
        self.relationship_text_rect = self.relationship_text_surface.get_rect(center=(214, 16))
        self.status_bar.blit(self.relationship_text_surface, self.relationship_text_rect)

        self.favorability_text_surface = self.status_bar_font.render(f'好感度:{self.agent.favorability}',
                                                                     True, (255, 255, 255))
        self.favorability_text_rect = self.favorability_text_surface.get_rect(center=(214, 48))
        self.status_bar.blit(self.favorability_text_surface, self.favorability_text_rect)

        self.trust_value_text_surface = self.status_bar_font.render(f'信任度:{self.agent.trust_value}',
                                                                    True, (255, 255, 255))
        self.trust_value_text_rect = self.trust_value_text_surface.get_rect(center=(214, 80))
        self.status_bar.blit(self.trust_value_text_surface, self.trust_value_text_rect)

    def character_img_and_relationship_change(self):
        if self.llm_response_text_analysis_flag:
            prompt_refresh_flag = False
            self.llm_response_text_filtered = self.llm_response_text  # 初始化过滤回复
            llm_response_ls = self.llm_response_text.replace('『', '').replace('』', '').split(' ')
            if len(llm_response_ls) > 1:
                self.llm_response_text_filtered = "".join(llm_response_ls[1:])  # 整合过滤后的回复
            else:
                llm_response_ls.insert(0, '0')
            print(f'过滤后的回复:{self.llm_response_text_filtered}')
            # 播放音频
            play_voice_async(self.llm_response_text_filtered,
                             model_name=self.speech_gen_model_list[self.current_select_speech_gen_model_index],
                             path=self.role_cards_path, text=self.sound_text,
                             role_key=self.role_key_ls[self.current_select_speech_gen_model_index])

            for byte in llm_response_ls:
                if byte in self.character_statu_dic.keys():
                    relationship_change_value_dic = {'0': 0, '+': random.uniform(0.1, 1),
                                                     '!+': random.uniform(1, 2), '!!+': random.uniform(2, 4),
                                                     '-': random.uniform(-10, -1),
                                                     '!-': random.uniform(-20, -10), '!!-': random.uniform(-40, -20)
                                                     }
                    self.character_image_path = random.sample(self.character_statu_dic[byte], 1)[0]
                    self.character_image = character_image_clipping.crop_image(self.character_image_path, 864)

                    if byte not in relationship_change_value_dic:
                        self.favorability_bonus_multiplier = len(byte)
                    else:
                        self.favorability_bonus_multiplier = 0

                    if byte in relationship_change_value_dic:
                        relationship_change_value = relationship_change_value_dic[byte]

                        # 加权好感度
                        if self.favorability_bonus_multiplier:
                            relationship_change_value *= self.favorability_bonus_multiplier

                        self.agent.favorability += round(relationship_change_value)
                        if 100 > self.agent.trust_value > -100:
                            if relationship_change_value > 0:
                                self.agent.trust_value += round(relationship_change_value * 0.3)
                            else:
                                self.agent.trust_value += round(relationship_change_value)
                        # 检查并处理 favorability 的边界情况
                        if self.agent.favorability >= 100:
                            if self.agent.relationship_index < 6:  # 确保不会超出上限
                                self.agent.relationship_index += 1
                                self.agent.favorability = 0
                                prompt_refresh_flag = True
                            else:
                                self.agent.favorability = 0
                        elif self.agent.favorability <= -100:
                            if self.agent.relationship_index > 0:  # 确保不会低于下限
                                self.agent.relationship_index -= 1
                                self.agent.favorability = 0
                            else:
                                self.relationship = '仇人'
                                self.agent.favorability = 0
                            prompt_refresh_flag = True
                    self.relationship = self.relationship_dict[self.agent.relationship_index]
                    print(self.relationship, self.agent.favorability)
                    if prompt_refresh_flag:
                        prompt_format = read_txt(f'{self.role_cards_path}prompt/special_role_player_prompt_format.txt')
                        new_prompt = prompt_format.format(relationship=self.relationship,
                                                          favorability=self.agent.favorability,
                                                          place='门厅')
                        self.conversation_history[self.prompt_index]["content"] = new_prompt
                    self.llm_response_text_analysis_flag = False
                    self.refresh_status_flag = True

                    return
            else:
                self.character_image_path = random.sample(self.character_statu_dic['0'], 1)[0]
                self.character_image = character_image_clipping.crop_image(self.character_image_path, 864)
            print(self.character_image)
            self.llm_response_text_analysis_flag = False

    def change_button_color(self, color):
        button_color = color
        pygame.draw.rect(self.screen, button_color, self.send_button)
        send_text = self.send_button_font.render('发送', True, self.BLACK)
        self.screen.blit(send_text, (self.send_button.x + 17, self.send_button.y + 10))

    def handle_events(self):
        self.event_list = pygame.event.get()
        for event in self.event_list:
            if event.type == pygame.QUIT:
                self.app_shut_down_func()
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.send_button.collidepoint(event.pos):
                    if self.user_text:
                        if not self.send_disable_flag:
                            # 将用户输入添加到对话历史
                            # self.conversation_history.append({"role": "user", "content": self.user_text})
                            self.llm_process_flag = True
                            self.send_disable_flag = True
                    self.send_button_clicked = True
                    self.button_press_time = pygame.time.get_ticks()

                if self.close_button.collidepoint(event.pos):
                    self.app_shut_down_func()
                    return False

                if self.min_button.collidepoint(event.pos):
                    pygame.display.iconify()

                if self.setting_button.collidepoint(event.pos):
                    self.menu_able_flag = not self.menu_able_flag

                if self.music_button.collidepoint(event.pos):
                    self.music_stop_flag = not self.music_stop_flag
                    if not self.music_stop_flag:
                        self.music_player.start()
                    else:
                        self.music_player.stop()

                if self.switch_role_button.collidepoint(event.pos):
                    self.switch_role()

                if self.speech_recognition_button.collidepoint(event.pos):
                    res_json = voice_recognition(model_flag=False)
                    if res_json:
                        self.user_text += res_json['result'][0]
                    elif res_json is None:
                        print('未识别出结果')
                    else:
                        self.microphone_able_flag = False

                if self.database_adapt_button.collidepoint(event.pos):
                    self.data_base_able_flag = not self.data_base_able_flag

                if self.net_work_adapt_button.collidepoint(event.pos):
                    self.net_work_able_flag = not self.net_work_able_flag

                if self.image_upload_button.collidepoint(event.pos):
                    self.upload_image_file_path = ImageUploader().get_image_path()

            if event.type == pygame.KEYDOWN:
                # 获取所有按键状态
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LCTRL] and keys[pygame.K_v]:
                    current_content = pyperclip.paste()
                    self.user_text += current_content

                if event.key == pygame.K_BACKSPACE:
                    self.backspace_pressed = True
                    self.delete_timer = pygame.time.get_ticks()  # 重置计时器
                elif event.key == pygame.K_RETURN:
                    if self.user_text:
                        if not self.send_disable_flag:
                            self.llm_process_flag = True
                            self.send_disable_flag = True
                    self.send_button_clicked = True
                    self.button_press_time = pygame.time.get_ticks()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.backspace_pressed = False

            if event.type == pygame.TEXTINPUT:
                self.user_text += event.text

        return True

    def app_shut_down_func(self):
        self.music_player.stop()
        if self.microphone_able_flag:
            close_stream()
        conversation_history_current_length = len(self.conversation_history)
        if conversation_history_current_length > 2 \
                and conversation_history_current_length > self.conversation_history_original_length:
            if self.standard_conversation_history:
                self.standard_conversation_history[self.prompt_index]["content"] = \
                    self.conversation_history[self.prompt_index]["content"]
                self.standard_conversation_history = self.standard_conversation_history + \
                                                     self.conversation_history[len(self.standard_conversation_history):]
            else:
                self.standard_conversation_history = self.conversation_history.copy()
            self.schedule_dic = {str(k): v for k, v in self.schedule_dic.items()}  # 日程表字典键进行字符串化
            saving = {"name": self.character_name_text, "relationship_index": self.agent.relationship_index,
                      "favorability": self.agent.favorability, "character_img": self.character_image_path,
                      "trust_value": self.agent.trust_value,
                      "date": str(get_date()),
                      "daily_schedule_dic": self.schedule_dic,
                      "memory": self.standard_conversation_history}
            save_memory_json(saving, self.role_cards_path)
            if self.token_num_save_flag:
                save_json({"token_num": self.token_num}, 'token_num', self.role_cards_path)

    def agent_response(self):
        if self.llm_process_flag:
            if self.token_num >= 64000:
                save_conversation_history(self.conversation_history)
                self.conversation_history = self.conversation_history[self.prompt_index:]
                self.prompt_index = 0
                self.token_num = history_token_calculate(self.conversation_history)

            # remove_flag = False
            ai_info = f'\nYour Status Parameters:[你和用户的关系:{self.relationship};' \
                      f'你对用户的好感度:{self.agent.favorability};你对用户的信任值:{self.agent.trust_value};' \
                      f'你的心情:平静;突发情况:无]'

            if self.setting_ls[4] == 0:
                vision_model_prompt = self.user_text
            else:
                vision_model_prompt = self.vision_mode[str(self.setting_ls[4])]

            if self.upload_image_file_path:
                conversation_history = [{
                    'role': 'user',
                    'content': vision_model_prompt,
                    'images': [fr"{self.upload_image_file_path}"]
                }]
                image_describe = chat_with_model(conversation_history, 'vision')[0]
                ai_info = f'{ai_info[:-1]};你看到的视觉信息:{image_describe}]'
                self.upload_image_file_path = None

            external_content = ai_info

            if self.user_text and (self.user_text.endswith('??') or self.data_base_able_flag):
                if self.setting_ls[2] == 0:
                    res_ls = search_answer(self.user_text, self.data)
                    res = "".join(res_ls)
                else:
                    res = self.v_kb.search(self.user_text)[0][0]

                if not res:
                    if self.net_work_able_flag:
                        # key_word = search_key_word(self.user_text, top_k_num=1)[0]
                        res = WebScarp().search_get(self.user_text)
                        if res is None:
                            res = "抱歉，暂未查询到结果"
                    else:
                        res = "抱歉，暂未查询到结果"

                external_content = self.external_data_query_result_processing(ai_info, res)

            elif self.net_work_able_flag:
                if '天气' in self.user_text:
                    res = WebScarp().autonavi_weather_forecast()
                else:
                    res = WebScarp().search_get(self.user_text)
                if res is None:
                    res = "抱歉，暂未查询到结果"
                external_content = self.external_data_query_result_processing(ai_info, res)

            else:
                # 将用户输入添加到对话历史
                self.conversation_history.append({"role": "user", "content": f'{self.user_text}{external_content}'})

            remove_flag = True
            back_tuple = chat_with_model(self.conversation_history, model=self.selected_option_index)
            if back_tuple is None:
                tokens = 0
                self.llm_response_text = '0 ...'
            else:
                tokens = back_tuple[1]
                self.llm_response_text = back_tuple[0]

            if tokens == 0:
                self.token_num += single_line_token_calculate(self.user_text)  # 计算token
            else:
                self.token_num = tokens
            if not self.token_num_save_flag:
                self.token_num_save_flag = True
            if remove_flag and external_content:
                self.conversation_history[-1]["content"] = self.conversation_history[-1]["content"]. \
                    replace(external_content, '').strip(' ')
            self.response_text_length = len(self.llm_response_text)
            # 将助手的回复添加到对话历史
            self.conversation_history.append({"role": "assistant", "content": self.llm_response_text})
            self.token_num += single_line_token_calculate(self.llm_response_text)  # 计算token
            self.refresh_dialogue_flag = True
            self.llm_process_flag = False
            self.user_text = ''
            self.send_disable_flag = False
            self.llm_response_text_analysis_flag = True

    def external_data_query_result_processing(self, ai_status, res):
        # 将用户输入添加到对话历史
        external_content = f'{ai_status}\nDataBase Result:[{res}]'
        self.conversation_history.append({"role": "user",
                                          "content": f'{self.user_text}{external_content}'})
        return external_content

    def update(self):

        flag = None

        self.clock_widget.update(self.event_list)  # 更新时钟

        self.character_img_and_relationship_change()
        current_time = pygame.time.get_ticks()

        if current_time - self.time_check_point >= 60000:  # 时间段检查
            self.time_period_now = get_current_time_period()['description'][0]
            self.time_check_point = current_time
            # print('一分钟过去了')

        current_setting_ls = self.setting_menu.update(self.event_list)
        if current_setting_ls is not None:
            if self.setting_ls != current_setting_ls:
                self.setting_ls = current_setting_ls.copy()
        current_select_model_index = self.setting_ls[0]

        current_select_speech_gen_model_index = self.setting_ls[1]
        if self.current_select_speech_gen_model_index != current_select_speech_gen_model_index:
            self.current_select_speech_gen_model_index = current_select_speech_gen_model_index
            print(f'已选择:{self.speech_gen_model_list[self.current_select_speech_gen_model_index]}')
        # 场景下拉框选择设定
        selected_room_index = self.room_select_box.update(self.event_list)
        if selected_room_index >= 0:
            self.background = pygame.image.load(f'imgs/black_room/'
                                                f'{self.room_ls[selected_room_index]}/{self.time_period_now}.png')

        if self.music_stop_flag:
            self.music_image_transformed = pygame.transform.scale(self.music_disabled_icon,
                                                                  (self.music_button.width,
                                                                   self.music_button.height))
        else:
            self.music_image_transformed = pygame.transform.scale(self.music_icon,
                                                                  (self.music_button.width,
                                                                   self.music_button.height))

        if self.selected_option_index == 0:
            flag = True

        if current_select_model_index >= 0:
            if self.selected_option_index != current_select_model_index:
                self.selected_option_index = current_select_model_index
                print(f'已选择:{self.model_list[self.selected_option_index]}')
                if self.selected_option_index != 0 and flag:
                    self.standard_conversation_history = copy.deepcopy(self.conversation_history)  # 备份聊天记录
                    for dic in self.conversation_history:
                        if dic['role'] == 'system':
                            dic['role'] = 'user'

                elif self.selected_option_index == 0 and not flag:
                    self.conversation_history = self.standard_conversation_history \
                                                + self.conversation_history[len(self.standard_conversation_history):]
            # print(self.standard_conversation_history)
            # print(self.conversation_history)

        if self.send_button_clicked:
            if current_time - self.button_press_time >= self.button_press_duration:
                self.change_btn_flag = True
                self.button_press_time = 0
                self.send_button_clicked = False

        if current_time - self.pointer_clock_time >= 500:
            self.cursor_flag = not self.cursor_flag
            self.pointer_clock_time = current_time

        if self.backspace_pressed and current_time - self.delete_timer > self.delete_interval:
            if self.user_text:
                self.user_text = self.user_text[:-1]
            self.delete_timer = current_time  # 重置计时器

    def draw(self):
        self.screen.fill((0, 0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.character_image, (int(self.WIDTH * 0.149), int(self.HEIGHT * 0.017)))

        pygame.draw.rect(self.screen, self.WHITE, self.input_box)
        pygame.draw.rect(self.screen, self.BLACK, self.input_box, 2)

        self.screen.blit(self.setting_image_transformed, self.setting_button)
        self.screen.blit(self.music_image_transformed, self.music_button)
        self.screen.blit(self.switch_image_transformed, self.switch_role_button)

        self.draw_button(self.GRAY, self.close_button, self.send_button_font, '×', self.DARK_GRAY, 12, 10)
        self.draw_button(self.GRAY, self.min_button, self.send_button_font, '-', self.DARK_GRAY, 12, 10)

        self.draw_button(self.GRAY, self.database_adapt_button, self.send_button_font,
                         '知识库', self.DARK_GRAY, 3, 12, self.data_base_able_flag, self.tick_icon)
        self.draw_button(self.GRAY, self.net_work_adapt_button, self.send_button_font,
                         '网络', self.DARK_GRAY, 15, 12, self.net_work_able_flag, self.tick_icon)
        self.screen.blit(self.speech_icon_image_transformed, self.speech_recognition_button)
        self.screen.blit(self.image_upload_image_transformed, self.image_upload_button)

        if self.refresh_status_flag:
            self.refresh_status()
            self.refresh_status_flag = False

        self.screen.blit(self.status_bar, self.status_bar_rect)

        if self.refresh_dialogue_flag:
            # 在屏幕中央绘制半透明图片
            self.image.fill((100, 100, 100, 128))  # 灰色，半透明
            max_num = int(self.image.get_width() / 24)
            if self.response_text_length + 2 < max_num:
                if '\n' not in self.llm_response_text:
                    self.text_surface = self.label_font.render(f'『{self.llm_response_text}』', True, (255, 255, 255))
                    self.text_rect = self.text_surface.get_rect(
                        center=(self.image_size[0] // 2, self.image_size[1] // 2))
                    self.image.blit(self.text_surface, self.text_rect)
                else:
                    text_ls = TextLineFeed(f'『{self.llm_response_text}』').type_judge()
                    for index, text in enumerate(text_ls):
                        self.text_surface = self.label_font.render(text, True, (255, 255, 255))

                        self.text_rect = self.text_surface.get_rect(
                            center=(self.image_size[0] // 2, self.image_size[1] // 2 + index * 32))
                        self.image.blit(self.text_surface, self.text_rect)
            else:
                self.llm_response_text = f'『{self.llm_response_text}』'
                text_ls = [self.llm_response_text[i:i + max_num] for i in range(0, self.response_text_length, max_num)]
                text_ls = TextLineFeed(text_ls).type_judge()
                for index, text in enumerate(text_ls):
                    self.text_surface = self.label_font.render(text, True, (255, 255, 255))

                    self.text_rect = self.text_surface.get_rect(
                        center=(self.image_size[0] // 2, self.image_size[1] // 2 + index * 32))
                    self.image.blit(self.text_surface, self.text_rect)

                # 将文字绘制到图片上
            self.image.blit(self.character_name_text_surface, self.character_name_text_rect)
            self.refresh_dialogue_flag = False
        image_rect = self.image.get_rect(center=(int(self.WIDTH * 0.5), int(self.HEIGHT * 0.728)))
        self.screen.blit(self.image, image_rect)

        self.show_text = f'{self.user_text}|' if self.cursor_flag else self.user_text
        text_surface = self.label_font.render(self.show_text, True, self.BLACK)
        self.screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 10))

        if not self.send_disable_flag:
            if self.change_btn_flag:
                self.change_button_color(self.DARK_GRAY)
                self.change_btn_flag = False
            else:
                self.change_button_color(self.GRAY)
        else:
            self.change_button_color(self.DARK_GRAY)

        if self.menu_able_flag:
            self.setting_menu.draw()
            self.screen.blit(self.setting_menu.surface, (self.setting_menu.x, self.setting_menu.y))

        self.room_select_box.draw(self.screen)  # 绘制场景选择下拉框

        self.clock_widget.draw(self.screen)  # 绘制时钟

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            pygame.key.start_text_input()
            pygame.key.set_text_input_rect(self.input_box)

            running = self.handle_events()
            self.update()
            self.draw()
            self.agent_response()

            self.clock.tick(60)
        self.music_player.stop()  # 确保在退出时停止音乐
        pygame.quit()
        sys.exit()


def lunch_chat():
    start_ollama()
    dialog_window = DialogWindow()
    dialog_window.run()


if __name__ == "__main__":
    lunch_chat()
