from PyQt5.QtWidgets import QPushButton, QLabel, QWidget,QApplication
from PyQt5 import uic,QtGui
from TextFactory import TextFactory
from Scrape import *
import sys
import os

"""适时清理TextFactory"""
"""自己断句，可自备文章"""
# 主界面
class MainUi:

    def __init__(self):
        self.ui = uic.loadUi('./ui/Main.ui')
        self.add_passage_btn = self.ui.pushButton_3
        self.start_writing_btn = self.ui.pushButton
        self.clear_passage_btn = self.ui.pushButton_2
        self.sub_btn = self.ui.pushButton_4
        self.container = self.ui.widget
        self.add_dir_passage()
        self.display_passage()
        self.set_btn()

    # 绑定按钮
    def set_btn(self):
        self.add_passage_btn.clicked.connect(self.add_btn_click)
        self.start_writing_btn.clicked.connect(self.writing_btn_click)
        self.clear_passage_btn.clicked.connect(self.clear_btn_click)
        self.sub_btn.clicked.connect(self.show_sub_click)

    #加入已存在文章
    def add_dir_passage(self):
        dir_passage_list = os.listdir('./Passages')
        for dir in dir_passage_list:
            with open(f'./Passages/{dir}','r',encoding='utf-8') as f:
                doc = f.read()
                doc = re.sub('\n','',doc)
                doc = re.split(r'[！？。]',doc)
                TextFactory.add_passage(doc)
        #将标题换为文件名
        TextFactory.title.clear()
        for dir in dir_passage_list:
            dir = re.sub(r'.txt','',dir)
            TextFactory.title.append(dir)
    # 展示已爬取文章列表
    def display_passage(self):
        font = QtGui.QFont()
        font.setFamily('方正正黑简体')
        font.setPointSize(20)
        for i, title in enumerate(TextFactory.title):
            one_title = QLabel(title, self.container)
            one_title.setFont(font)
            one_title.resize(1000,50)
            one_title.move(10, 50 * i)

    def add_btn_click(self):
        self.add_passage_page = AddPassageUi()
        self.add_passage_page.ui.show()
        self.ui.close()

    def writing_btn_click(self):
        self.input_title_page = InputTitle()
        self.input_title_page.ui.show()
        self.ui.close()

    def clear_btn_click(self):
        TextFactory.clear_passage()
        self.refresh = MainUi()
        self.refresh.ui.show()
        self.ui.close()

    def show_sub_click(self):
        self.subui = Chose_passage()
        self.subui.ui.show()
        self.ui.close()

#添加文章
class AddPassageUi():

    def __init__(self):
        self.ui = uic.loadUi('./ui/add_passage.ui')
        self.input = self.ui.lineEdit
        self.complete_btn = self.ui.pushButton_2
        self.cancel_btn = self.ui.pushButton
        self.set_btn()

    def set_btn(self):
        self.complete_btn.clicked.connect(self.complete_btn_click)
        self.cancel_btn.clicked.connect(self.cancel_btn_click)

    def complete_btn_click(self):
        scrape_page = ScrapeCertainPassage(self.input.text())
        passage = scrape_page.scrape()
        TextFactory.add_passage(passage)
        self.main_ui = MainUi()
        self.main_ui.ui.show()
        self.ui.close()

    def cancel_btn_click(self):
        self.main_ui = MainUi()
        self.main_ui.ui.show()
        self.ui.close()

#输入标题
class InputTitle():

    def __init__(self):
        self.ui = uic.loadUi('./ui/input_title.ui')
        self.input = self.ui.lineEdit
        self.complete_btn = self.ui.pushButton
        self.complete_btn.clicked.connect(self.start_writing)

    def start_writing(self):
        TextFactory.current_passage = ''
        TextFactory.current_title = self.input.text()
        TextFactory.write_in()
        self.writing_page = WritingPassagePage()
        self.writing_page.ui.show()
        self.ui.close()
