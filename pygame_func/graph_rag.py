class SimpleGraphRAG:
    def __init__(self):
        # 初始化简单知识图谱
        self.knowledge_graph = {
            # 实体: [(关系, 目标实体), ...]
            "苹果": [("CEO", "蒂姆·库克"), ("产品", "iPhone"), ("成立时间", 1976)],
            "蒂姆·库克": [("职位", "CEO"), ("公司", "苹果"), ("入职时间", 2011)],
            "iPhone": [("品牌", "苹果"), ("类型", "智能手机"), ("首发时间", 2007)]
        }

    def retrieve(self, query: str, max_hops=1):
        """检索过程"""
        # 1. 简单查询解析（实际应用需要NLP处理）
        keywords = query.lower().split()

        # 2. 知识图谱检索
        context = []
        visited = set()

        # 初始节点
        for keyword in keywords:
            if keyword in self.knowledge_graph:
                visited.add(keyword)
                context.extend([(keyword, rel, obj) for rel, obj in self.knowledge_graph[keyword]])

        # 扩展一度关系（可选）
        if max_hops > 0:
            for _, _, obj in context.copy():
                if obj in self.knowledge_graph and obj not in visited:
                    visited.add(obj)
                    context.extend([(obj, rel, o) for rel, o in self.knowledge_graph[obj]])

        return context

    def generate_response(self, context):
        """生成简单响应"""
        if not context:
            return "未找到相关信息"

        response = "找到以下相关信息：\n"
        for subj, rel, obj in context:
            response += f"- {subj} → {rel} → {obj}\n"
        return response


# 使用示例
if __name__ == "__main__":
    # 初始化系统
    graph_rag = SimpleGraphRAG()

    # 用户查询
    query = "苹果 CEO"

    # 检索过程
    context = graph_rag.retrieve(query)

    # 生成响应
    print(graph_rag.generate_response(context))