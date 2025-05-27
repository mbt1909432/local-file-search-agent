from enum import Enum, auto
from tkinter import EXCEPTION
from typing import Callable, Union, Any

Observation = Union[str,EXCEPTION]

class NAME(Enum):

    COUNT_FILES = auto()
    FIND_FILES = auto()
    FIRE = auto()
    ICE = auto()

    def __str__(self):
        return self.name.lower()

def fire_skill(skill:str)->str:
    """
    火焰技能描述
    @param skill:
    @return:
    """
    return "火系魔法伤害3000，对冰系特工"

def ice_skill(skill:str)->str:
    """
    冰系技能描述
    @param skill:
    @return:
    """
    return "冰系魔法伤害23456，对草系特工"

class tool:

    def __init__(self,name:NAME,func: Callable[..., Any]):
        self.name=name
        self.func=func

    def tool_use(self,**kwargs)->Observation:

        try:
            return str(self.func(**kwargs))

        except Exception as e:
            return  str(e)

    def get_tool_info(self):
        return f"tool_name:{self.name.name.lower()}|tool_description:{self.func.__doc__}"

if __name__=="__main__":
    pass
    from local_seach_tools import  count_files
    tool_example=tool(NAME.COUNT_FILES,count_files)
    print(tool_example.get_tool_info())
    parameters={"path":"~/Documents","file_pattern":"*"}
    print(tool_example.tool_use())#count_files("~/Documents", file_pattern="*")