#写作
class WritingPassagePage():

    def __init__(self):
        self.ui = uic.loadUi('./ui/writing.ui')
        self.cancel_btn = self.ui.pushButton_5
        self.text = self.ui.textBrowser
        self.text.setText(TextFactory.current_passage)
        self.all_sentences_btn = self.ui.pushButton_4
        self.front_sentences_btn = self.ui.pushButton_3
        self.middle_sentences_btn = self.ui.pushButton
        self.back_sentences_btn = self.ui.pushButton_2
        self.set_btn()

    def set_btn(self):
        self.cancel_btn.clicked.connect(self.cancel_btn_click)
        self.all_sentences_btn.clicked.connect(self.all_btn_click)
        self.front_sentences_btn.clicked.connect(self.front_btn_click)
        self.middle_sentences_btn.clicked.connect(self.middle_btn_click)
        self.back_sentences_btn.clicked.connect(self.back_btn_click)

    def cancel_btn_click(self):
        TextFactory.current_passage= '' #返回时清空当前进度
        TextFactory.current_title = ''
        self.main_ui = MainUi()
        self.main_ui.ui.show()
        self.ui.close()

    # 传入不同句子
    def all_btn_click(self):
        self.choose_page = ChooseSentences(TextFactory.all_passage)
        self.choose_page.ui.show()
        self.ui.close()

    def front_btn_click(self):
        self.choose_page = ChooseSentences(TextFactory.front_passage)
        self.choose_page.ui.show()
        self.ui.close()

    def middle_btn_click(self):
        self.choose_page = ChooseSentences(TextFactory.middle_passage)
        self.choose_page.ui.show()
        self.ui.close()

    def back_btn_click(self):
        self.choose_page = ChooseSentences(TextFactory.back_passage)
        self.choose_page.ui.show()
        self.ui.close()


# 展示传入的句子,并选择
class ChooseSentences(QWidget):

    def __init__(self, sentences):
        super().__init__()
        self.ui = uic.loadUi('./ui/choose_sentence.ui')
        self.sentences = sentences
        self.container = self.ui.widget
        self.cancel_btn = self.ui.pushButton
        self.cancel_btn.clicked.connect(self.cancel_btn_click)
        self.text = self.ui.textBrowser
        self.display_sentences()
        self.display_passage()

    def display_sentences(self):
        font = QtGui.QFont()
        font.setFamily('方正正黑简体')
        font.setPointSize(15)
        for i, text in enumerate(self.sentences):       #展示句子
            sentence = QPushButton(text, self.container)
            sentence.setFont(font)
            sentence.resize(3000, 50)
            sentence.move(10, 50 * i)
            sentence.clicked.connect(lambda: self.writing(self.sender().text()))

    def writing(self, sentence):
        TextFactory.current_passage += sentence
        TextFactory.current_passage +='。'  #分割时去掉了逗号
        TextFactory.write_in()
        self.display_passage()

    #更新展示
    def display_passage(self):
        self.text.setText(TextFactory.current_passage)

    def cancel_btn_click(self):
        self.writing_page = WritingPassagePage()
        self.writing_page.ui.show()
        self.ui.close()

