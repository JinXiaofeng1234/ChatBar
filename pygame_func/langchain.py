import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import logging
import jieba.analyse as analyse


class SimpleVectorStore:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.vectors = None
        self.texts = []
        self.original_texts = []

    def add_texts(self, texts):
        self.original_texts.extend(texts)
        tokenized_texts = [" ".join(jieba.lcut(text)) for text in texts]
        self.texts.extend(tokenized_texts)
        self.vectors = self.vectorizer.fit_transform(self.texts)

    def similarity_search(self, query, k=1):
        query_vector = self.vectorizer.transform([" ".join(jieba.lcut(query))])
        similarities = cosine_similarity(query_vector, self.vectors).flatten()
        top_k_indices = similarities.argsort()[-k:][::-1]
        top_k_similarities = similarities[top_k_indices]
        return [(self.original_texts[i], similarities[i]) for i in top_k_indices]


def read_data(json_file_path):
    vector_store = SimpleVectorStore()
    with open(json_file_path, encoding='utf-8') as user_file:
        file_contents = user_file.read()

    parsed_json = json.loads(file_contents)
    qa_pairs = parsed_json["QA_pairs"]
    vector_store.add_texts(qa_pairs)
    return vector_store


def search_answer(question, data_vector):
    result_ls = list()
    query = question
    results = data_vector.similarity_search(query, k=4)
    for item in results:
        if item[1] > 0:
            result_ls.append(item[0])

    return result_ls  # 返回最匹配的结果和其相似度


def history_token_calculate(dic_ls):
    token = 0
    for dic in dic_ls:
        token_num = len(jieba.lcut(dic["content"]))
        token += token_num
    return token


def single_line_token_calculate(content):
    token_num = len(jieba.lcut(content))
    return token_num


def search_key_word(text, top_k_num):
    keywords = analyse.tfidf(text, topK=top_k_num)
    return keywords


jieba.setLogLevel(logging.CRITICAL)

if __name__ == "__main__":
    data = read_data(r"F:\Backup\python_game\galgame\role_cards\樱井惠\character_info\qa_info.json")
    res_ls = search_answer('你喜欢参加什么活动', data)
    if res_ls:
        print("".join(res_ls))
