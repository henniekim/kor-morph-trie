import numpy as np

# 문법 파일 불러오기
class Grammar :
    def __init__(self):
        self.contents = None
        self.filePath = 'grammar.txt'

    def load(self, filePath):
        try:
            self.contents = np.loadtxt(filePath, dtype='str', delimiter='\n', encoding='utf-8-sig')
            print("문법 정보를 불러왔습니다.")
            return self.contents

        # 파일 없을 때 예외 처리
        except:
            print("문법 정보가 없습니다.")

# 사전 파일 불러오기
class Dict :
    def __init__(self):

        self.contents = None
        self.numberOfContents = 0
        self.filePath = "dictionary_org.txt"

    def load(self, filePath):
        try:
            # 첫 문자에 ufeff가 붙는 현상 제거 : utf-8-sig로 해결
            self.contents = np.loadtxt(filePath, dtype='str', delimiter='   ', encoding='utf-8-sig')
            print("사전을 불러왔습니다. (utf-8 인코딩)")
            self.numberOfContents = len(self.contents)
            print("사전에 들어있는 단어 개수는 " + str(self.numberOfContents) + "개 입니다.")

        # 사전 파일 없을 때 예외 처리
        except:
            print("사전이 없습니다. ")
