import discord
import requests
import json
import asyncio
import aiohttp  # aiohttpをインポート

# Discordのボットトークンを設定
TOKEN = 'Token'

# サーバー情報を取得するURL
API_URL = 'https://api.scpslgame.com/serverinfo.php?id=serverId&key=APIkey'

# intentsの設定（ボットの基本設定）
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def get_server_info():
    try:
        response = requests.get(API_URL)
        data = response.json()

        if data.get('Success'):
            server = data['Servers'][0]
            players = server.get('Players', '0/30')  # 現在のプレイヤー数/最大人数を取得
            ip = server.get('IP', '不明')  # IPが返される場合
            return players, ip
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching server info: {e}")
        return None, None

async def send_embed_to_discord(players, ip):
    # プレイヤー数を「0/30」形式から編集する
    if players != '不明':
        current_players, max_players = players.split('/')  # 現在のプレイヤー数と最大プレイヤー数を分割
        players_display = f"現在のプレイヤー数: {current_players}/{max_players}人"
    else:
        players_display = "プレイヤー数: 不明"

    # Discordで送信する埋め込みメッセージ
    embed = discord.Embed(
        title="SCPSL サーバー状態",
        description=players_display,
        color=discord.Color.blue()
    )
    embed.add_field(name="サーバー情報", value=f"ポート: 7777", inline=False)
    embed.add_field(name="IPアドレス", value=ip, inline=False)

    webhook_url = "webhookId"

    # aiohttpでWebhookにPOSTリクエストを送信
    async with aiohttp.ClientSession() as session:
        payload = {'embeds': [embed.to_dict()]}
        async with session.post(webhook_url, json=payload) as response:
            if response.status == 204:
                print("メッセージを送信しました！")
            else:
                print(f"送信エラー: {response.status}")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    
    # サーバー情報を取得
    players, ip = await get_server_info()

    if players and ip:
        await send_embed_to_discord(players, ip)

    await asyncio.sleep(60)  # 60秒ごとに更新

# ボットの実行
client.run(TOKEN)
