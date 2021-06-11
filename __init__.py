from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.permission import SUPERUSER
from .data_source import Peeping

img = "http://melodyknit.club:8000/peeping/image?uid=1"
my_xml = """
<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
    <item layout="2" advertiser_id="0" aid="0">
        <picture cover="item" w="0" h="0" />
        <title>标题</title>
        <summary>描述</summary>
    </item><source name="QQ超级会员" icon="{url}" action="app" appid="-1" />
</msg>
"""

peeping = on_command("窥屏", permission=SUPERUSER, block=False, priority=1)


@peeping.handle()
async def peeping_handle(bot: Bot, event: GroupMessageEvent):
    async with Peeping() as p:
        await peeping.send(MessageSegment.xml(p.get_xml()))
        await peeping.finish(await p.get_send_msg())
