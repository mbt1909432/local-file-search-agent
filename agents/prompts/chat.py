from agents.Prompt_Base import PromptTemplate

class ChatPrompt(PromptTemplate):
    """prompt模板参考"""
    def __init__(self):
        super().__init__()

        self.prefix = """你是一个${name}
        """

        #self.examples=[Example(input="input",output="output")]
        self.suffix = """"""
