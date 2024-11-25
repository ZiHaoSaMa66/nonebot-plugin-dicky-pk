from pathlib import Path
import json
import random
import time

import datetime

from .db import DB

# 可维护性较差致歉
# 我是真懒得去写sql
# 摆烂了喵 json万岁()


class baka_json_db:
    def __init__(self):
        self.json_path = Path() / "data" / "chinchin_pk"
        self.json_path.mkdir(mode=0o777, exist_ok=True)

    def get_str_abs_path(self, filename: str) -> str:
        """
        获取字符串类型的绝对路径
        - `filename`: 文件名
        """
        return str(Path(self.json_path / filename))

    def read_db(self):

        p = self.get_str_abs_path("baka_db.json")

        if not Path(p).exists():
            self.over_write_full_db({})
            return {}
            
    
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    def write_db(self, data: dict) -> None:
        """
        写入数据库
        - `data`: 要写入的数据
        """

        p = self.get_str_abs_path("baka_db.json")

        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def over_write_full_db(self, data: dict) -> None:
        self.write_db(data)

    # def write_user_info(self, data_name:str,qq_id:str|int, user_data:dict):
    #     '''
    #     写入用户数据信息
    #     - `data_name`: 数据名称
    #     - `qq_id`: QQ号
    #     - `user_data`: 用户数据
    #     '''

    #     read_data = self.read_db()

    #     if read_data.get(data_name) is None:
    #         read_data[data_name] = {}

    #     read_data[data_name][str(qq_id)] = user_data
    #     self.over_write_full_db(read_data)
    def write_user_data_key(self, data_name: str, qq_id: str | int, key: str, value):
        """
        写入用户数据信息
        - `data_name`: 数据名称
        - `qq_id`: QQ号
        - `key`: 键
        - `value`: 值
        """

        read_data = self.read_db()

        if read_data.get(data_name) is None:
            read_data[data_name] = {}

        if read_data[data_name].get(str(qq_id)) is None:
            read_data[data_name][str(qq_id)] = {}
            read_data[data_name][str(qq_id)][key] = value
        else:
            read_data[data_name][str(qq_id)][key] = value

        self.over_write_full_db(read_data)

    def get_user_data_key(
        self, data_name: str, qq_id: str | int, key: str
    ) -> None | str | int:
        """
        获取用户数据信息
        - `data_name`: 数据名称
        - `qq_id`: QQ号
        - `key`: 键
        """

        read_data = self.read_db()

        user_data = read_data.get(data_name)

        if user_data is None:
            return None

        user_info = user_data.get(str(qq_id))
        if user_info is None:
            return None

        return user_info.get(key)

    def get_user_info(self, data_name: str, qq_id: str | int) -> None | dict:
        """
        获取用户数据信息
        - `data_name`: 数据名称
        - `qq_id`: QQ号
        """

        read_data = self.read_db()

        user_data = read_data.get(data_name)

        if user_data is None:
            return None

        user_info = user_data.get(str(qq_id))
        if user_info is None:
            return None

        return user_info

    @staticmethod
    def get_a_time_str() -> str:
        """
        获取一个时间字符串
        """
        now_time = datetime.datetime.now()
        return now_time.strftime("%Y-%m-%d_%H:%M:%S")

    @staticmethod
    def compare_time_with_now_is_over_1_day(time_str: str) -> bool:
        """
        比较时间字符串是否超过一天
        - `time_str`: 时间字符串
        """
        now_time = datetime.datetime.now()
        time_obj = datetime.datetime.strptime(time_str, "%Y-%m-%d_%H:%M:%S")

        if (now_time - time_obj).days > 0:
            return True

        return False

    @staticmethod
    def compare_time_with_now_is_over_1_hour(time_str: str) -> bool:
        """
        比较时间字符串是否超过一小时
        - `time_str`: 时间字符串
        """
        now_time = datetime.datetime.now()
        time_obj = datetime.datetime.strptime(time_str, "%Y-%m-%d_%H:%M:%S")

        if (now_time - time_obj).seconds > 3600:
            return True

        return False


