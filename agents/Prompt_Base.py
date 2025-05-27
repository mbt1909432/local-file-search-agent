from typing import Dict, Any, Optional, List
from string import Template

from pydantic import BaseModel, Field
from  enum import Enum


class PromptType(Enum):
    PREFIX = "PREFIX"
    EXAMPLE = "EXAMPLE"
    SUFFIX = "SUFFIX"
    USER = "USER"



class Example(BaseModel):
    input: str = Field(..., description="示例输入")
    output: str = Field(..., description="示例输出")



class PromptTemplate:
    """提示模板基类"""
    
    def __init__(self):
        """初始化提示模板"""
        self.prefix = ""
        self.examples: List[Example] = []
        self.suffix = ""
        self.user=""#特别用于react
        
    def set_examples_str(self) -> str:

        if not self.examples:
            return ""
            
        examples_str = "\n\nExamples:\n"
        for i, example in enumerate(self.examples, 1):
            examples_str += f"Example {i}:\n"
            examples_str += f"Input:\n{example.input}\n"
            examples_str += f"Output:\n{example.output}\n\n"
        return examples_str

    def _format_prompt(self, prompt: str, prompt_type: PromptType, **kwargs) -> Optional[str]:

        return Template(prompt).substitute(**kwargs) #TODO:添加安全检测 若传参不完全


    def get_format_system_prompt(self, **kwargs) -> str:

        formatted_prefix = self._format_prompt(self.prefix, PromptType.PREFIX, **kwargs) or ""
        formatted_suffix = self._format_prompt(self.suffix, PromptType.SUFFIX, **kwargs) or ""
        examples_str = self.set_examples_str()
        result = formatted_prefix + examples_str + formatted_suffix

        if result is None:
            result=""

        return result

    def get_format_user_prompt(self, **kwargs) -> str:

        formatted_user = self._format_prompt(self.user, PromptType.USER, **kwargs) or ""

        return formatted_user




