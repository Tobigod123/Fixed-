import datetime
import anitopy
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)
import os, time, asyncio, json
from bot.localisation import Localisation
from bot import (
  DOWNLOAD_LOCATION, 
  AUTH_USERS,
  LOG_CHANNEL,
  UPDATES_CHANNEL,
  SESSION_NAME,
  data,
  app, 
)

from bot.helper_funcs.ffmpeg import (
  convert_video,
  media_info,
  take_screen_shot,
  get_width_height
)

from bot.helper_funcs.display_progress import (
  progress_for_pyrogram,
  TimeFormatter,
  humanbytes
)

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

os.system("wget https://telegra.ph/file/1c74222f7f12c42573455.jpg -O thumb.jpg")

CURRENT_PROCESSES = {}
CHAT_FLOOD = {}
broadcast_ids = {}
bot = app        
async def incoming_start_message_f(bot, update):
    """/start command"""
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Localisation.START_TEXT,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Source Code 👻', url='https://t.me/Asimplekid')
                ]
            ]
        ),
        reply_to_message_id=update.id,
    )
    
async def incoming_compress_message_f(update):
  """/compress command"""
                                
  isAuto = True
  d_start = time.time()
  c_start = time.time()
  u_start = time.time()
  status = DOWNLOAD_LOCATION + "/status.json"
  sent_message = await bot.send_message(
  chat_id=update.chat.id,
  text=Localisation.DOWNLOAD_START,
  reply_to_message_id=update.id
              )
  chat_id = LOG_CHANNEL
  utc_now = datetime.datetime.utcnow()
  ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
  ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
  bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
  bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
  now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
  download_start = await bot.send_message(chat_id, f"**Bot Become Busy Now !!** \n\nDownload Started at `{now}`")
  try:
      d_start = time.time()
      status = DOWNLOAD_LOCATION + "/status.json"
      with open(status, 'w') as f:
        statusMsg = {
          'running': True,
          'message': sent_message.id
        }

        json.dump(statusMsg, f, indent=2)
      video = await bot.download_media(
        #message=update.reply_to_message,
        message=update,  
        #file_name=saved_file_path,
        progress=progress_for_pyrogram,
        progress_args=(
          bot,
          Localisation.DOWNLOAD_START,
          sent_message,
          d_start
        )
      )
      saved_file_path = video
      eni = saved_file_path.split("/")[-1]
      xnx = eni.split(".")[-1]
      opm = eni.replace(f".{xnx}", " .mkv")
      nam = opm.replace("_", " ")
      nam = opm.replace(".", " ")
      anitopy_options = {'allowed_delimiters': ' '}
      new_name = anitopy.parse(nam)
      anime_name = new_name['anime_title']
      episode_no = new_name['episode_number']  
      joined_string = joined_string = f"S1E{episode_no} - {anime_name} [480p][Dual][@Anime_Sensei_Network].mkv"
      if 'anime_season' in new_name.keys():
        animes_season = new_name['anime_season']
        joined_string = joined_string = f"S{animes_season}E{episode_no} - {anime_name} [480p][Dual][@Anime_Sensei_Network].mkv"


      LOGGER.info(saved_file_path)  
      LOGGER.info(video)
      if( video is None ):
        try:
          await sent_message.edit_text(
            text="Download Stopped 🛑"
          )
          chat_id = LOG_CHANNEL
          utc_now = datetime.datetime.utcnow()
          ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
          ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
          bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
          bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
          now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
          await bot.send_message(chat_id, f"**Download Stopped, Bot is Free Now !!** \n\nProcess Done at `{now}`")
          await download_start.delete()
        except:
          pass
       # delete_downloads()
        LOGGER.info("Download Stopped 🛑")
        return
  except (ValueError) as e:
      try:
        await sent_message.edit_text(
          text=str(e)
        )
      except:
          pass
      #delete_downloads()            
  try:
      await sent_message.edit_text(                
        text=Localisation.SAVED_RECVD_DOC_FILE                
      )
  except:
      pass     
    
  if os.path.exists(saved_file_path):
    downloaded_time = TimeFormatter((time.time() - d_start)*1000)
    duration, bitrate = await media_info(saved_file_path)
    if duration is None or bitrate is None:
      try:
        await sent_message.edit_text(                
          text="⚠️ Getting Video Metadata Failed ⚠️"                
        )
        chat_id = LOG_CHANNEL
        utc_now = datetime.datetime.utcnow()
        ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
        ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
        bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
        bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
        now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
        await bot.send_message(chat_id, f"**Download Failed, Bot is Free Now !!** \n\nProcess Done at `{now}`")
        await download_start.delete()
      except:
          pass          
      return
    thumb_image_path = await take_screen_shot(
      saved_file_path,
      os.path.dirname(os.path.abspath(saved_file_path)),
      (duration / 2)
    )
    if os.path.exists('/app/thumb.jpg'):
        thumbnailed = "thumb.jpg"
    else:
        thumbnailed = thumb_image_path
    width, height = get_width_height(saved_file_path)
    chat_id = LOG_CHANNEL
    utc_now = datetime.datetime.utcnow()
    ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
    ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
    bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
    bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
    now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
    await download_start.delete()
    compress_start = await bot.send_message(chat_id, f"**Compressing Video ...** \n\nProcess Started at `{now}`")
    await sent_message.edit_text(                    
      text=Localisation.COMPRESS_START                    
    )
    c_start = time.time()
    o = await convert_video(
           video, 
           DOWNLOAD_LOCATION, 
           duration, 
           bot, 
           sent_message, 
           compress_start
         )
    compressed_time = TimeFormatter((time.time() - c_start)*1000)
    LOGGER.info(o)
    if o == 'stopped':
      return
    if o is not None:
      chat_id = LOG_CHANNEL
      utc_now = datetime.datetime.utcnow()
      ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
      ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
      bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
      bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
      now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
      await compress_start.delete()
      upload_start = await bot.send_message(chat_id, f"**Uploading Video ...** \n\nProcess Started at `{now}`")
      await sent_message.edit_text(                    
        text=Localisation.UPLOAD_START,                    
      )
      u_start = time.time()
      caption = Localisation.COMPRESS_SUCCESS.replace('{}', downloaded_time, 1).replace('{}', compressed_time, 1)
      upload = await bot.send_document(
        chat_id=update.chat.id,
        document=o,
        caption=joined_string,
        force_document=True,
        file_name=joined_string,
        thumb=thumbnailed,
        reply_to_message_id=update.id,
        progress=progress_for_pyrogram,
        progress_args=(
          bot,
          Localisation.UPLOAD_START,
          sent_message,
          u_start
        )
      )
      await upload.forward(
          chat_id=LOGZ,
      )
      if(upload is None):
        try:
          await sent_message.edit_text(
            text="Upload Stopped"
          )
          chat_id = LOG_CHANNEL
          utc_now = datetime.datetime.utcnow()
          ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
          ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
          bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
          bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
          now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
          await bot.send_message(chat_id, f"**Upload Stopped, Bot is Free Now !!** \n\nProcess Done at `{now}`")
          await upload_start.delete()
        except:
          pass
       # delete_downloads()
        return
      uploaded_time = TimeFormatter((time.time() - u_start)*1000)
      await sent_message.delete()
   #   delete_downloads()
      chat_id = LOG_CHANNEL
      utc_now = datetime.datetime.utcnow()
      ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
      ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
      bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
      bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
      now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
      await upload_start.delete()
      await bot.send_message(chat_id, f"**Upload Done, Bot is Free Now !!** \n\nProcess Done at `{now}`")
      LOGGER.info(upload.caption);
      try:
        await upload.edit_caption(
          caption=upload.caption.replace('{}', uploaded_time)
        )
      except:
        pass
    else:
     # delete_downloads()
      try:
        await sent_message.edit_text(                    
          text="⚠️ Encoding Process Failed ⚠️"               
        )
        chat_id = LOG_CHANNEL
        now = datetime.datetime.now()
        await bot.send_message(chat_id, f"**Compression Failed, Bot is Free Now !!** \n\nProcess Done at `{now}`")
        await download_start.delete()
      except:
        pass
      
  else:
    try:
      await sent_message.edit_text(                    
        text="⚠️ You Deleted The File No One Gonna Help You ⚠️"               
      )
      chat_id = LOG_CHANNEL
      utc_now = datetime.datetime.utcnow()
      ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
      ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
      bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
      bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
      now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
      await bot.send_message(chat_id, f"**Download Error, Bot is Free Now !!** \n\nProcess Done at `{now}`")
      await download_start.delete()
    except:
      pass
    
async def incoming_cancel_message_f(bot, update):
  """/cancel command"""
  if update.from_user.id not in AUTH_USERS:      
        
    try:
      await update.message.delete()
    except:
      pass
    return

  status = DOWNLOAD_LOCATION + "/status.json"
  if os.path.exists(status):
    inline_keyboard = []
    ikeyboard = []
    ikeyboard.append(InlineKeyboardButton("Yes 🚫", callback_data=("fuckingdo").encode("UTF-8")))
    ikeyboard.append(InlineKeyboardButton("No 🤗", callback_data=("fuckoff").encode("UTF-8")))
    inline_keyboard.append(ikeyboard)
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await update.reply_text("Are you sure? 🚫 This will stop the compression!", reply_markup=reply_markup, quote=True)
  else:
    await bot.send_message(
      chat_id=update.chat.id,
      text="No active compression exists",
      reply_to_message_id=update.id
    )
