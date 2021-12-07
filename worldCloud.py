import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def chinese_word_cloud():
    # 词云文本的路径
    path = "./Chinese.txt"

    # 打开文件读取
    with open(path, 'r', encoding="utf-8") as f:
        cut_text = f.read()
        pass

    # 打印读取结果
    # print(cut_text)

    # jieba 分词
    jieba_str = jieba.cut(cut_text)
    # print(jieba_str)
    cut_text = " ".join(jieba_str)
    # print(cut_text)

    # 配置词云图，并生成词云图
    word_cloud = WordCloud(
        # 注意字体设置（win 自带字体库，选择自己需要的字体即可）
        font_path="C:/Windows/Fonts/simfang.ttf",
        background_color="white",
        width=1920,
        height=1080
    ).generate(cut_text)

    # 显示词云图
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()

    # 保存词云图
    word_cloud.to_file("./chinese_word_cloud.png")
    pass


def main():
    chinese_word_cloud()
    pass


if __name__ == '__main__':
    main()
    pass