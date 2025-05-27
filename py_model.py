
from pydantic import BaseModel, Field

class Message(BaseModel):
    #变量名:类型=Field
    role:str=Field(...,description="角色")
    content :str= Field(..., description="输出内容")
