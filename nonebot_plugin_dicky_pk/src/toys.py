from .db import DB
from .config import Config

# 尝试对原仓库内Issue建议进行修改
# 码力不足 尽力模仿原有插件写法

class ToysSystem:
    
    @staticmethod
    # 检查玩家是否被贞操锁硬控
    def check_user_is_hard_control(qq:int):
        pass
    
    @staticmethod
    def buy_toys(ctx:dict):
        '''购买玩具'''
        
        qq = ctx["qq"]
        group = ctx["group"]
        
        user_data = DB.load_data(qq)
        
        pass
    
    @staticmethod
    def use_toys(ctx:dict):
        '''使用玩具'''
        
        qq = ctx["qq"]
        group = ctx["group"]
        
        user_data = DB.load_data(qq)
        
        pass