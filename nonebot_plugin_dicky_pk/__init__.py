import asyncio
from pathlib import Path
import ujson as json
from nonebot import on_command
from nonebot.plugin import PluginMetadata
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageSegment,
    MessageEvent,
    GroupMessageEvent,
    GROUP_OWNER,
    GROUP_ADMIN,
)

from .src.main import KEYWORDS, message_processor as chinchin


usage: str = """

指令表:
    开启(关闭)牛子秘境
    牛子帮助
    启用(禁用)牛子pk
    牛子
    pk @用户
    🔒(suo/嗦/锁)我
    🔒(suo/嗦/锁) @用户
    打胶
    看他牛子(看看牛子) @用户
    注册牛子
    牛子排名(牛子排行)
    牛友(牛子好友/牛子朋友)
    关注牛子(添加牛友)
    取关牛子(删除牛友)
    牛子转生
    牛子成就
    牛子仙境
    牛子修炼(牛子练功/牛子修仙)
    
    牛子道具列表(牛子道具商店)
    牛子道具购买
    牛子道具使用 (序号) @某人

""".strip()

toy_shop = '''

序号 名称 价格 介绍
1 贞操🔒 30 一段时间内不能suo/打胶 , 施法者可以主动打开
2 猪腰子 10 +1cm总长度
3 羊腰子 20 +2cm总长度
4 大保健 30 一段时间内增加的长度x1.2,不可重复使用,可与其他道具叠加
5 肾宝 45 一段时间内增加的长度x1.5,不可重复使用,可与其他道具叠加
6 高科技海绵体修复乳液 60 立刻增加1cm + 3%总长度
7 精力液 50 立刻刷新冷却
8 cheems的戒色刀 80 -5%总长度
使用方法 牛子道具使用 (序号) @某人
没@就是对自己使用

'''.strip()

__plugin_meta__ = PluginMetadata(
    name="牛子PK",
    description="🥵",
    usage=usage,
    type="application",
    homepage="https://github.com/tkgs0/nonebot-plugin-dicky-pk",
    supported_adapters={"~onebot.v11"}
)


confpath = Path() / 'data' / 'chinchin_pk' / 'chinchin.json'
confpath.parent.mkdir(parents=True, exist_ok=True)

enablelist = (
    json.loads(confpath.read_text(encoding='utf-8'))
    if confpath.is_file()
    else {'all': False, 'group': []}
)


def save_conf():
    confpath.write_text(json.dumps(enablelist), encoding='utf-8')


def dicky_run(msg: str, bot: Bot, event: GroupMessageEvent , **keyword_args):

    def get_at_segment(qq: int):
        return f'{MessageSegment.at(qq)}'
    def send_message(qq: int, group: int, message: str):
        loop = asyncio.get_running_loop()
        loop.create_task(bot.send_group_msg(group_id=group, message=message))

    if not enablelist['all']:
        return
    if not event.group_id in enablelist['group']:
        return
    uid = event.user_id
    gid = event.group_id
    uids = [at.data['qq'] for at in event.get_message()['at']]
    at_id = int(uids[0]) if uids else None
    nickname = event.sender.card if event.sender.card else event.sender.nickname
    fuzzy_match = True
    chinchin(
        msg, uid, gid, at_id, nickname, fuzzy_match,
        get_at_segment, send_message , keyword_args=keyword_args
    )


get_chinchin = on_command(
    '牛子',
    priority=20,
    block=True
)

@get_chinchin.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    if not enablelist['all']:
        return
    if not event.group_id in enablelist['group']:
        return
    if (msg := arg.extract_plain_text()).startswith('帮助'):
        await get_chinchin.finish(usage)
    dicky_run('牛子'+msg, bot, event)
    return


@on_command(
    'pk',
    priority=15,
    block=True
).handle()
async def _(bot: Bot, event: GroupMessageEvent):
    dicky_run(KEYWORDS['pk'][0], bot, event)
    return


@on_command(
    '🔒我',
    aliases={"suo我", "嗦我", "锁我"},
    priority=15,
    block=True
).handle()
async def _(bot: Bot, event: GroupMessageEvent):
    dicky_run(KEYWORDS['lock_me'][0], bot, event)
    return


