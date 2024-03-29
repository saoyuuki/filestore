#(©)CodeXBotz
import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT , SHORTENER_API as _shortener_api , SHORTENER_SITE as _shortener , HOW_TO_DOWNLOAD
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user , get_short
from urllib.parse import quote
from cloudscraper import create_scraper

async def short_url(longurl):
    cget = create_scraper().request
    res = cget('GET', f'https://{_shortener}/api?api={_shortener_api}&url={quote(longurl)}').json()
    shorted = res['shortenedUrl'] #.replace("files.technicalatg.com","atglinks.com")
    return shorted

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text)>7 and "short" not in text:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()
        cap_txt=f"⭐️ Your Files Include :- \n\n"
        for i , msg in enumerate(messages , start=1):
            if i > 10: 
                cap_txt += f'And More...\n'
                break
            try : caption = msg.caption.html 
            except: continue
            cap_txt += f'{i}. <code>{caption}</code>\n'
        cap_txt +="\n🌟 Powered By :- <a href='https://t.me/Binge_Pirates'>Binge Pirates</a>"
        if "#sample_video" not in messages[0].caption.lower():
            pin_ms = await message.reply_text(f'<b>{cap_txt.strip()}</b>' , quote=True , disable_web_page_preview=True ,reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('Send Again ↻',callback_data=f'resend {text.split(maxsplit=1)[1]}')]
            ]))
            await pin_ms.pin(both_sides=True)
        for msg in messages:
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
            except:
                pass
        if "#sample_video" not in messages[0].caption.lower():
            await client.send_message(message.chat.id , f'''<b>Thank You 🙏 For Using Our Channel To Download These Files.

    🌟 Powered By :- <a href='https://t.me/Binge_Pirates'>Binge Pirates</a></b>''', disable_web_page_preview=True ,reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('Channel  ⭧',url='https://telegram.me/Binge_Pirates')]
    ]))
            await client.send_sticker(message.chat.id , 'CAACAgUAAxkBAAEDjqZlH-D08AwLuMm5gxrHW06y4qolNgACJgADQ3PJEk-nRpVqAvN6HgQ')
        return
    elif "short" in text:
        text=text.split(maxsplit=1)[1][5:]
        result=await get_short(text)
        try:
            result=result[text]
        except:
            return
        temp_msg = await message.reply("Please wait...")
        shortened_link=await short_url(result)
        if not shortened_link:
            return
        try:
            base64_string = result.split("=",maxsplit=1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        try:
            messages = await get_messages(client, ids[:4])
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()
        txt=""
        ctr=1
        for msg in messages:
            if len(ids)>4 and ctr == 5:
                break
            txt += f"➤ <code>{msg.caption}</code>\n"
        if len(ids)>4:
            txt += f"➤ <code>And More</code>\n"
        await message.reply_text(f'''<b>Hey 👋 <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> , Your File(s) With Name(s)
        
{txt.strip()}

Is Ready To Be Sent , Open The Below Link With Help Of How To Download Link To Get Your File(s)</b>''',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("• Open Link •",url=shortened_link)],[InlineKeyboardButton("• How To Download •",url=HOW_TO_DOWNLOAD)]]))
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("😊 About Me", callback_data = "about"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
        )
        await message.reply_text(
            text = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            disable_web_page_preview = True,
            quote = True
        )
        return

    
#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##

    
    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(
                "Join Channel",
                url = client.invitelink)
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = 'Try Again',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
