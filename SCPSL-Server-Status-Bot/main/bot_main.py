# bot_main.py
import discord
import asyncio
import aiohttp
from server_info import get_server_info, create_server_embed

# DiscordボットのトークンとWebhook URLを設定
TOKEN = 'Token'
WEBHOOK_URL = 'webhookId'

# DiscordのIntents設定
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def send_embed_to_discord(embed):
    async with aiohttp.ClientSession() as session:
        payload = {'embeds': [embed.to_dict()]}
        async with session.post(WEBHOOK_URL, json=payload) as response:
            if response.status == 204:
                print("メッセージを送信しました！")
            else:
                print(f"送信エラー: {response.status}")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    
    while True:
        players, ip = await get_server_info()

        if players and ip:
            embed = await create_server_embed(players, ip)
            await send_embed_to_discord(embed)
        else:
            print("サーバー情報を取得できませんでした。")

        await asyncio.sleep(60)  # 60秒ごとにループ

client.run(TOKEN)
