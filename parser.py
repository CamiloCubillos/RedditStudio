class Parser:

    def __init__(self, raw_text: str):
        self.raw_text = raw_text
        self.story = ""
        self.autor = ""

    def parse(self):
        lines = self.raw_text.split("\n")
        self.autor = lines[0]
        self.story = "".join(lines[1:])
