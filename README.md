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
Entire code is the same except for the tensor_load_rgbimage(...) function. You can find it in "MSGNet.py" file. The problem iccured when you tried to resize your image, specifically, Image.ANTIALIAS parameter from the Pillow library caused the error. It deprecated and was removed on July 1, 2023.
![image](https://github.com/tipofyzik/image_styling_tg_bot/assets/84290230/e7456cb9-fd16-4c0f-a534-ccbb6a81c5ba)
For this reason, Image.LANCZOS parameter is used the results of which are scarcely inferior to the previous method.

## 2. About creating and using a bot
The bot was created by @BotFather. You can read more about its creating [here](https://sendpulse.com/knowledge-base/chatbot/telegram/create-telegram-chatbot#create-bot). Also I used [aiogram](https://docs.aiogram.dev/en/latest/) framework to write bot functionality. If you wanna see for other sources go to the last section. The work of the bot will be discussed further.



## 3. Docker and deploy

## 4. Usage restrictions
All limitations are related to small amounts of free memory on the server. So, it's more recommendations to using a bot:  
1. The input images are resized to 512 * 512 pixels. Despite the fact that it reduces the quality of the resulting image, it also increases the speed of processing input images and obtaining the result. You can change this parameter int the **transform_image()** function in the **tgbot.py** file.  
2. As the resources of the server are poor, I wouldn't recommend to upload large-size photos. It should be max 5MBytes so as not to kill the server.  
3. 

## 5. Results
Some good results recieved from the bot  
![image](https://github.com/tipofyzik/image_styling_tg_bot/assets/84290230/17b40370-fa9b-4a0c-8dd7-8f636398a6db)
![image](https://github.com/tipofyzik/image_styling_tg_bot/assets/84290230/96a238c2-134e-42d0-a496-10544f1c8046)

## 6. Sources
Russian sources (you can use the google translate if you need):  
[1] My original repository: https://github.com/tipofyzik/ImageStyling_tgbot  
[2] Creating simple function for your bot: https://mastergroosha.github.io/aiogram-3-guide/ 

English sources:  
[3] About the MSG-Net: https://www.researchgate.net/figure/An-overview-of-MSG-Net-Multi-style-Generative-Network-The-transformation-network_fig1_315489372  
[4] MSG-Net implementation: https://github.com/zhanghang1989/PyTorch-Multi-Style-Transfer  
[5] Aiogram documentation: https://docs.aiogram.dev/en/latest/  
[6] About docker: https://en.wikipedia.org/wiki/Docker_(software)  
[7] Docker official (for installation): https://www.docker.com/  
[8] Docker in VSCode (to create dockerfile): https://code.visualstudio.com/docs/containers/overview  
[9] Docker hub (to upload docker image): https://hub.docker.com/  
[10] Docker playground (to deploy telegram bot): https://www.docker.com/play-with-docker/

