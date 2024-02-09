import logging
import moviepy.editor as mp
import moviepy.video.fx.all as vfx
import os
import time
import keyboards as kb

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from moviepy.editor import *
from config import BOT_TOKEN



bot = Bot(token = BOT_TOKEN)
dp = Dispatcher(bot)



logging.basicConfig(level=logging.ERROR)


@dp.message_handler(commands=["start"])
async def start_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, text="Hello, You can send me your videos and I will make circles out of them. \nThere are two modes of operation: \n~Auto mode \n~Square mode. \nThe first is suitable for any video size, and the second is only for square. Both have their pros and cons. \nGood luck!")


@dp.message_handler(content_types=["video"])
async def download_video(msg: types.Message):
    file_id = msg.video.file_id # Get file id
    file = await bot.get_file(file_id) # Get file path
    await bot.download_file(file.file_path, "video.mp4")
    await bot.send_message(msg.from_user.id, text = "one second (5~10), this video is downloading")
    time.sleep(5)
    await bot.send_message(msg.from_user.id, text = "choice mode", reply_markup=kb.mode_selection)


@dp.message_handler(lambda message: message.text == "Square Mode")
async def square_mode(msg: types.Message):
    stats = os.stat("video.mp4")
    clip = VideoFileClip("video.mp4")
    value = clip.size
    print(value[0], value[1])
    if (value[0] > 500) or (value[1] > 500):
        if value[0] == value[1]:
            await bot.send_message(msg.from_user.id, text = "square, but larger than 500x500")
            os.remove("video.mp4")
        else:
            await bot.send_message(msg.from_user.id, text = "not square")
            os.remove("video.mp4")                 
    else:
        if stats.st_size > 8388608:
            await bot.send_message(msg.from_user.id, text = "square, but more than 8mb")
            os.remove("video.mp4")
        else:
            await bot.send_video_note(msg.from_user.id, video_note=open("video.mp4", "rb"))
            os.remove("video.mp4")


@dp.message_handler(lambda message: message.text == "Auto Mode")
async def auto_mode(msg: types.Message):
    stats = os.stat("video.mp4")
    clip = VideoFileClip("video.mp4")
    value = clip.size
    print(value[0], value[1])
    if (value[0] == value[1]) and (value[0] + value[1] <= 1000):
        await bot.send_video_note(msg.from_user.id, video_note=open("video.mp4", "rb"))
    else:
        if stats.st_size > 8388608:
            await bot.send_message(msg.from_user.id, text = "video is too big")
            os.remove("video.mp4")
        else:
            clip_16_9 = mp.VideoFileClip("video.mp4")
            clip_9_16 = vfx.crop(clip_16_9, x1=0, y1=0, width=500, height=500)
            clip_9_16.write_videofile("output.mp4")       
            await bot.send_message(msg.from_user.id, text = "I am working...")
            time.sleep(2)
            await bot.send_message(msg.from_user.id, text = "I am working...")
            time.sleep(2)
            await bot.send_message(msg.from_user.id, text = "I am working...")       
            await bot.send_video_note(msg.from_user.id, video_note=open("output.mp4", "rb"))
            os.remove("video.mp4")
            os.remove("output.mp4")        


if __name__ == '__main__':
    executor.start_polling(dp)