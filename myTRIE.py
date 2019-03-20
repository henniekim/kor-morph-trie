import collections

class Node:
    def __init__(self, label=None, data=None):
        self.label = label
        self.data = data
        self.children = collections.defaultdict(Trie)
        self.NodeCount = 0

    def add_child(self, key, data=None): # 부모 노드에 자식 노드를 추가하는 기능
        if not isinstance(key, Node):
            self.children[key] = Node(key, data)
        else :
            self.children[key.label] = key

    def __getitem__(self, key):
        return self.children[key]

    def __str__(self, depth=0): # TRIE 구조를 출력하는 기능
        s=[]
        for key in self.children:
            s.append('{}{} {}'.format(' ' * depth, key or '#', '\n'
                                      + self.children[key].__str__(depth + 1)))
        return ''.join(s)

class Trie :
    def __init__(self):
        self.head=Node()

    def __getitem__(self, key):
        return self.head.children[key]

    def __str__(self, depth=0):
        return self.head.__str__()

    def add(self, word, data):
        current_node = self.head
        word_finished = True

        for i in range(len(word)):
            if word[i] in current_node.children:
                current_node = current_node.children[word[i]]
            else:
                word_finished = False
                break

        if not word_finished:
            while i < len(word):

                if i == len(word)-1 :
                    current_node.add_child(word[i], data)
                else:
                    current_node.add_child(word[i])
                current_node.NodeCount += 1
                current_node = current_node.children[word[i]]
                i += 1

        current_node.add_child(None)
        current_node.NodeCount += 1
        current_node = current_node.children[None]
        current_node.data = data


    def has_word(self, word):
        if word == '':
            return False
        if word == None:
            raise ValueError("NULL 이 아닌 String 을 입력하세요")

        current_node = self.head
        exists = True
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]

            else:
                exists = False
                break
        if exists :
            if current_node.data == None:
                exists = False

        return exists

    def getData(self, word):
        if not self.has_word(word):
            #print("'{}'를 사전에서 찾을 수 없습니다.".format(word))
            return []

        current_node = self.head
        for letter in word:
            current_node = current_node[letter]

        return_data = current_node.data
        if return_data is None :
            return_data = []

        return return_data