@on_command(
    '🔒',
    aliases={"suo", "嗦", "锁"},
    priority=15,
    block=True
).handle()
async def _(bot: Bot, event: GroupMessageEvent):
    dicky_run(KEYWORDS['lock'][0], bot, event)
    return


@on_command(
    '打胶',
    priority=15,
    block=True
).handle()
async def _(bot: Bot, event: GroupMessageEvent):
    dicky_run(KEYWORDS['glue'][0], bot, event)
    return


@on_command(
    '看他牛子',
    aliases={"看看牛子"},
    priority=15,
    block=True
).handle()
async def _(bot: Bot, event: GroupMessageEvent):
    dicky_run(KEYWORDS['see_chinchin'][0], bot, event)
    return


@on_command(
    '注册牛子',
    priority=15,
    block=True
).handle()
async def _(bot: Bot, event: GroupMessageEvent):
    dicky_run(KEYWORDS['sign_up'][0], bot, event)
    return


@on_command(
    '牛友',
    priority=15,
    block=True
).handle()
async def _(bot: Bot, event: GroupMessageEvent):
    dicky_run(KEYWORDS['friends'][0], bot, event)
    return


@on_command(
    '关注牛子',
    aliases={"添加牛友"},
    priority=15,
    block=True
).handle()
async def _(bot: Bot, event: GroupMessageEvent):
    dicky_run(KEYWORDS['friends_add'][0], bot, event)
    return


@on_command(
    '取关牛子',
    aliases={"删除牛友"},
    priority=15,
    block=True
).handle()
async def _(bot: Bot, event: GroupMessageEvent):
    dicky_run(KEYWORDS['friends_delete'][0], bot, event)
    return


def set_enable(gid: int, en: bool):
    if en:
        enablelist['group'].append(gid)
        list(set(enablelist['group']))
    else:
        enablelist['group'] = [uid for uid in enablelist['group'] if not uid == gid]
    save_conf()


enable_jjpk = on_command(
    '启用牛子pk',
    aliases={'开启牛子pk', '启用dicky-pk', '开启dicky-pk'},
    permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER,
    priority=5,
    block=True
)

@enable_jjpk.handle()
async def _(event: GroupMessageEvent):
    if not enablelist['all']:
        return
    set_enable(event.group_id, True)
    await enable_jjpk.finish('已启用群聊小游戏: Dicky-PK')


disable_jjpk = on_command(
    '禁用牛子pk',
    aliases={'关闭牛子pk', '禁用dicky-pk', '关闭dicky-pk'},
    permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER,
    priority=5,
    block=True
)

@disable_jjpk.handle()
async def _(event: GroupMessageEvent):
    if not enablelist['all']:
        return
    set_enable(event.group_id, False)
    await disable_jjpk.finish('已禁用群聊小游戏: Dicky-PK')


chinchin_enable = on_command(
    '开启牛子秘境',
    permission=SUPERUSER,
    priority=2,
    block=True
)

@chinchin_enable.handle()
async def _(event: MessageEvent):
    msg = ''
    if isinstance(event, GroupMessageEvent):
        set_enable(event.group_id, True)
        msg += '\n已在本群启用牛子pk'
    enablelist['all']  = True
    save_conf()
    await chinchin_enable.finish('牛子秘境已开启.'+msg)


chinchin_disable = on_command(
    '关闭牛子秘境',
    permission=SUPERUSER,
    priority=2,
    block=True
)

@chinchin_disable.handle()
async def _():
    enablelist['group'].clear()
    enablelist['all']  = False
    save_conf()
    await chinchin_disable.finish('牛子秘境已关闭.')

chinchin_toy_shop = on_command(
    '牛子道具列表',
    aliases={'牛子道具商店'},
    priority=15,
    block=True
)

@chinchin_toy_shop.handle()
async def _():
    await chinchin_toy_shop.finish(toy_shop)


chinchin_buy_toy = on_command(
    '牛子道具',
    priority=15,
    block=True
)

@chinchin_buy_toy.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    if not enablelist['all']:
        return
    if not event.group_id in enablelist['group']:
        return
    if (msg := arg.extract_plain_text()).startswith('列表'):
        await chinchin_buy_toy.finish(toy_shop)
    elif msg.startswith('商店'):
        await chinchin_buy_toy.finish(toy_shop)
    
    dicky_run('牛子道具'+msg, bot, event, toy_option=msg)
    
    return


