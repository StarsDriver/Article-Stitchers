import jieba
import random
# 暂存文章
class TextFactory():

    title = []  #保存标题
    all_passage = []  #保存全部句子
    new_passage = '' #同义词替换后
    front_passage = []  #保存开头、过渡、结尾句
    middle_passage = []
    back_passage = []
    current_passage ='' #保存正在写的文章
    current_title = ''#保存当前标题
    SYNONYMS = []#放同义词
    all_words = []#文章分词

    def __init__(self):
        pass

    #读取同义词包
    @classmethod
    def init_synonyms(cls):
        with open('./Synonyms/SYNONYMS.txt','r',encoding='utf-8') as f:
            for line in f:
                temp = line.strip().split('-')
                cls.SYNONYMS.append(temp)


    @classmethod
    def add_passage(cls, new_passage):

        size = len(new_passage)
        cls.all_passage.extend(new_passage)
        cls.title.append(new_passage[0])
        for i in range(len(new_passage)):
            if i < size / 4:
                cls.front_passage.append(new_passage[i])
            if i >= size / 4 and i < size * 3 / 4:
                cls.middle_passage.append(new_passage[i])
            if i >= size * 3 / 4:
                cls.back_passage.append(new_passage[i])

    @classmethod
    def clear_passage(cls):
        cls.title.clear()
        cls.all_passage.clear()
        cls.front_passage.clear()
        cls.middle_passage.clear()
        cls.back_passage.clear()
        cls.current_passage = ''
        cls.current_title = ''

    @classmethod
    def write_in(cls):
        with open(f'./Passages/{cls.current_title}.txt','w',encoding='utf-8') as f:
            f.write(cls.current_passage)

    @classmethod
    def split_pas(cls):
        #将文章分词
        cls.all_words = list(jieba.cut(cls.current_passage))

    @classmethod
    def compare_word(cls,cur_num):
        """

        :param cur_num:
        :return: 近义词
        """
        new_word = ''
        has_found = False
        for synonyms_s in cls.SYNONYMS:  # 每一族近义词
            if has_found == False:  # 还没找到近义词
                for i, synonyms in enumerate(synonyms_s):
                    if cls.all_words[cur_num] == synonyms:
                        # if random.random() <0.3:
                        #    has_found = True
                        #   break
                        new_word = synonyms_s[i - 1]  # 有相同的词，从剩下的词中抽取
                        has_found = True
                        break
        if new_word =='':
            return '词库暂无近义词'
        else:
            return new_word

if __name__ =='__main__':
    text = '大一劳动教育报告1200字学校组织的社会实践和劳动实践，让我从中学到很多很多的东西，也得到了许多深刻的待人接物、为人处世的道理。我们学校把社会实践和劳动实践作为我们小学生走进社会进行实践的场所,让我们参与社会,在公益劳动的实践中有所启示。通过小组为单位的社区志愿服务,启发了我们在公益劳动中寻找能使我们受到教育,有所感悟的亮点,引导我们去了解社会、感受社会和认知社会。在敬老院中，我们小组的同学毫不嫌脏。耐心，仔细地帮助老人们洗.脚，剪指甲。这些都让我们体会到了老一辈的寂寞和孤独，同时又使我们感到自己的幸福和一些.自私、狭隘。我们在那里尽可能地多和老人聊天、谈心，竭尽所能使老人感到温暖。我们还帮助敬老院的职工一起打扫敬老院。虽然我们满头大汗，但我们很高兴，因为我们心里都有一股自豪感。而这种自豪感不是在学校里能够体会到的。公益劳动是不记报酬，不谋私利，不斤斤计较的;公益劳动是忘我的劳动，也是培养我们关心公共事业热情的。参加公益劳动的光荣感，塑造自己美好的心灵。这些都让我们觉得自己就是另一个雷锋，心里有一种说不出的愉快和自豪。处于这个时代的我们，大多都是独生子女，对待一些人际关系和自我评估的方面都有所欠缺。而这次的集体社会劳动和实践，使我体会到了集体的力量，集体的温暖和自己的不足。也让我亲身体会到了劳动的光荣和自豪。这些都是促进我努力改正自身错误，正确认识自己和评价自己新的思考。而现在，由于一切向钱看的思想的影响，在一些人的头脑中装满了金钱的利益，干什么事都讲钱，干活不讲报酬认为是傻瓜，甚至有的“社会公益劳动”也变相要钱。在这种情况下，学校有意识地组织了我们去参加力所能及的公益劳动，对于抵制一切向钱看的思想腐蚀可以起到一定的作用。这次的社会实践和劳动实践让我们亲身体会到了劳动的艰辛和劳动创造世界的真理，抵制了我们轻视劳动和不劳而获的思想的侵蚀，避免了我们形成好逸恶劳的坏习惯。公益劳动也同样加强了我们的劳动观念，帮助我们树立正确的人生观、价值观。社会实践和劳动同样培养了我们的竞争意识和开拓进取的精神。学校这次组织的社会实践和劳动，让我懂得了劳动不仅能造福社会，而且能陶冶情操，美化心灵。而我们也该为了公共利益而自觉自愿地参加劳动，因为，那是我们小学生的劳动态度的一个特征。不记报酬也是我们小学生劳动态度的一个特征。我们讲的公益劳动，就是以不记报酬为前提的;那是根据以公共利益而劳动;我们必须为公共利益而劳动，自觉要求进行劳动。积极参加公益劳动是为社会尽力，是热爱劳动的表现。社区劳动实践活动，提高了我们的社会实践能力。引导了我们接触，了解社会，增强我们的社会责任感和社会适应能力。而学校组织的劳动，更让我们明白了学会独立的重要性。在竞争如此激烈的今天，对于我们这些出生牛犊的小学生们，独立的培养和社会的洗礼是多么的重要。在这个更新速度超快的今天，如何适应社会也是我们即将面临的困难。对于现在的我们，越早接触这个日新月异的社会，就意味着我们越能适应.它。'
    print(text)
    TextFactory.current_passage = text
    TextFactory.init_synonyms()
    TextFactory.sub_repetition()


    #print(TextFactory.SYNONYMS)







