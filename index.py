import asyncio
import json
import websockets
import os
import time

os.system('clear' if os.name == 'posix' else 'cls')

time.sleep(1)

print("\nHangi seçeneği seçmek istiyorsunuz: ")

print("\n> 1 - Sesli Kanala Katıl ")

print("\n> 2 - Çıkış ")

askim = int(input("\nSeçiminiz: "))

if askim == 1:
    print("Lütfen token'larınızı Tokens.txt dosyasına eklediğinizden emin olun.")

    with open("tokens.txt", "r") as token_file:
        tokens = token_file.readlines()
        server_id = input("Sunucu ID'si: ")
        channel_id = input("Kanal ID'si: ")

    async def change_nick(token, guild_id):
        try:
            async with websockets.connect('wss://gateway.discord.gg/?v=9&encoding=json') as websocket:
                hello = await websocket.recv()
                hello_json = json.loads(hello)
                heartbeat_interval = hello_json['d']['heartbeat_interval']
                await websocket.send(json.dumps({"op": 2, "d": {"token": token.strip(), "properties": {"$os": "windows", "$browser": "Discord", "$device": "desktop"}}}))
                await asyncio.sleep(1)
                await websocket.send(json.dumps({"op": 3, "d": {"guild_id": guild_id, "nick": "Lefter"}}))
        except Exception as e:
            print(f"Hata oluştu: {e}")

    async def connect(token):
        while True:
            try:
                async with websockets.connect('wss://gateway.discord.gg/?v=9&encoding=json') as websocket:
                    hello = await websocket.recv()
                    hello_json = json.loads(hello)
                    heartbeat_interval = hello_json['d']['heartbeat_interval']
                    await websocket.send(json.dumps({"op": 2, "d": {"token": token.strip(), "properties": {"$os": "windows", "$browser": "Discord", "$device": "desktop"}}}))
                    await websocket.send(json.dumps({"op": 4, "d": {"guild_id": server_id, "channel_id": channel_id, "self_mute": True, "self_deaf": True}}))  
                    print(f"{token.strip()} joined")
                    await change_nick(token.strip(), server_id)
                    while True:
                        await asyncio.sleep(10)
                        try:
                            await websocket.send(json.dumps({"op": 1, "d": None}))
                        except websockets.exceptions.ConnectionClosed:
                            print(f"{token.strip()} bağlantısı kesildi, tekrar bağlanılıyor...")
                            break
            except Exception as e:
                print(f"Hata oluştu: {e}")

    async def main():
        tasks = []
        for token in tokens:
            task = asyncio.create_task(connect(token))
            tasks.append(task)
        await asyncio.gather(*tasks)

    asyncio.run(main())

elif askim == 2:
    print("Programdan çıkılıyor...")
else:
    print("Geçersiz bir seçim yaptınız. Lütfen tekrar deneyin.")
