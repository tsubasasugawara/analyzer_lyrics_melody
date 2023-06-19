import spacy
from spacy import displacy
from ..utils import util

class GrammarParser:
    def __init__(self, nlp_model_name: str):
        """歌詞の文法構造を解析するクラス

        Args:
            nlp_model_name (str): 使用する自然言語処理モデル名
        
        Attribute:
            nlp (spacy.Language): モデルを読み込んだもの
        """

        self.nlp = spacy.load(nlp_model_name)

    def parse(self, lyrics: str) -> spacy.Language:
        """歌詞の文法構造を解析する

        Args:
            lyrics (str): 解析したい歌詞

        Returns:
            spacy.Language: 解析結果
        """

        return self.nlp(lyrics)
     
    def visualize(self, doc: spacy.Language) -> None:
        """歌詞の文法構造を可視化する

        Args:
            doc (spacy.Language): parse関数での解析結果
        """

        displacy.render(doc, style='dep', jupyter=True, options={"compact": True, "distance": 90})
    
    def get_words_list(self, doc: spacy.Language) -> list:
        """形態素解析によって分割された単語のリスト

        Args:
            doc (spacy.Language): _description_

        Returns:
            list: 単語のリスト
        """

        words_list = []
        for token in doc:
            words_list.append(token.text)

        return words_list
   
    def to_tree_map(self, doc: spacy.Language) -> dict:
        """構文解析木を辞書型にする

        Args:
            doc (spacy.Language): parse関数での解析結果

        Returns:
            dict: 構文解析木
        """

        tree_list = []
        for sent in doc.sents:
            tree_list.append(self.__recur_tree(sent.root))

        return self.__join_roots(tree_list)

    def __recur_tree(self, token) -> dict:
        """再帰的に木を作成する

        Args:
            token (_type_): 文法構造解析結果のトークン

        Returns:
            dict: ノード
        """

        node = {"word": token.text, "id": token.i, "children": {}}

        node["children"] = []
        for child in token.children:
            node["children"].append(self.__recur_tree(child))

        return node
    
    def __join_roots(self, roots: list) -> dict:
        """複数あるルートを一つにまとめる

        Args:
            roots (list): ルートのリスト

        Returns:
            dict: 結合後の木
        """

        if len(roots) == 1:
            return roots[0]
        elif len(roots) <= 0:
            return roots

        res = roots[0]
        for i in range(1, len(roots)):
            if len(res["children"]) > len(roots[i]["children"]):
                temp = roots[i]
                temp["children"].append(res)
                res = temp
            else:
                res["children"].append(roots[i])

        return res

    #TODO: 句読点を追加すると歌詞の木に追加されてしまい、対応する音符が無いためエラーになる可能性あり
    def add_punctuation(self, text: str) -> str:
        """句読点を追加

        Args:
            text (str): 句読点を追加したい文字列

        Returns:
            str: 句読点を追加した文字列
        """

        doc = self.nlp(text)

        res = ""
        pre_token = None

        for sent in doc.sents:
            for token in sent:
                
                if token.text != "\n":
                    res = res + token.text

                if pre_token == None:
                    pre_token = token
                    continue

                pre_morph = pre_token.morph.get("Inflection")

                if token.text == "\n" and pre_token.text != ("!" or "?" or "！" or "？"):
                    if (
                        (len(pre_morph) > 0 and util.contains(["連用形", "連体形"], pre_morph[0]))
                        or util.contains(["名詞", "間投詞", "副詞", "接続詞", "感嘆詞"], pre_token.tag_)
                        or ("助詞" in pre_token.tag_ and "終助詞" not in pre_token.tag_)
                        ):
                        res = res + "、"
                    else:
                        res = res + "。"

                pre_token = token

        return res
