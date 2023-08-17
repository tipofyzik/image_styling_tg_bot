from tgbot.MSGNet import *

from aiogram import Bot, Dispatcher, executor, types
import shutil
import os



# Create model instance
model = Net(ngf=128)
model_dict = torch.load('tgbot/21styles.model')
model_dict_clone = model_dict.copy()
for key, value in model_dict_clone.items():
    if key.endswith(('running_mean', 'running_var')):
        del model_dict[key]
model.load_state_dict(model_dict, False)

# Now we need to implement the image transformation function
async def transform_image(original_image, style_image, image_size, path):
   content_image = tensor_load_rgbimage(original_image, size=image_size,keep_asp=True).unsqueeze(0)
   style = tensor_load_rgbimage(style_image, size=image_size).unsqueeze(0)
   style = preprocess_batch(style)
   style_v = Variable(style)
   content_image = Variable(preprocess_batch(content_image))
   model.setTarget(style_v)
   output = model(content_image)
   tensor_save_bgrimage(output.data[0], f'{path}/result.jpg', False)

# Bot initialization
with open('API.txt', 'r') as file:
   TG_BOT_TOKEN=file.readline()
bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher(bot)

global original, style
global x, y
x=y=original=style=None


def firstkeyboard():
   button=[
      [types.KeyboardButton(text="/help"),
      types.KeyboardButton(text="/transfer_style"),
      types.KeyboardButton(text="/restart")]
   ]
   keyboard = types.ReplyKeyboardMarkup(
      keyboard=button, 
      resize_keyboard=True)
   return keyboard

def keyboard():
   buttons=[
      [types.KeyboardButton(text="/original_image"),
      types.KeyboardButton(text="/style_image"),
      types.KeyboardButton(text="/restart")]
   ]
   if x is not None and y is not None:
      buttons[0].insert(-1, types.KeyboardButton(text="/result"))

   keyboard = types.ReplyKeyboardMarkup(
      keyboard=buttons, 
      resize_keyboard=True)
   return keyboard



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
   global original, style
   global x, y
   x=y=original=style=None
   await message.answer("""Hello!
I'm a bot that will help you transfer the style of one image to another.
To learn about the functionality, use the command /help.
To proceed to photo upload, use the command /transfer_style.
""", reply_markup=firstkeyboard()) #Since the code works asynchronously, we must write await.

@dp.message_handler(commands=['help'])
async def get_images(message: types.Message):
   text=f"""/transfer\_style - allows you to proceed to photo upload.
/original\_image - allows you to upload the photo on which the style will be transferred.
/style\_image - allows you to upload the photo from which the style will be taken.
/result - once both images are uploaded, allows you to see the result.
/restart - if you want to return to the main menu. The command is available at all times.

/tests - here developer test results are shown. Press or type /test to learn more. This command doesn't affect the bot's functionality.

Enjoy your time!"""
   await message.answer(text, parse_mode=types.ParseMode.MARKDOWN)

@dp.message_handler(commands=['transfer_style'])
async def get_images(message: types.Message):
   await message.answer("""You can start uploading the photos, don't forget to specify the type of photo - original or style!
To do this, click on the corresponding button or enter the command manually. You can upload photos in any order, the main thing is to upload both.""", reply_markup=keyboard())

@dp.message_handler(commands=['original_image'])
async def get_original_images(message):
   global original, style
   await message.answer("Upload the photo _on which_ you want to transfer the style.", 
                        parse_mode=types.ParseMode.MARKDOWN, reply_markup=keyboard())
   original=True
   style=False

@dp.message_handler(commands=['style_image'])
async def get_style_images(message):
   global style, original
   await message.answer("Upload the photo _from which_ you want to transfer the style.", 
                        parse_mode=types.ParseMode.MARKDOWN, reply_markup=keyboard())
   style=True
   original=False

