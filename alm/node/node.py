class Node:
    def __init__(self, id, children: list, end: bool, word: str =None, notes: str =None):
        """ノード

        Args:
            id (Any): ノードのID
            children (list): 子ノードのリスト
            end(bool): 葉かどうか
            word (str, optional): 単語 Defaults to None.
            notes (list, optional): 音符のリスト Defaults to None.
        """
        self.id = id
        self.word = word
        self.end = end
        self.notes = notes
        self.children = children

    def to_dict(self) -> dict:
        """Nodeオブジェクトを辞書型配列にする

        Returns:
            dict: Nodeを辞書型配列に変換した結果
        """

        res = {"id": self.id, "end": self.end, "children": []}

        if self.word != None:
            res["word"] = self.word

        if self.notes != None:
            res["notes"] = self.notes

        for child in self.children:
            res["children"].append(child.to_dict())

        return res 