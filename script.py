from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.sync import TelegramClient
from pyrogram import Client, filters
import random, asyncio, json

with open('setting.json', 'r', encoding = 'utf') as out:
    setting = json.load(out)

app = Client(
    'my_account',
    api_id = setting['account']['api_id'],
    api_hash = setting['account']['api_hash']
)

client = TelegramClient(
    setting['account']['username'], 
    setting['account']['api_id'],
    setting['account']['api_hash']
)
client.start()

@app.on_message(filters.command('invite', prefixes = '/') & filters.me)
async def invite_settings(_, message) -> None:
    if not setting['channel_to_invite']:
        channel = message.text.split('/invite ', maxsplit = 1)[1]
    else:
        channel = setting['channel_to_invite']
    
    members = await client.get_participants(message.chat.id)
    delete_message = await message.delete()
    chats = await client.get_dialogs()
    dialog = [cht for cht in chats if channel in cht.name][0]

    await client(
        InviteToChannelRequest(
            dialog, 
            [mem.id for mem in members]
        )
    )

if __name__ == "__main__":
    app.run()
