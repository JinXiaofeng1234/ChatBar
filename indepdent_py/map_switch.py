import pygame
from prompt_reader import read_json

# 转换为可JSON序列化的格式
def convert_for_json(maps_dict):
    json_dict = {}
    for map_path, connections in maps_dict.items():
        json_connections = []
        for (rect, target) in connections:
            # 将Rect转换为列表[x, y, width, height]
            json_connections.append(([rect.x, rect.y, rect.width, rect.height], target))
        json_dict[map_path] = json_connections
    return json_dict

def switch_map(current_map_path, click_pos, maps_dict=None):
    """
    Pygame 地图切换函数 - 支持一张地图上的多个可点击区域

    参数:
        current_map_path (str): 当前背景图路径
        click_pos (tuple): 鼠标点击坐标，格式为 (x, y)
        maps_dict (dict, optional): 地图数据字典，如果为 None 则使用默认地图数据

    返回:
        str: 新背景图路径
    """
    # 如果未提供地图数据，使用默认配置
    if maps_dict is None:
        # 地图链条定义：每个地图有多个可点击区域
        # 使用 pygame.Rect 来定义区域
        return 0
    else:
        maps_dict = convert_for_json(maps_dict)

    # 检查当前地图是否在地图链条中
    if current_map_path not in maps_dict:
        return current_map_path

    # 获取当前地图的所有可点击区域
    clickable_areas = maps_dict[current_map_path]

    # 检查点击位置是否在任何可点击区域内
    for rect, target_map in clickable_areas:
        if rect.collidepoint(click_pos):
            return target_map

    # 如果点击位置不在任何可点击区域内，返回当前地图
    return current_map_path


# 示例：如何在 Pygame 游戏循环中使用此函数
def game_example():
    pygame.init()
    screen = pygame.display.set_mode((1024, 860))
    pygame.display.set_caption("地图切换示例")

    # 当前地图
    current_map_path = "maps/main_hall.png"
    current_map = pygame.image.load(current_map_path).convert()

    # 地图字典加载
    maps_cache = {}  # 缓存已加载的地图

    # 游戏主循环
    running = True
    maps = read_json('../role_cards/樱井惠/maps_dict.json')
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    # 获取点击位置并切换地图
                    new_map_path = switch_map(current_map_path, event.pos, maps_dict=maps)

                    # 如果地图变化，加载新地图
                    if new_map_path != current_map_path:
                        # 检查缓存中是否已有该地图
                        if new_map_path in maps_cache:
                            current_map = maps_cache[new_map_path]
                        else:
                            # 加载并缓存新地图
                            try:
                                current_map = pygame.image.load(new_map_path).convert()
                                maps_cache[new_map_path] = current_map
                            except pygame.error:
                                print(f"无法加载地图: {new_map_path}")
                                continue

                        current_map_path = new_map_path
                        print(f"切换到新地图: {current_map_path}")

                        # 绘制当前地图
        screen.blit(current_map, (0, 0))
        pygame.display.flip()

    pygame.quit()


# 如果是作为主模块运行，执行示例
if __name__ == "__main__":
    game_example()