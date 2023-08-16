# image_styling_tg_bot

This is an english version of [my final project](https://github.com/tipofyzik/ImageStyling_tgbot) that I've made on the [Deep Learning School course by MIPT](https://dls.samcs.ru/en/dls) this june. The original was written in russian, so you can translate it with google. I reworked the structure of the text a little, but the essence is the same.

Brief explanation of my project's goal: First of all, it was necessary to create a telegram bot that can transfer image style from one image to another. The bot should be based on Generative Adversarial Network (GAN). An additional goal was to deploy the bot to the server. I've done both of them! Entire code was written in Python.

For not wasting the resources of the server the bot was stopped. You can run your own by downloading repository and following the deploy server instruction (see "Docker and deploy" section).  
My telegram bot: @image_styling_tg_bot

## About the repository usage before we start
  1. Folder "Notebook": it contains notebook and necessary photos for it. This is solely required for showcasing the operation of the chosen GAN and is not necessary for the functioning of the Telegram bot.
  2. To run your own bot you need:  
     **•** Download the "tgbot" folder, the "app.py", and the "API.txt" files  
     **•** [Create your own bot](https://sendpulse.com/knowledge-base/chatbot/telegram/create-telegram-chatbot#create-bot) (read the 1st chapter)  
     **•** Copy an API that was given by @BotFather and put it in **API.txt**    
     **•** Install all required libraries (see "requirements.txt")  
     **•** Run "app.py"
  3. If you wanna run your bot through docker you also need to download the dockerfile and follow the instruction from the "Docker and deploy" section.

## 1. Bot neural network selection
  The MSG-Net was selected in the [implementation from zhanghang1989](https://github.com/zhanghang1989/PyTorch-Multi-Style-Transfer). Other networks like [CycleGan](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix) or [Deep Photo Style Transfer](https://github.com/ray075hl/DeepPhotoStyle_pytorch) (DPST) were also considered when choosing a network. However, I stopped on the MSG-Net for the following reasons:
  **•** The main reason is that MSGNet is not as resource-intensive as, for example, Deep Photo Style Transfer, which consequently results in relatively fast image processing speed and allows deploying the network on free resources.
  **•** An equally important reason is that the neural network achieves a commendable level of style transfer quality compared with CycleGan and similar models.
  **•** The implementation is clear and consice, making it possible to integrate MSG-Net into the bot without significant effort. 

Nevertheless, in comparison with DPST network, the MSG-Net has a significant lack: It ocassionally results in uneven style transfer. 

There is an example: I uploaded the cat photo as the original image and the starry sky as the style. I haven't recieved starry cat as output, it just became multicolor:) I think this is because there are not enough layers in the MSG-Net, especially compared with DPST. The latter uses VGG-19 network features that obviously gives a essentially better result. So, times to times the result may not meet expectations.  
![image](https://github.com/tipofyzik/image_styling_tg_bot/assets/84290230/40c644fa-febd-42f7-9d7c-ba3768a0e398)

**About fixing errors in the code**:  


## 2. About creating and using a bot

## 3. Docker and deploy

## 4. Usage restrictions

## 5. Results
