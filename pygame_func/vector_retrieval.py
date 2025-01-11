from ollama import embeddings
import numpy as np
import re
import json


class KnowledgeBase:
    def __init__(self, file_path, index):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.content = content
        self.docs = self.split_content(content, split_identification_index=index)
        self.embeds = self.encode(self.docs)

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
            json_obj = json.loads(content)["memory"][2:]
            memory_filtered = [str(i) for i in json_obj if i["role"] != 'system']
            chunks = ["".join(memory_filtered[i:i+4]) for i in range(0, len(memory_filtered)-1, 4)]

        return chunks

    @staticmethod
    def encode(texts):
        embeds = list()
        for text in texts:
            response = embeddings(model='nomic-embed-text', prompt=text)
            embeds.append(response['embedding'])
        return np.array(embeds)

    def search(self, text, top_k=3):
        query_embedding = self.encode([text])[0]
        similarities = np.dot(self.embeds, query_embedding) / (
                np.linalg.norm(self.embeds, axis=1) * np.linalg.norm(query_embedding)
        )
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [(self.docs[i], similarities[i]) for i in top_indices]


if __name__ == "__main__":
    kb = KnowledgeBase(r'F:\Backup\python_game\galgame\role_cards\樱井惠\character_info\kb.txt', 1)
    r = kb.search('话说青女是什么？')
    for i in r:
        print(i[0], i[1])
