from duckduckgo_search import DDGS

# 配置代理
proxies = {
    "http://": "http://192.168.1.7:7892",  # 根据你的VPN端口修改
    "https://": "http://192.168.1.7:7892"
}

# 创建搜索实例，设置代理和更长的超时时间
ddgs = DDGS(proxies=proxies, timeout=20)

try:
    # 搜索新闻
    news = ddgs.news(
        keywords="中国",
        region="wt-wt",
        safesearch="off"
    )

    # 遍历结果
    for r in news:
        print(f"标题: {r['title']}")


except Exception as e:
    print(f"发生错误: {e}")