@dp.message_handler(content_types=['photo'])
async def save_image(message):
   global original, style
   global x, y
   if original is None and style is None:
      await message.answer("""The type of photo was not specified!
Please select the type of photo by entering the appropriate command, and then upload the photo again.""")
   elif original:
      await message.photo[-1].download(destination_file=f'{message.from_user.username}/original_image.jpg')
      await message.answer("Original received!")
      x=True
      if x and y:
         await message.answer("Hooray, all the photos are here! You can now check out the result.", reply_markup=keyboard())
   elif style:
      await message.photo[-1].download(destination_file=f'{message.from_user.username}/style_image.jpg')
      await message.answer("Style recieved!")
      y=True
      if x and y:
         await message.answer("Hooray, all the photos are here! You can now check out the result.", reply_markup=keyboard())

# Функция по обработке изображений и получения результата
@dp.message_handler(commands=['result'])
async def result(message: types.Message):
   global x, y
   # Если хочется изменить размер изображения при обработке - поменяйте цифру в строке ниже
   image_size=512

   if x is None and y is None:
      await message.answer("No photos have been received yet! Use /transfer_style to proceed to the upload.")
   elif x is None:
      await message.answer("The original image was not received! To upload it, use /original_image.")
   elif y is None:
      await message.answer("The style was not received! To upload it, use /style_image.")
   else:
      await message.answer("Please wait, the image processing is in progress...")
      await transform_image(f'{message.from_user.username}/original_image.jpg', 
                     f'{message.from_user.username}/style_image.jpg', image_size=image_size, path=f'{message.from_user.username}')
      await bot.send_photo(chat_id=message.chat.id, photo=open(f'{message.from_user.username}/result.jpg', 'rb'), 
                           caption='Your modified photo!', reply_markup=keyboard())

# Функция возврата в меню start и очищение файлов
@dp.message_handler(commands=['restart'])
async def cancel_act(message: types.Message):
   if os.path.exists(f'{message.from_user.username}'):
      shutil.rmtree(f'{message.from_user.username}', ignore_errors=True)
   await message.answer("Uploaded images, if any, have been deleted! Let's start over.")
   await send_welcome(message)



@dp.message_handler(commands=['tests'])
async def show_tests(message: types.Message):
   await message.answer("""
This function displays tests. Here are 5 pictures, each is a result of the two photos below.
The first one is a turtle - the style of the second photo, which is a sunset, was transferred onto it.""", reply_markup=firstkeyboard())
   media_group = types.MediaGroup() 
   media_group.attach_photo(types.InputFile('tgbot/tests/turtle.jpeg'))
   media_group.attach_photo(types.InputFile('tgbot/tests/real_sunset.jpg'))
   await bot.send_media_group(chat_id=message.chat.id, media=media_group)

   await message.answer("""
Here are the transfer results at different image sizes: 512 -> 768 -> 1024 -> 1536 -> 2048 from the first to the last photo, respectively.
You can easily notice the changes even in compressed files by simply scrolling through the photos.""", reply_markup=firstkeyboard())
   media_group = types.MediaGroup() 
   media_group.attach_photo(types.InputFile('tgbot/tests/512.jpg'))
   media_group.attach_photo(types.InputFile('tgbot/tests/768.jpg'))
   media_group.attach_photo(types.InputFile('tgbot/tests/1024.jpg'))
   media_group.attach_photo(types.InputFile('tgbot/tests/1536.jpg'))
   media_group.attach_photo(types.InputFile('tgbot/tests/2048.jpg'))
   await bot.send_media_group(chat_id=message.chat.id, media=media_group)

   await message.answer("""
An image_size of 2048 caused my computer to glitch a bit, and with image_size of 4096, it couldn't handle it at all.
To optimize processing time, image_size was set to 512 - images are processed quickly and the result is almost immediate.
However, if you want to improve the transfer quality, I recommend setting the size to 1024 or 1536. Further increasing the size enhances quality, but not significantly.
""", reply_markup=firstkeyboard())



@dp.message_handler()
async def echo(message: types.Message):
   await message.reply("""I'm sorry, but I don't understand that command!
Use the /help command to familiarize yourself with my functionality.""")
   
