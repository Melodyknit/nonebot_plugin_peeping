from aiohttp import ClientSession
from asyncio import sleep
from json import loads
from typing import Union

xml = """
<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<msg serviceID="146" templateID="1" action="web" brief="暗中观察" sourceMsgId="0" url="https://jq.qq.com/?_wv=1027&k=WxWt4kW9" flag="0" adverSign="0" multiMsgFlag="0">
    <item layout="2" advertiser_id="0" aid="0">
        <picture cover="{url}" w="0" h="0" />
        <title>暗中观察</title>
        <summary>暗中观察</summary>
    </item>
    <source name="暗中观察" icon="" action="app" appid="-1" />
</msg>
"""
main_url = "http://melodyknit.club:8000/peeping"


class Peeping:
    def __init__(self, interval: int = 5):
        self._xml = xml
        self._session = ClientSession()
        self.uid = None
        self.interval = interval
        self.img_url = f"{main_url}/image?uid="

    async def _get(self, url, params=None) -> Union[dict, list]:
        async with self._session.get(url, params=params) as res:
            return loads(await res.read())

    async def __aenter__(self):
        self.uid = (await self._get(main_url))["uid"]
        self.img_url += str(self.uid)
        return self

    def get_xml(self) -> str:
        return self._xml.format(url=self.img_url)

    @staticmethod
    def _msg(info) -> str:
        return (f"时间：{info['time']}\n"
                f"IP：{info['host']}\n"
                f"所在地：{info['referer']}\n"
                f"设备：{info['ua']}")

    async def get_data(self) -> dict:
        await sleep(self.interval - 1)
        return await self._get(main_url, params={"uid": self.uid})

    async def get_send_msg(self) -> str:
        data = await self.get_data()
        if data:
            return "\n---\n".join([self._msg(info) for info in data])
        else:
            return "未发现"

    async def __aexit__(self, *ags):
        await self._session.close()
