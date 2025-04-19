# server_info.py
import requests
import discord

# サーバー情報を取得するURL（必要に応じて置き換えてください）
API_URL = 'https://api.scpslgame.com/serverinfo.php?id=serverId&key=APIkey'

async def get_server_info():
    try:
        response = requests.get(API_URL)
        data = response.json()

        if data.get('Success'):
            server = data['Servers'][0]
            players = server.get('Players', '0/30')
            ip = server.get('IP', '不明')
            return players, ip
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching server info: {e}")
        return None, None

async def create_server_embed(players, ip):
    if players != '不明':
        current_players, max_players = players.split('/')
        players_display = f"現在のプレイヤー数: {current_players}/{max_players}人"
    else:
        players_display = "プレイヤー数: 不明"

    embed = discord.Embed(
        title="SCPSL サーバー状態",
        description=players_display,
        color=discord.Color.blue()
    )
    embed.add_field(name="サーバー情報", value=f"ポート: 7777", inline=False)
    embed.add_field(name="IPアドレス", value=ip, inline=False)

    return embed
