class TextLineFeed:
    def __init__(self, text):
        self.text = text

    def type_judge(self):
        if type(self.text) == str:
            split_ls = self.string_process()
        else:
            split_ls = self.ls_process()
        return split_ls

    def string_process(self):
        ls = [chunk for chunk in self.text.split('\n') if chunk]
        return ls

    def ls_process(self):
        new_ls = []
        for chunk in self.text:
            if '\n' in chunk:
                ls = [i for i in chunk.split('\n') if i]
            else:
                ls = [chunk]
            new_ls += ls
        return new_ls


if __name__ == "__main__":
    text_ls = TextLineFeed(["""+ 晚安，金晓锋。愿宁静与美好伴随你入梦。

我们明天再见吧。祝你""", '有个好梦。']).type_judge()
    print(text_ls)
