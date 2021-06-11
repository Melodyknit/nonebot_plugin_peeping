from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.permission import SUPERUSER
from .data_source import Peeping

peeping = on_command("窥屏", permission=SUPERUSER, block=False, priority=1)


@peeping.handle()
async def peeping_handle(bot: Bot, event: GroupMessageEvent):
    async with Peeping() as p:
        await peeping.send(MessageSegment.xml(await p.get_xml()))
        await peeping.finish(await p.get_send_msg())
