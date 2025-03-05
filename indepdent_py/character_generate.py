import random

# 随机生成每个人格维度的分数
openness = random.randint(0, 100)
conscientiousness = random.randint(0, 100)
extraversion = random.randint(0, 100)
agreeableness = random.randint(0, 100)
neuroticism = random.randint(0, 100)


# 描述每个维度的具体特征
def describe_personality():
    descriptions = {
        '开放性（Openness）': openness,
        '尽责性（Conscientiousness）': conscientiousness,
        '外向性（Extraversion）': extraversion,
        '宜人性（Agreeableness）': agreeableness,
        '神经质（Neuroticism）': neuroticism
    }

    for trait, score in descriptions.items():
        if trait == '开放性（Openness）':
            if score <= 20:
                print(f"{trait}: 保守与传统，喜爱重复性任务，拒绝变革。")
            elif score <= 40:
                print(f"{trait}: 较少创新，稳定可靠，但不喜欢冒险。")
            elif score <= 60:
                print(f"{trait}: 适度开放，愿意接受新观点，但行动较谨慎。")
            elif score <= 80:
                print(f"{trait}: 创新思想，愿意尝试新事物，对新环境较易适应。")
            else:
                print(f"{trait}: 极具创造力，喜欢挑战常规并追求新体验。")

        elif trait == '尽责性（Conscientiousness）':
            if score <= 20:
                print(f"{trait}: 随意和无计划，易受干扰，常缺乏条理。")
            elif score <= 40:
                print(f"{trait}: 有时表现负责，但在冲突下容易分心。")
            elif score <= 60:
                print(f"{trait}: 通常有条理，能较好地管理时间。")
            elif score <= 80:
                print(f"{trait}: 高度负责，注重细节，极少拖延。")
            else:
                print(f"{trait}: 完美主义者，极其勤奋，有时过于苛求。")

        elif trait == '外向性（Extraversion）':
            if score <= 20:
                print(f"{trait}: 内向，喜欢独处，社交需求低。")
            elif score <= 40:
                print(f"{trait}: 中度内向，在小团体中表现舒适。")
            elif score <= 60:
                print(f"{trait}: 适度外向，社交自如但也享受安静时光。")
            elif score <= 80:
                print(f"{trait}: 外向活跃，喜欢人群，容易与人交流。")
            else:
                print(f"{trait}: 极具社交性和领导魅力，最适合公共场合。")

        elif trait == '宜人性（Agreeableness）':
            if score <= 20:
                print(f"{trait}: 冷漠，易冲突，常持批评态度。")
            elif score <= 40:
                print(f"{trait}: 有时急躁，偶尔友好，易妥协。")
            elif score <= 60:
                print(f"{trait}: 通常友善可靠，与人合作良好。")
            elif score <= 80:
                print(f"{trait}: 乐于助人，关心他人，富有同情心。")
            else:
                print(f"{trait}: 极为利他主义，利他过度有时忽略自我需求。")

        elif trait == '神经质（Neuroticism）':
            if score <= 20:
                print(f"{trait}: 情感稳定，极少感到焦虑或压力。")
            elif score <= 40:
                print(f"{trait}: 偶尔经历压力，有一定的应对策略。")
            elif score <= 60:
                print(f"{trait}: 情绪变化偶发，遇到挫折可能需要时间恢复。")
            elif score <= 80:
                print(f"{trait}: 常感到焦虑和压力，容易情绪化。")
            else:
                print(f"{trait}: 情绪极易波动，常常处于应激状态。")

            # 调用函数输出结果


describe_personality()