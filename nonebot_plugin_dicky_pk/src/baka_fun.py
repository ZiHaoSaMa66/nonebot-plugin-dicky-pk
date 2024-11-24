from pathlib import Path
import json
import random
import time

from .db import DB

# 可维护性较差致歉 
# 我是真懒得去写sql
# 摆烂了喵 json万岁()

class baka_json_db:
    def __init__(self):
        self.json_path = Path() / 'data' / 'chinchin_pk'
        self.json_path.mkdir(mode=0o777, exist_ok=True)
    
    def get_str_abs_path(self, filename) -> str:
        '''
        获取字符串类型的绝对路径
        - `filename`: 文件名
        '''
        return str(Path(self.json_path / filename))

    def read_db(self):
        
        p = self.get_str_abs_path('baka_db.json')
        
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        return data
    
    def write_db(self, data):
        '''
        写入数据库
        - `data`: 要写入的数据
        '''
        
        p = self.get_str_abs_path('baka_db.json')
        
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def get_user_info(self, data_name,qq_id):
        '''
        获取用户数据信息
        - `data_name`: 数据名称
        - `qq_id`: QQ号
        '''
        
        read_data = self.read_db()
        
        user_data = read_data.get(data_name)
        
        if user_data is None:
            return None
        
        user_info = user_data.get(str(qq_id))
        if user_info is None:
            return None
        
        return user_info
        

baka_db = baka_json_db()

# 文件示例结构(?)
# db_file_data_exp = {
#     "data_name":{
#         "qq_id":{
#             "last_time":0,
#         }
#     }
# }

# 一些配置
baka_config = {
    # 失败概率 [0,1]
    "an_tou_faild": 0.05,
    "an_tou_success_added_min_length": 0.3,
    "an_tou_success_added_max_length": 1.2,
    # 判定成功后加长度的范围
    "an_tou_success_tar_add_min_length": 0.05,
    "an_tou_success_tar_add_max_length": 0.5,
    # 被按头者判定成功后加长度的范围
    "an_tou_day_limit": 20,
}

def is_integer(number) -> bool:
    '''判断是否为整数'''
    if number - int(number) == 0:
        return True
    
    return False

def plus_user_length(qq_id,length):
    user_data = DB.load_data(qq_id)
    
    db_length = user_data.get("length")
    
    calc = db_length + length
    
    # 如果为整数 需要保留一位小数
    if is_integer(calc):
        calc = round(calc,1)
    
    user_data["length"] = calc
    
    DB.write_data(user_data)
    
    
def decide_roll_success(rate) -> bool:
    '''
    - 决定是否判定成功
    - `rate`: 失败概率 `[0,1]`
    '''
    import random
    rand_num = random.random()
    
    if rand_num < rate: # 失败
        return False
    # 成功
    return True


def an_head_suo_me_run(cmd_runner_qqid,target_qqid) -> str:
    '''按头suo我'''
    day_limit = baka_config.get("an_tou_day_limit")

    # 失败概率
    faild_rate = baka_config.get("an_tou_faild")
    
    succ_added_min_length = baka_config.get("an_tou_success_added_min_length")
    succ_added_max_length = baka_config.get("an_tou_success_added_max_length")
    
    tar_add_min_length = baka_config.get("an_tou_success_tar_add_min_length")
    tar_add_max_length = baka_config.get("an_tou_success_tar_add_max_length")
    
    random.seed(time.time())
    
    main_add_length = round(random.uniform(succ_added_min_length,succ_added_max_length),1)
    
    # 判定成功后加长度的范围
    tar_add_length = round(random.uniform(tar_add_min_length,tar_add_max_length),1)
    
    msg = ""
    
    if decide_roll_success(faild_rate):
        # 如果成功 加长度
        plus_user_length(cmd_runner_qqid,main_add_length)
        plus_user_length(target_qqid,tar_add_length)
        msg = f"按着头被suo的很舒服,长度增加了{main_add_length}cm,被按头者增加了{tar_add_length}cm"
    else:
        # suo爆炸了 扣长度
        plus_user_length(cmd_runner_qqid,float(-main_add_length))
        msg = f"对方技巧不行,被suo爆炸了,你的长度减少了{main_add_length}cm"
    
    return msg
    
    pass