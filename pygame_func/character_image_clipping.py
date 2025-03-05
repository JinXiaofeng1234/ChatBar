import pygame


def crop_image(image_path, height):
    # 确保视频模式已设置
    # screen = pygame.display.set_mode((1, 1), pygame.HIDDEN)
    # 直接加载图片，不需要初始化 Pygame（假设调用方已经初始化）
    original_image = pygame.image.load(image_path).convert_alpha()

    # 剪裁高度（保留200像素）
    preserved_height = height

    # 创建剪裁后的Surface
    cropped_image = pygame.Surface((original_image.get_width(), preserved_height), pygame.SRCALPHA)
    cropped_image.blit(original_image, (0, 0), (0, 0, original_image.get_width(), preserved_height))

    # 关闭临时创建的屏幕
    # pygame.display.quit()

    return cropped_image


def save_cropped_image(surface, output_path):
    # 保存裁剪后的图片
    pygame.image.save(surface, output_path)


if __name__ == "__main__":
    pygame.init()
    save_cropped_image(crop_image('../role_cards/樱井惠/portrait/0/芳乃a_0_1860_1911.png', 864), 'test.png')
    pygame.quit()