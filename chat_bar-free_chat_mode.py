import pygame
import sys
import os
from llm_api_request import chat_with_model
from start_ollama import start_ollama
from prompt_reader import read_txt, read_json, save_memory_json, \
    save_conversation_history, save_json
from music_player import MusicPlayer
from get_voice import play_voice_async, play_sound_async
from files_sort import list_files_sorted_by_time
from langchain import search_answer, read_data, history_token_calculate, single_line_token_calculate
from vector_retrieval import KnowledgeBase
from text_line_feed_split import TextLineFeed, clean_llm_response
import random
from speech_recognition import voice_recognition, close_stream
from web_search import WebScarp
from setting_menu import ScreenBoard
from npc import IntelligentAgent
import copy
from upload_file import ImageUploader
from select_box import OptionBox
from switch_character_pose_box import ImageTransitionBox
from confirm_time import get_current_time_period
from daily_task_creator import create_daily_schedule, get_date
from clock import CLOCK
import pyperclip
from role_cards_selector import FolderSelector
from cheater_app import TextInputter
from scroll_text_box import ScrollableTextBox
from index_check import index_check
from create_ai_info import creat_ai_info
from emotion_recognition import call_ai_api


class DialogWindow:
    def __init__(self):
        # === 颜色常量 ===
        self.RED = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.DARK_GRAY = (150, 150, 150)
        self.GRAY = (200, 200, 200)
        self.WHITE = (255, 255, 255)

        # === UI图标资源 ===
        self.music_image_transformed = None
        self.database_adapt_transformed = None
        self.net_work_adapt_transformed = None
        self.eye_transformed = None
        self.ai_info_send_transformed = None
        self.ai_emtion_recog_transformed = None

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
        self.send_disable_flag = False
        self.send_button_clicked = False

        # === UI文本 ===
        self.text_surface = None
        self.text_rect = None
        self.character_name_text_rect = None
        self.character_name_text_surface = None

        # === UI布局和状态 ===
        self.WIDTH = 1024
        self.HEIGHT = 860
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
        self.time_period_now = None
        self.button_press_time = 0
        self.button_press_duration = 200

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
        self.model_system_support_ls = None
        self.vision_model_prompt = str()
        self.ai_emotion_recog_flag = False

        # === 角色状态相关 ===
        self.character_statu_dic = None
        self.character_name_text = None
        self.character_image_box = None
        self.character_image_path = None
        self.avatar = None
        self.agent = None
        self.relationship = None
        self.relationship_dict = None
        self.favorability_bonus_multiplier = None
        self.character_image_ls_ls = None
        self.character_expressions_flag_ls = ['0', '+', '!+', '!!+', '-', '!-', '!!-', '~', '!~', '!!~']
        self.image_transition_mode_index = 0

        # === 状态显示元素 ===
        self.trust_value_text_rect = None
        self.trust_value_text_surface = None
        self.favorability_text_rect = None
        self.favorability_text_surface = None
        self.relationship_text_rect = None
        self.relationship_text_surface = None
        self.change_btn_flag = bool()

        # === 对话和输入相关 ===
        self.conversation_history = None
        self.conversation_history_original_length = None
        self.standard_conversation_history = None
        self.prompt = None
        self.prompt_index = None
        self.user_text = None
        self.filtered_index_ls = None
        self.position_x = None
        self.single_line_max_num = None
        self.max_lines = None
        self.ai_info_flag = True

        # === 调度和时间相关 ===
        self.schedule_dic = None
        self.daily_schedule_dic = None
        self.event_list = None
        self.time_check_point = 0

        # === 系统标志位 ===
        self.refresh_status_flag = bool()
        self.refresh_dialogue_flag = False
        self.data_base_able_flag = False
        self.net_work_able_flag = False
        self.music_stop_flag = False
        self.menu_able_flag = False
        self.ui_visible_flag = True
        self.eye_btn_hover_flag = False
        self.microphone_able_flag = bool()

        # === 文件和路径 ===
        self.upload_file_content = str()

        # === 配置和设置 ===
        self.transformed_ls = list()
        self.transformed_names_ls = list()
        self.button_variables_ls = list()
        self.setting_ls = [0, 0, 0, 0, 0, 0]
        self.current_select_speech_gen_model_index = -1
        self.selected_option_index = -1
        self.sound_text = str()

        # === 数据和存储 ===
        self.qa_db = None
        self.paragraph_rag_db = None
        self.fragmented_rag_db = None
        self.memory_rag_db = None
        self.memory_graph_rag_db = None
        self.latest_saving = None
        self.music_player = None

        # === 语音合成音色相关 ===
        self.recho_role_key = None
        self.fish_role_key = None
        self.role_key_ls = None

        # === 环境设置 ===
        os.environ["SDL_IME_SHOW_UI"] = "1"

        pygame.init()

        # 设置窗口尺寸
        title_icon_surface = pygame.image.load('imgs/icon.png')
        pygame.display.set_icon(title_icon_surface)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.NOFRAME)
        pygame.display.set_caption("AI伙伴")

        # 获取UI列表文字
        self.ui_txt_dic = read_json('ui_variable_data/ui_txt.json')

        # 设定字体
        self.status_bar_font = pygame.font.SysFont('SimHei', 20)
        self.label_font = pygame.font.SysFont('SimHei', 24)
        self.character_name_font = pygame.font.SysFont('SimHei', 32)
        self.send_button_font = pygame.font.SysFont('SimHei', 32)
        self.character_name_font.set_italic(True)

        self.role_cards_path = 'role_cards/樱井惠/'
        # 获取时间段
        self.time_period_now = get_current_time_period()['description'][0]
        print(self.time_period_now)
        self.role_init()
        self.game_init()

    def game_init(self):

        # 加载时钟
        self.clock_widget = CLOCK(825, 79, 'imgs/icon/clock.png')

        """ 加载图像资源 """
        icon_path = "imgs/icon"
        icons = read_json('ui_variable_data/icon_variable.json')

        for key, value in icons.items():
            setattr(self, key, pygame.image.load(f"{icon_path}/{value}"))

        # 初始化音频
        pygame.mixer.init()

        # 初始化背景音乐
        bgm_list = [fr'bgm\{music}' for music in os.listdir('bgm') if music.endswith('.mp3')]

        # 导入视觉任务提示词字典
        self.vision_mode = read_json('vision_mode/vision_mode.json')["vision_dict"]

        # 初始化下拉框
        self.model_list = self.ui_txt_dic["model_list"]  # 定义大语言模型列表
        self.model_system_support_ls = self.ui_txt_dic["model_system_support_ls"]  # 定义大语言模型对于system角色的支持性列表
        self.speech_gen_model_list = self.ui_txt_dic["speech_gen_model_list"]
        self.setting_menu = ScreenBoard(400, 580, text_dic=self.ui_txt_dic, x=312, y=140)  # 基活菜单

        # 文本输入框设置
        self.input_box = ScrollableTextBox(73, 789, 762, 45, (255, 255, 255), self.label_font)

        # 设定人物状态栏
        self.create_status()

        self.refresh_status()

        self.status_bar_rect = self.status_bar.get_rect(center=(222, 99))
        # 创建半透明图片
        self.image_size = (879, 283)
        self.position_x = self.image_size[0] // 2  # 计算对话框的中线x轴值
        self.image = pygame.Surface(self.image_size, pygame.SRCALPHA)
        self.single_line_max_num = int(self.image.get_width() / 24)  # 计算单行最大字符数
        self.max_lines = int(self.image.get_height() / 32) - 2  # 计算最多行数
        self.image.fill((100, 100, 100, 128))  # 灰色，半透明

        self.draw_character_name()  # 绘制人物名字

        # 生成button控件
        buttons = read_json('ui_variable_data/button_variable.json')
        for key, value in buttons.items():
            setattr(self, key, pygame.Rect(value[0], value[1], value[2], value[3]))

        # 场景选择按钮
        self.room_select_box = OptionBox(
            72, 430, 160, 50, (150, 150, 150), (100, 200, 255), pygame.font.SysFont('simhei', 30),
            self.room_name_ls)

        # 生成按钮transformed
        self.transformed_names_ls = read_json('ui_variable_data/transformed.json')
        icon_variables_ls = [vars(self)[key] for key in list(icons.keys())[8:]]
        self.button_variables_ls = [vars(self)[key] for key in list(buttons.keys())[1:]]

        for t_name, icon, button in zip(self.transformed_names_ls, icon_variables_ls, self.button_variables_ls):
            setattr(self, t_name, pygame.transform.scale(icon, (button.width, button.height)))

        # 光标设置
        self.clock = pygame.time.Clock()

        # 初始化音乐播放器
        self.music_player = MusicPlayer(bgm_list)  # 替换为你的音乐文件路径
        self.music_player.start()  # 启动播放音乐
        play_sound_async(self.role_cards_path)  # 播放欢迎语句

    def create_status(self):
        self.img_size = (300, 128)
        self.status_bar = pygame.Surface(self.img_size, pygame.SRCALPHA)
        self.status_bar.fill((100, 100, 100, 128))  # 灰色，半透明
        self.status_bar.blit(self.avatar, (0, 0))

    def draw_character_name(self):
        name_label_text = f'〖{self.character_name_text}〗:'
        self.character_name_text_surface = self.character_name_font.render(name_label_text, True, (255, 255, 255))
        self.character_name_text_rect = self.character_name_text_surface.get_rect(
            center=(24 * (len(name_label_text) / 2) + 6,
                    25))
        self.text_surface = self.label_font.render(f'『{self.llm_response_text}』', True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(self.image_size[0] // 2, self.image_size[1] // 2))
        # 将文字绘制到图片上
        self.image.blit(self.text_surface, self.text_rect)
        self.image.blit(self.character_name_text_surface, self.character_name_text_rect)

    def role_init(self):
        # 导入背景图设置
        bg_dic = read_json(f'{self.role_cards_path}bg_v1/bg_name_ls.json')
        self.room_name_ls = bg_dic["bg_name_ls"]
        self.room_ls = bg_dic["bg_ls"]
        self.background = pygame.image.load(f'{self.role_cards_path}bg_v1/{self.room_ls[0]}/'
                                            f'{self.time_period_now}.png')

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
        self.init_db()  # 初始化知识库
        # 读入日程字典
        self.daily_schedule_dic = read_json(f'{self.role_cards_path}actions.json')
        # 初始化对话历史
        self.conversation_history = list()
        # 设定用户回复
        self.user_text = ''
        # 加载人物状态机
        portrait_path = f'{self.role_cards_path}portrait'

        self.init_character_statu_dic(portrait_path)
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
            self.llm_response_text_analysis_flag = True
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
        if 'token_num.json' in os.listdir(self.role_cards_path) and self.latest_saving:
            # print(1)
            self.token_num = read_json(f'{self.role_cards_path}token_num.json')["token_num"]
            self.token_num += single_line_token_calculate(schedule_string)
        else:
            self.token_num = history_token_calculate(self.conversation_history)
        if self.llm_response_text:
            self.response_text_length = len(self.llm_response_text)
            self.refresh_dialogue_flag = True
        # 定义人物关系字典
        self.relationship_dict = {int(key): value for key, value in self.ui_txt_dic["relationship_dic"].items()}
        if self.latest_saving:
            self.agent.relationship_index = self.latest_saving["relationship_index"]
            self.agent.favorability = self.latest_saving["favorability"]
            self.agent.trust_value = self.latest_saving['trust_value']
        else:
            self.agent.relationship_index = 0
            self.agent.favorability = 0
        self.relationship = self.relationship_dict[self.agent.relationship_index]

        # 设定人物立绘图片和信任度
        if not self.character_image_box:
            if self.latest_saving:
                self.character_image_path = self.latest_saving["character_img"]
                self.character_image_box = ImageTransitionBox(153, 15, self.character_image_path
                                                              , "", True)

            else:
                self.character_image_path = random.sample(self.character_statu_dic['0'], 1)[0]
                self.character_image_box = ImageTransitionBox(153, 15, self.character_image_path,
                                                              "", True)

        self.character_img_and_relationship_change()

        # 设定角色卡人物名字
        if not self.character_name_text:
            if self.latest_saving:
                self.character_name_text = self.latest_saving['name']
            else:
                self.character_name_text = '智能体'

    def init_db(self):
        # 载入向量化数据库
        qa_db_path = f'{self.role_cards_path}character_info/qa_info.json'
        self.qa_db = read_data(qa_db_path) if os.path.exists(qa_db_path) else None
        paragraph_rag_db_path = f'{self.role_cards_path}character_info/paragraph_rag.txt'
        self.paragraph_rag_db = KnowledgeBase(paragraph_rag_db_path, 1) \
            if os.path.exists(paragraph_rag_db_path) else None
        fragmented_rag_db_path = f'{self.role_cards_path}character_info/fragmented_rag.txt'
        self.fragmented_rag_db = KnowledgeBase(fragmented_rag_db_path, 0) \
            if os.path.exists(fragmented_rag_db_path) else None
        memory_json_path = f'{self.role_cards_path}memory_info/memory.json'
        self.memory_rag_db = KnowledgeBase(memory_json_path, 2) if os.path.exists(memory_json_path) else None
        self.memory_graph_rag_db = None

    def init_character_statu_dic(self, portrait_path):
        character_status_neutral_ls = [f'{portrait_path}/0/{file}' for file in os.listdir(f'{portrait_path}/0')]
        character_status_happy_ls = [f'{portrait_path}/+/{file}' for file in os.listdir(f'{portrait_path}/+')]
        character_status_very_happy_ls = [f'{portrait_path}/!+/{file}'
                                          for file in os.listdir(f'{portrait_path}/!+')]
        character_status_extremely_happy_ls = [f'{portrait_path}/!!+/{file}'
                                               for file in os.listdir(f'{portrait_path}/!!+')]
        character_status_angry_ls = [f'{portrait_path}/-/{file}' for file in os.listdir(f'{portrait_path}/-')]
        character_status_very_angry_ls = [f'{portrait_path}/!-/{file}' for file in os.listdir(f'{portrait_path}/!-')]
        character_status_extremely_angry_ls = [f'{portrait_path}/!!-/{file}'
                                               for file in os.listdir(f'{portrait_path}/!!-')]
        character_status_sad_ls = [f'{portrait_path}/~/{file}' for file in os.listdir(f'{portrait_path}/~')]
        character_status_very_sad_ls = [f'{portrait_path}/!~/{file}'
                                        for file in os.listdir(f'{portrait_path}/!~')]
        character_status_extremely_sad_ls = [f'{portrait_path}/!!~/{file}'
                                             for file in os.listdir(f'{portrait_path}/!!~')]
        self.character_image_ls_ls = [character_status_neutral_ls, character_status_happy_ls,
                                      character_status_very_happy_ls, character_status_extremely_happy_ls,
                                      character_status_angry_ls, character_status_very_angry_ls,
                                      character_status_extremely_angry_ls, character_status_sad_ls,
                                      character_status_very_sad_ls, character_status_extremely_sad_ls]
        self.character_statu_dic = {v: k for v, k in
                                    zip(self.character_expressions_flag_ls, self.character_image_ls_ls)}

    def switch_role(self):
        role_cards_path = FolderSelector().get_folder_path('role_cards')
        if role_cards_path and self.role_cards_path != role_cards_path:
            self.role_cards_path = role_cards_path
            self.latest_saving = None  # 清空此前角色存档
            self.character_image_box = None  # 清空过往角色立绘
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
            llm_response_ls = self.filter_recovery()  # 过滤大模型回复
            # 播放音频
            play_voice_async(self.llm_response_text_filtered,
                             model_name=self.speech_gen_model_list[self.current_select_speech_gen_model_index],
                             path=self.role_cards_path, text=self.sound_text,
                             role_key=self.role_key_ls[self.current_select_speech_gen_model_index])

            byte = llm_response_ls[0] # 获取ai反馈情感标识符
            if byte in self.character_statu_dic.keys():
                relationship_change_value_dic = {'0': 0, '+': random.uniform(0.1, 1),
                                                 '!+': random.uniform(1, 2), '!!+': random.uniform(2, 4),
                                                 '-': random.uniform(-10, -1),
                                                 '!-': random.uniform(-20, -10), '!!-': random.uniform(-40, -20)
                                                 }
                self.update_character_image(byte, self.image_transition_mode_index)  # 更新人物立绘

                if byte in relationship_change_value_dic:
                    self.update_relationship(byte, relationship_change_value_dic)  # 确定关系偏移量
                    prompt_refresh_flag = self.check_favorability_boundaries(prompt_refresh_flag)  # 检测关系索引
                self.relationship = self.relationship_dict[self.agent.relationship_index]  # 更新关系值
                print(self.relationship, self.agent.favorability)
                self.refresh_prompt(prompt_refresh_flag)  # 更新高级提示词
                self.llm_response_text_analysis_flag = False
                self.refresh_status_flag = True
            else:
                self.update_character_image('0', self.image_transition_mode_index)
                print(self.character_image_box)
                self.llm_response_text_analysis_flag = False

    def update_character_image(self, byte, index):
        previous_character_image_path = self.character_image_path
        self.character_image_check(byte, previous_character_image_path)  # 检查立绘有无重复,如果重复则重新随机
        if index == 0:
            self.character_image_box.init_setting(153, 15,
                                                  previous_character_image_path,
                                                  self.character_image_path,
                                                  True)
        else:
            image_path_ls = self.character_image_ls_ls[index_check(self.character_expressions_flag_ls.index(byte))]
            path_ls = self.character_image_box.refresh_settings(153, 15, previous_character_image_path,
                                                                self.character_image_path,
                                                                False, image_path_ls=image_path_ls,
                                                                auto_motion_flag=True,
                                                                motion_done_flag=True)
            self.character_image_path = path_ls[-1]

    def update_relationship(self, byte, relationship_change_value_dic):
        self.favorability_bonus_multiplier = len(byte) if byte in relationship_change_value_dic else 0
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

    def check_favorability_boundaries(self, prompt_refresh_flag):
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
        return prompt_refresh_flag

    def refresh_prompt(self, prompt_refresh_flag):
        if prompt_refresh_flag:
            prompt_format = read_txt(f'{self.role_cards_path}prompt/special_role_player_prompt_format.txt')
            new_prompt = prompt_format.format(relationship=self.relationship,
                                              favorability=self.agent.favorability,
                                              place='门厅')
            self.conversation_history[self.prompt_index]["content"] = new_prompt

    def filter_recovery(self):
        self.llm_response_text_filtered = self.llm_response_text  # 初始化过滤回复
        if self.ai_emotion_recog_flag:
            emotion_byte = self.character_expressions_flag_ls[call_ai_api(self.llm_response_text)['result']['class']]
            llm_response_ls = [emotion_byte, self.llm_response_text]
        else:
            llm_response_ls = self.llm_response_text.split(' ')
            if len(llm_response_ls) == 1:
                    llm_response_ls.insert(0, '0')

        self.llm_response_text_filtered = "".join(llm_response_ls[1:])  # 整合过滤后的回复
        self.llm_response_text_filtered = self.llm_response_text_filtered.replace('\n', '')  # 清除回车
        self.llm_response_text_filtered = clean_llm_response(self.llm_response_text_filtered)  # 清除动作神态描写
        print(f'过滤后的回复:{self.llm_response_text_filtered}')
        return llm_response_ls

    def character_image_check(self, byte, previous_character_image_path):
        while True:
            self.character_image_path = random.sample(self.character_statu_dic[byte], 1)[0]
            if previous_character_image_path != self.character_image_path:
                return

    def change_button_color(self, color):
        button_color = color
        pygame.draw.rect(self.screen, button_color, self.send_button)  # 绘制矩形
        pygame.draw.rect(self.screen, (0, 0, 0), self.send_button, 2)  # 绘制边框
        send_text = self.send_button_font.render('发送', True, self.BLACK)
        self.screen.blit(send_text, (self.send_button.x + 17, self.send_button.y + 10))

    def handle_events(self):
        self.event_list = pygame.event.get()
        for event in self.event_list:
            if event.type == pygame.QUIT:
                self.app_shut_down_func()
                return False

            # Hover 事件处理
            if event.type == pygame.MOUSEMOTION:
                self.eye_btn_hover_flag = True if self.UI_visible_button.collidepoint(event.pos) else False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.ui_visible_flag:
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

                    if self.modify_llm_response_button.collidepoint(event.pos):
                        self.modify_llm_response_button_clicked_func()

                    if self.llm_repeat_button.collidepoint(event.pos):
                        self.llm_repeat_button_clicked_func()

                    if self.llm_response_copy_button.collidepoint(event.pos):
                        if len(self.conversation_history) > self.conversation_history_original_length:
                            pyperclip.copy(self.conversation_history[-1]['content'])
                        else:
                            pyperclip.copy(self.conversation_history[-4]['content'])

                    if self.conversation_history_save_button.collidepoint(event.pos):
                        self.limit_context_length()

                    if self.speech_recognition_button.collidepoint(event.pos):
                        res_json = voice_recognition(model_flag=False)
                        if res_json:
                            self.input_box.text += res_json['result'][0]
                        elif res_json is None:
                            print('未识别出结果')
                        else:
                            self.microphone_able_flag = False

                    if self.database_adapt_button.collidepoint(event.pos):
                        self.data_base_able_flag = not self.data_base_able_flag
                        if self.data_base_able_flag:
                            print('数据库查询已开启')
                        else:
                            print('数据库查询已关闭')

                    if self.net_work_adapt_button.collidepoint(event.pos):
                        self.net_work_able_flag = not self.net_work_able_flag
                        if self.net_work_able_flag:
                            print('网络查询已开启')
                        else:
                            print('网络查询已关闭')

                    if self.image_upload_button.collidepoint(event.pos):
                        if self.setting_ls[4] == 0:
                            self.vision_model_prompt = self.user_text
                        else:
                            self.vision_model_prompt = self.vision_mode[str(self.setting_ls[4])]
                        self.upload_file_content = ImageUploader().get_image_path(model_prompt=self.vision_model_prompt)

                    if self.ai_info_send_flag_button.collidepoint(event.pos):
                        self.ai_info_flag = not self.ai_info_flag
                        print('智能体参数发送模式已变动')

                    if self.ai_emotion_recog_button.collidepoint(event.pos):
                        self.ai_emotion_recog_flag = not self.ai_emotion_recog_flag

                if self.send_button.collidepoint(event.pos):
                    self.user_text = self.input_box.text
                    if self.user_text:
                        if not self.send_disable_flag:
                            self.llm_process_flag = True
                            self.send_disable_flag = True
                    else:
                        print('没有输入任何内容')
                    self.send_button_clicked = True
                    self.button_press_time = pygame.time.get_ticks()

                if self.UI_visible_button.collidepoint(event.pos):
                    self.ui_visible_flag = not self.ui_visible_flag

            if event.type == pygame.KEYDOWN:
                # 获取所有按键状态
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LCTRL] and keys[pygame.K_v]:
                    current_content = pyperclip.paste()
                    self.input_box.text += current_content

                if event.key == pygame.K_RETURN:
                    self.user_text = self.input_box.text
                    if self.user_text:
                        if not self.send_disable_flag:
                            self.llm_process_flag = True
                            self.send_disable_flag = True
                    else:
                        print('没有输入任何内容')
                    self.send_button_clicked = True
                    self.button_press_time = pygame.time.get_ticks()
        return True

    def llm_repeat_button_clicked_func(self):
        if len(self.conversation_history) > self.conversation_history_original_length:
            if not self.send_disable_flag:
                self.conversation_history.pop(-1)
                self.llm_process_flag = True
                self.send_disable_flag = True
            self.send_button_clicked = True
            self.button_press_time = pygame.time.get_ticks()
        else:
            print('现在还不能使用该功能')

    def modify_llm_response_button_clicked_func(self):
        if len(self.conversation_history) > self.conversation_history_original_length:
            flag = False
        else:
            flag = True
        new_agent = TextInputter(self.conversation_history, flag, self.agent).get_changes()
        if new_agent:
            # 打印回复
            new_response = new_agent[1]
            if new_response != self.llm_response_text:
                self.llm_response_text = new_response
                self.refresh_dialogue_flag = True
                self.print_llm_response()
                if not flag:
                    self.conversation_history[-1]['content'] = new_response
                else:
                    self.conversation_history[-4]['content'] = new_response

            self.agent.relationship_index = new_agent[0]
            self.agent.favorability = new_agent[2]
            self.agent.trust_value = new_agent[3]
            if self.relationship_dict[self.agent.relationship_index] != self.relationship:
                self.relationship = self.relationship_dict[self.agent.relationship_index]
                self.refresh_prompt(True)
            self.refresh_status_flag = True

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
        if not self.llm_process_flag:
            return
        if self.token_num >= 64000:
            self.limit_context_length()

        ai_info, res = self._extreme_content_init() # 获取智能体状态和知识库查询结果

        send_content = self.send_info_to_llm(ai_status=ai_info, res=res)  # 装填用户回复

        self._llm_response_process(external_content=send_content)  # 大模型回复结果处理
        self._reset_system_flags()  # 重置部分系统标志位

    def _extreme_content_init(self):
        res = str()
        ai_info = creat_ai_info(self.relationship, self.agent.favorability, self.agent.trust_value) \
            if self.ai_info_flag else None  # 智能体参数信息生成
        if self.user_text and (self.user_text.endswith('??') or self.data_base_able_flag):
            res = self.db_search(self.setting_ls[2])

            if not res:
                if self.net_work_able_flag:
                    res = WebScarp().search_get(self.user_text)
                    if res is None:
                        res = "抱歉，暂未查询到结果"
                else:
                    res = "抱歉，暂未查询到结果"

        elif self.net_work_able_flag:
            res = self.web_search()
        elif self.upload_file_content:
            res = self.upload_file_content
            self.upload_file_content = None
        return ai_info, res

    def _llm_response_process(self, external_content):
        back_tuple = chat_with_model(self.conversation_history, model=self.selected_option_index)
        if back_tuple is None:
            tokens = 0
            self.llm_response_text = '0 ...' if not self.ai_emotion_recog_flag else '...'
        else:
            tokens = back_tuple[1]
            self.llm_response_text = back_tuple[0]
        if tokens == 0 or not tokens:
            self.token_num += single_line_token_calculate(self.user_text)  # 计算token
        else:
            self.token_num = tokens
        if not self.token_num_save_flag:
            self.token_num_save_flag = True
        if external_content:
            self.conversation_history[-1]["content"] = self.user_text
        self.response_text_length = len(self.llm_response_text)
        # 将助手的回复添加到对话历史
        self.conversation_history.append({"role": "assistant", "content": self.llm_response_text})
        if not tokens:
            self.token_num += single_line_token_calculate(self.llm_response_text)  # 计算token

    def _reset_system_flags(self):
        self.refresh_dialogue_flag = True
        self.llm_process_flag = False
        self.user_text = ''
        self.input_box.text = ''
        self.input_box.text_changed_flag = True
        self.send_disable_flag = False
        self.llm_response_text_analysis_flag = True

    def web_search(self):
        if '天气' in self.user_text:
            res = WebScarp().autonavi_weather_forecast()
        else:
            res = WebScarp().search_get(self.user_text)
        if res is None:
            res = "抱歉，暂未查询到结果"
        return res

    def db_search(self, db_index):
        res_ls = None
        if db_index == 0:
            res_ls = search_answer(self.user_text, self.qa_db)
        elif db_index == 1:
            res_ls = [item[0] for item in self.paragraph_rag_db.search(self.user_text)]
        elif db_index == 2:
            res_ls = [item[0] for item in self.fragmented_rag_db.search(self.user_text)]
        elif db_index == 3:
            res_ls = [item[0] for item in self.memory_rag_db.search(self.user_text)]
        else:
            pass

        res = "".join(res_ls) if res_ls else None
        return res

    def limit_context_length(self):  # 修剪上下文
        save_conversation_history(self.conversation_history,
                                  self.prompt_index, f'{self.role_cards_path}/memory_info/')
        if not self.memory_rag_db:
            memory_json_path = f'{self.role_cards_path}memory_info/memory.json'
            self.memory_rag_db = KnowledgeBase(memory_json_path, 2)
        self.standard_conversation_history = None  # 清空备份聊天记录
        self.conversation_history = self.conversation_history[self.prompt_index:]
        self.conversation_history_original_length = len(self.conversation_history)
        # print(self.conversation_history)
        self.prompt_index = 0
        self.token_num = history_token_calculate(self.conversation_history)

    def send_info_to_llm(self, ai_status, res):
        # 将用户输入添加到对话历史
        send_content = str()
        if all([not ai_status, not res]):
            send_content = self.user_text
        elif ai_status and res:
            external_content = f'{ai_status}\nDataBase Result:[{res}]'
            send_content = f'{self.user_text}\n{external_content}'
        elif ai_status and not res:
            send_content = f'{self.user_text}\n{ai_status}'
        elif not ai_status and res:
            send_content = f'{self.user_text}\nDataBase Result:[{res}]'
        self.conversation_history.append({"role": "user",
                                          "content": send_content})
        return send_content

    def update(self):

        self.clock_widget.update(self.event_list)  # 更新时钟

        self.character_img_and_relationship_change()
        current_time = pygame.time.get_ticks()

        self.character_image_box.update(self.event_list)  # 更新立绘切换盒

        if current_time - self.time_check_point >= 60000:  # 时间段检查
            self.time_period_now = get_current_time_period()['description'][0]
            self.time_check_point = current_time
            # print('一分钟过去了')

        current_setting_ls = self.setting_menu.update(self.event_list)
        if current_setting_ls is not None:
            if self.setting_ls != current_setting_ls:
                self.setting_ls = current_setting_ls.copy()
        current_select_model_index = self.setting_ls[0]  # 获取大模型选择结果
        current_select_speech_gen_model_index = self.setting_ls[1]  # 获取语言大模型选择结果
        self.image_transition_mode_index = self.setting_ls[5]  # 获取立绘动画模式结果
        if self.current_select_speech_gen_model_index != current_select_speech_gen_model_index:
            self.current_select_speech_gen_model_index = current_select_speech_gen_model_index
            print(f'已选择:{self.speech_gen_model_list[self.current_select_speech_gen_model_index]}')
        # 场景下拉框选择设定
        selected_room_index = self.room_select_box.update(self.event_list)
        if selected_room_index >= 0:
            self.background = pygame.image.load(f'{self.role_cards_path}bg_v1/'
                                                f'{self.room_ls[selected_room_index]}/{self.time_period_now}.png')

        self.music_image_transformed = self.get_scaled_icon(
            self.music_icon, self.music_disabled_icon, self.music_button, not self.music_stop_flag
        )

        self.database_adapt_transformed = self.get_scaled_icon(
            self.knowledge_base_icon, self.knowledge_base_disabled_icon, self.database_adapt_button,
            self.data_base_able_flag
        )

        self.net_work_adapt_transformed = self.get_scaled_icon(
            self.net_work_icon, self.net_work_disabled_icon, self.net_work_adapt_button, self.net_work_able_flag
        )

        self.eye_transformed = self.get_scaled_icon(
            self.eye_on_icon, self.eye_close_icon, self.UI_visible_button, self.ui_visible_flag
        )

        self.ai_info_send_transformed = self.get_scaled_icon(
            self.ai_info_send_abled_icon, self.ai_info_send_disabled_icon, self.ai_info_send_flag_button, self.ai_info_flag
        )

        self.ai_emtion_recog_transformed = self.get_scaled_icon(
            self.ai_emotion_recog_abled_icon, self.ai_emotion_recog_disabled_icon, self.ai_emotion_recog_button, self.ai_emotion_recog_flag
        )

        if current_select_model_index >= 0:
            if self.selected_option_index != current_select_model_index:
                self.selected_option_index = current_select_model_index
                print(f'已选择:{self.model_list[self.selected_option_index]}')
                system_role_flag = self.model_system_support_ls[self.selected_option_index]
                if not system_role_flag:
                    print('该模型不支持system角色')
                    self.standard_conversation_history = copy.deepcopy(self.conversation_history)  # 备份聊天记录
                    for dic in self.conversation_history:
                        if dic['role'] == 'system':
                            dic['role'] = 'user'

                elif system_role_flag:
                    print('该模型支持system角色')
                    if self.standard_conversation_history:
                        self.conversation_history = self.standard_conversation_history + \
                                                    self.conversation_history[len(self.standard_conversation_history):]
        if self.send_button_clicked:
            if current_time - self.button_press_time >= self.button_press_duration:
                self.change_btn_flag = True
                self.button_press_time = 0
                self.send_button_clicked = False

        self.input_box.handle_event(self.event_list)

    @staticmethod
    def get_scaled_icon(icon, disabled_icon, button, flag):
        """根据标志返回缩放后的图标"""
        return pygame.transform.scale(icon if flag else disabled_icon, (button.width, button.height))

    def draw(self):
        self.draw_ui()  # 绘制UI控件

        self.print_llm_response()  # 将大模型的回复打印到对话框上

        if self.menu_able_flag:
            self.setting_menu.draw()
            self.screen.blit(self.setting_menu.surface, (self.setting_menu.x, self.setting_menu.y))

        if self.ui_visible_flag:
            self.room_select_box.draw(self.screen)  # 绘制场景选择下拉框

        pygame.display.flip()

    def draw_ui(self):
        self.screen.fill((0, 0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.character_image_box.draw(self.screen)

        self.input_box.draw(self.screen)  # 绘制输入框

        self.transformed_ls = [vars(self)[key] for key in self.transformed_names_ls]

        if self.ui_visible_flag:
            [self.screen.blit(transformed, button) for transformed, button in
             zip(self.transformed_ls, self.button_variables_ls)]
        else:
            if self.eye_btn_hover_flag:
                self.screen.blit(self.eye_transformed, self.UI_visible_button)

        if self.refresh_status_flag:
            self.refresh_status()
            self.refresh_status_flag = False
        self.screen.blit(self.status_bar, self.status_bar_rect)

        # Determine the color based on the flags
        button_color = self.DARK_GRAY if self.send_disable_flag or self.change_btn_flag else self.GRAY

        # Change the button color
        self.change_button_color(button_color)

        # Reset the change_btn_flag if it was True
        if self.change_btn_flag:
            self.change_btn_flag = False

        if self.ui_visible_flag:
            self.clock_widget.draw(self.screen)  # 绘制时钟

    def print_llm_response(self):
        if self.refresh_dialogue_flag:
            # 在屏幕中央绘制半透明图片
            self.image.fill((100, 100, 100, 128))  # 灰色，半透明
            if self.response_text_length + 2 < self.single_line_max_num:
                if '\n' not in self.llm_response_text:
                    self.text_surface = self.label_font.render(f'『{self.llm_response_text}』', True, (255, 255, 255))
                    self.text_rect = self.text_surface.get_rect(
                        center=(self.position_x, self.image_size[1] // 2))
                    self.image.blit(self.text_surface, self.text_rect)
                else:
                    text_ls = TextLineFeed(f'『{self.llm_response_text}』').type_judge()
                    for index, text in enumerate(text_ls):
                        self.text_surface = self.label_font.render(text, True, (255, 255, 255))

                        self.text_rect = self.text_surface.get_rect(
                            center=(self.position_x, self.image_size[1] // 2 + index * 32))
                        self.image.blit(self.text_surface, self.text_rect)
            else:
                self.llm_response_text = f'『{self.llm_response_text}』'
                self.llm_response_text = self.llm_response_text.replace('\n', '')
                text_ls = [self.llm_response_text[i:i + self.single_line_max_num]
                           for i in range(0, self.response_text_length, self.single_line_max_num)]
                text_ls_length = len(text_ls)
                original_position_y = ((self.max_lines - text_ls_length) // 2 + 1) * 32 + 64
                for index, text in enumerate(text_ls):
                    self.text_surface = self.label_font.render(text, True, (255, 255, 255))

                    self.text_rect = self.text_surface.get_rect(
                        center=(self.position_x, original_position_y + index * 32))
                    self.image.blit(self.text_surface, self.text_rect)

            # 将文字绘制到图片上
            self.image.blit(self.character_name_text_surface, self.character_name_text_rect)
            self.refresh_dialogue_flag = False
        image_rect = self.image.get_rect(center=(512, 626))
        self.screen.blit(self.image, image_rect)

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