class Sub_Repetition():

    def __init__(self,current_num=0):
        TextFactory.init_synonyms()
        self.ui = uic.loadUi('./ui/sub_rep.ui')
        self.current_num = current_num
        self.container = self.ui.widget
        self.list = TextFactory.all_words
        self.pre_btn = self.ui.pushButton_5
        self.next_btn = self.ui.pushButton_6
        self.pre_btn.clicked.connect(self.pre_word)
        self.next_btn.clicked.connect(self.next_word)
        font1 = QtGui.QFont()  # 正常展示字体
        font1.setFamily('方正正黑简体')
        font1.setPointSize(15)
        self.font1 = font1
        font2 = QtGui.QFont()  # 突出展示字体
        font2.setFamily('可口可乐在乎体 楷体')
        font2.setPointSize(20)
        font2.setUnderline(True)
        self.font2 = font2
        self.display(self.current_num)
        self.chose = self.ui.textBrowser # 可替换词展示框
        self.choice = '' #备选词
        self.choice = TextFactory.compare_word(self.current_num)
        self.chose.setText(self.choice)
        self.rep_btn = self.ui.pushButton_7 # 同义词替换按钮
        self.rep_btn.clicked.connect(self.change_word)
        self.input = self.ui.lineEdit  # 输入想替换的词
        self.input_btn = self.ui.pushButton  # 完成替换
        self.input_btn.clicked.connect(self.input_comple)
        self.comple = self.ui.pushButton_4 #  替换完成
        self.comple.clicked.connect(self.all_comple)


    def pre_word(self):

        pre_name = 'label' + str(self.current_num)
        pre = self.container.findChild(QLabel, pre_name);
        pre.setFont(self.font1)
        if(self.current_num >0):
            self.current_num -=1
        cur = self.container.findChild(QLabel, 'label' + str(self.current_num))
        cur.setFont(self.font2)
        self.choice = TextFactory.compare_word(self.current_num)
        self.chose.setText(self.choice)

    def next_word(self):
        pre_name = 'label'+str(self.current_num)
        pre = self.container.findChild(QLabel,pre_name);
        pre.setFont(self.font1)
        if (self.current_num < len(self.list)-1):
            self.current_num += 1
        cur = self.container.findChild(QLabel,'label'+str(self.current_num))
        cur.setFont(self.font2)
        self.choice = TextFactory.compare_word(self.current_num)
        self.chose.setText(self.choice)

    def change_word(self):
        if self.choice != '词库暂无近义词':
            TextFactory.all_words[self.current_num] = self.choice
            cur = self.container.findChild(QLabel, 'label' + str(self.current_num))
            cur.setText(self.choice)
            self.choice = TextFactory.compare_word(self.current_num)
            self.chose.setText(self.choice)

    def input_comple(self):

        input_word = self.input.text()
        TextFactory.all_words[self.current_num] = input_word
        cur = self.container.findChild(QLabel, 'label' + str(self.current_num))
        cur.setText(input_word)
        self.choice = TextFactory.compare_word(self.current_num)
        self.chose.setText(self.choice)

    def display(self,current_num):
        l = 1
        current_x = 0
        for i, text in enumerate(self.list): #展示句子
            name = 'label'+str(i)
            word = QLabel(text, self.container)
            word.setObjectName(name)
            word.resize(120,40)
            word.setFont(self.font1)
            if(i == current_num):
                word.setFont(self.font2)
            if(i%5 == 0):
                l = l+1
                current_x = 0

            word.move(current_x, 40 * l)
            current_x += 40*len(text)

    def all_comple(self):
        passage = ''
        for word in TextFactory.all_words:
            passage += word
        TextFactory.current_passage = passage
        TextFactory.write_in()
        self.main = MainUi()
        self.main.ui.show()
        self.ui.close()

class Chose_passage(QWidget):  # 选择文章降重

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui/choose_passage.ui')
        self.container = self.ui.widget
        self.display()

    def display(self):
        for i, text in enumerate(TextFactory.title):       #展示句子
            title = QPushButton(text, self.container)
            title.resize(1000, 50)
            font = QtGui.QFont()  # 正常展示字体
            font.setFamily('方正正黑简体')
            font.setPointSize(15)
            title.setFont(font)
            title.move(250, 50 * i)
            title.clicked.connect(lambda: self.set_passage(self.sender().text()))

    def set_passage(self,title):
        TextFactory.current_title = title
        with open(f'./Passages/{title}.txt','r',encoding='utf-8') as f:
            TextFactory.current_passage = f.read()
            TextFactory.split_pas()
        self.start()

    def start(self):
        self.start_sub = Sub_Repetition()
        self.start_sub.ui.show()
        self.ui.close()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_ui = MainUi()
    main_ui.ui.show()
    app.exec()

