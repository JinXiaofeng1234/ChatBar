from ollama import embeddings
import numpy as np
import re
import os
from tqdm import tqdm
from ChatBar.prompt_reader import save_json, read_json


def expand_indices(indices, max_length):
    """
    扩展索引并处理边界问题

    参数:
    - indices: 原始索引列表
    - max_length: 总文本长度

    返回:
    - 扩展后的不重复索引列表
    """
    # 将每个索引向两边扩展1个单位
    expanded = set()
    for idx in indices:
        # 处理左边界
        left = max(0, idx - 1)
        # 处理右边界
        right = min(max_length - 1, idx + 1)

        # 添加扩展后的索引范围
        expanded.update(list(range(left, right + 1)))

    return sorted(list(expanded))


class KnowledgeBase:
    def __init__(self, file_path, index):
        self.index = index
        encode_flag = True
        path_ls = file_path.split('/')
        main_path = f'{"/".join(path_ls[:-1])}/{path_ls[-1].split(".")[0]}'
        cache_npy_file_path = f'{main_path}.npy'
        cache_json_file_path = f'{main_path}.json'

        if self.index == 2:
            cache_json_file_path = f'{main_path}_.json'

        if os.path.exists(cache_npy_file_path):
            encode_flag = False

        if encode_flag:
            content = file_path
            if self.index != 2:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                f.close()

            self.content = content
            self.docs = self.split_content(self.content, split_identification_index=self.index)

            docs_file_name = f'{path_ls[-1].split(".")[0]}'
            if self.index == 2:
                docs_file_name = f'{docs_file_name}_'

            save_json(self.docs, docs_file_name, f'{"/".join(path_ls[:-1])}/')

            self.embeds = self.encode(self.docs)
            np.save(cache_npy_file_path, self.embeds)

        else:
            self.docs = read_json(cache_json_file_path)
            self.embeds = np.load(cache_npy_file_path)
        self.docs_length = len(self.docs)

    @staticmethod
    def split_content(content, split_identification_index, max_length=256, ):
        chunks = []
        if split_identification_index == 0:  # 语义切割
            # 更完善的中文和英文标点符号处理
            pattern = r'([。！？…\.\!?]+[\'"』」》）\]\}]*)|\n{2,}'

            # 分割文本
            parts = re.split(pattern, content)
            sentences = []

            # 重新组合句子
            for i in range(0, len(parts) - 1, 2):
                if parts[i]:  # 处理正文部分
                    if i + 1 < len(parts) and parts[i + 1]:  # 有标点符号
                        sentences.append(parts[i] + parts[i + 1])
                    else:  # 没有标点符号
                        sentences.append(parts[i])

                        # 过滤空句子并去除首尾空白
            sentences = [s.strip() for s in sentences if s.strip()]

            current_chunk = []
            current_length = 0

            for sentence in sentences:
                sentence_length = len(sentence)

                # 处理超长句子
                if sentence_length > max_length:
                    # 如果当前chunk不为空，先保存
                    if current_chunk:
                        chunks.append(''.join(current_chunk))
                        current_chunk = []
                        current_length = 0

                    # 将超长句子按max_length切分
                    for i in range(0, sentence_length, max_length):
                        chunk = sentence[i:i + max_length]
                        chunks.append(chunk)
                    continue

                # 如果加入当前句子会超过max_length
                if current_length + sentence_length > max_length:
                    # 保存当前chunk
                    if current_chunk:
                        chunks.append(''.join(current_chunk))
                    current_chunk = [sentence]
                    current_length = sentence_length
                else:
                    current_chunk.append(sentence)
                    current_length += sentence_length

            # 处理最后剩余的chunk
            if current_chunk:
                chunks.append(''.join(current_chunk))

        elif split_identification_index == 1:  # 分段洛切片
            chunks = content.split('###')

        elif split_identification_index == 2:
            conversation_dic = read_json(content)
            memory_filtered = [i for i in conversation_dic if i["role"] != 'system']
            chunks = ["".join([f'{item["role"]}:{item["content"]}' for item in memory_filtered[i:i + 4]])
                      for i in range(0, len(memory_filtered) - 1, 4)]

        return chunks

    @staticmethod
    def encode(texts):
        embeds = list()
        for text in tqdm(texts):
            response = embeddings(model='bge-m3', prompt=text)
            embeds.append(response['embedding'])
        return np.array(embeds)

    def search(self, text, top_k=2):
        query_embedding = self.encode([text])[0]
        similarities = np.dot(self.embeds, query_embedding) / (
                np.linalg.norm(self.embeds, axis=1) * np.linalg.norm(query_embedding)
        )
        top_indices = [_property_index for _property_index in np.argsort(similarities)[::-1]
                       if similarities[_property_index] > 0.2]
        if top_k and top_indices and len(top_indices) > top_k:
            top_indices = top_indices[:top_k]

        if self.index != 1:
            top_indices = expand_indices(top_indices, self.docs_length)

        return [(self.docs[i], similarities[i]) for i in top_indices]


if __name__ == "__main__":
    kb = KnowledgeBase(r"F:/Backup/python_game/ChatBar/role_cards/樱井惠/character_info/test_kb2.txt", 0)
    while True:
        question = input('请输入问题:')
        if question == 'quit':
            break
        r = kb.search(question)
        for i in r:
            print(i[0], i[1])