class an_tou_db:
    @staticmethod
    def check_is_in_cd(qq_id) -> bool:
        """
        - 检查是否在冷却时间内
        - `qq_id`: QQ号
        - 如果为`True` 则在冷却时间内 拒绝执行
        - 如果为`False` 则可以执行
        """

        def this_db_w(k, v):
            baka_db.write_user_data_key("hu_suo", qq_id, k, v)

        def this_db_r(k):
            return baka_db.get_user_data_key("hu_suo", qq_id, k)

        last_time = str(this_db_r("antou_last_time"))
        # 加str()是因为类型检查 好烦*

        dayily_suo_times = this_db_r("dayily_suo_times")


        if dayily_suo_times is None:
            # 如果无数据则初始化
            dayily_suo_times = 1
            this_db_w("dayily_suo_times", dayily_suo_times)
            this_db_w("antou_last_time", baka_db.get_a_time_str())

            return False
        
        if last_time and baka_db.compare_time_with_now_is_over_1_day(last_time):
            # 到了新的一天刷新次数限制
            this_db_w("dayily_suo_times", 1)
            this_db_w("antou_last_time", baka_db.get_a_time_str())
            return False

        if int(dayily_suo_times) >= baka_config["an_tou_day_limit"]:
            # 如果超过次数限制
            # 且且超过冷却时间
            if last_time and baka_db.compare_time_with_now_is_over_1_hour(last_time):
                # 冷却时间到了 允许执行

                _dayily_suo_times = dayily_suo_times + 1  # type: ignore

                this_db_w("dayily_suo_times", _dayily_suo_times)
                this_db_w("antou_last_time", baka_db.get_a_time_str())
                return False

            # 冷却时间未到 不能执行
            return True
        else:
            # 还没到次数限制 允许执行
            _dayily_suo_times = dayily_suo_times + 1  # type: ignore

            this_db_w("dayily_suo_times", _dayily_suo_times)
            this_db_w("antou_last_time", baka_db.get_a_time_str())
            
            return False

        print("debug > 所有分支均以经过是不是漏条件了?")
        return True


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
    "an_tou_faild": 0.1,
    "an_tou_success_added_min_length": 0.3,
    "an_tou_success_added_max_length": 1.2,
    # 判定成功后加长度的范围
    "an_tou_success_tar_add_min_length": 0.05,
    "an_tou_success_tar_add_max_length": 0.5,
    # 被按头者判定成功后加长度的范围
    "an_tou_day_limit": 12,
    # 每日限制次数 超过次数限制 则进入冷却时间
    
    "fix_zero_can_pk_min_pk_length": 10, # 修复长度为0的玩家可以pk的最小pk长度
    
}

def fix_zero_can_pk(qq_id) -> bool:
    """
    修复长度为0的玩家可以pk
    - `qq_id`: QQ号
    
    - 返回`True` 则可以pk
    - 返回`False` 则不可以pk
    
    """
    user_data = DB.load_data(qq_id)

    db_length = user_data.get("length") # type: ignore

    min_length = baka_config["fix_zero_can_pk_min_pk_length"]

    if db_length <= min_length:
        return False
    
    return True

def is_integer(number) -> bool:
    """判断是否为整数"""
    if number - int(number) == 0:
        return True

    return False


def plus_user_length(qq_id, length:float):
    '''
    追加用户长度
    - `qq_id`: QQ号
    - `length`: 长度(cm)
    '''
    
    user_data = DB.load_data(qq_id)

    db_length = user_data.get("length") # type: ignore

    calc = db_length + length # type: ignore

    # 如果为整数 需要保留一位小数
    if is_integer(calc):
        calc = round(calc, 1)

    user_data["length"] = calc # type: ignore

    DB.write_data(user_data) # type: ignore


def decide_roll_success(rate) -> bool:
    """
    - 决定是否判定成功
    - `rate`: 失败概率 `[0,1]`
    """
    import random

    rand_num = random.random()

    if rand_num < rate:  # 失败
        return False
    # 成功
    return True


# def roll_a_number(min_num, max_num) -> float:
#     '''
#     - 随机生成一个数字
#     (需要确保每次调用都不一样)
#     - `min_num`: 最小值
#     - `max_num`: 最大值
#     '''
    

def an_head_suo_me_run(cmd_runner_qqid, target_qqid) -> str:
    """按头suo我"""

    if an_tou_db.check_is_in_cd(cmd_runner_qqid):
        return "嘴都suo麻了！,休息一下吧"

    # 失败概率
    faild_rate = baka_config.get("an_tou_faild")

    succ_added_min_length = baka_config["an_tou_success_added_min_length"]
    succ_added_max_length = baka_config["an_tou_success_added_max_length"]

    tar_add_min_length = baka_config["an_tou_success_tar_add_min_length"]
    tar_add_max_length = baka_config["an_tou_success_tar_add_max_length"]

    random.seed(time.time())

    main_add_length = round(random.uniform(succ_added_min_length, succ_added_max_length), 1)

    # 判定成功后加长度的范围
    tar_add_length = round(random.uniform(tar_add_min_length, tar_add_max_length), 1)

    msg = ""

    if decide_roll_success(faild_rate):
        # 如果成功 加长度
        plus_user_length(cmd_runner_qqid, main_add_length)
        plus_user_length(target_qqid, tar_add_length)
        msg = f"两个人suo的很舒服,你的长度增加了{main_add_length}cm,对方长度增加了{tar_add_length}cm"
    else:
        # suo爆炸了 扣长度
        plus_user_length(cmd_runner_qqid, float(-main_add_length))
        plus_user_length(target_qqid, float(-main_add_length))
        msg = f"对方技巧不行,把你的牛牛suo爆炸了,你的长度减少了{main_add_length}cm,对方长度也减少了{tar_add_length}cm"

    return msg

