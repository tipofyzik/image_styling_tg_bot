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



## 2. About using a bot
The bot was created by @BotFather. You can read more about its creating [here](https://sendpulse.com/knowledge-base/chatbot/telegram/create-telegram-chatbot#create-bot). Also I used [aiogram](https://docs.aiogram.dev/en/latest/) framework to write bot functionality. If you wanna see for other sources go to the last section. The work of the bot will be discussed further.



## 3. Docker and deploy
Here we'll discuss how to create docker image, upload it on docker hub and deploy you telegram bot. That was completely new information for me, so I'll try to explain it as crearly as possible. If you know nothing about docker how ot was with me you can read the basics [here](https://en.wikipedia.org/wiki/Docker_(software)). 

So what should we do to deploy our bot? Let's take a closer look:
1. First of all, we should install docker desktop on pc. You can download it [here](https://www.docker.com/).  
2. Next, it's necessary to write two files - one with the required libraries and the second directly with the dockerfile. First is a txt-file that's common named  "reqierements.txt" - you write here all libraries that are used. The second file is dockerfile which is a set of commands for building a docker image. An example, excepting for files in my repository, canbe seen, for an instance, [here](https://www.educative.io/answers/how-do-you-write-a-dockerfile).

Since 3rd point the first two must be completed and the docker desktop app must be run.  
3. Open the console and go to the directory where the project is located. Here we just creating our docker image by set of command in console:  
**•** docker build -t <your_image_name> <path_to_dockerfile>  
**(OPTIONAL)** After the build is complete, you can test your image by running it with the following command:  
**•** docker run <your_image_name>  
4. Next, we want to upload our docker image on docker hub. Open the site, register there, next, open the console and write:  
**•** docker login  
After you logged in, we write these two commands:  
**•** docker tag <your_image_name> <dockerhub_username>/<your_image_name>  
**•** docker push <dockerhub_username>/<your_image_name>  
The first line creates new name for our docker image; this is necessary for uploading it on docker hub. The second line uploads our image on the site.

The last part - run on server. All we need:  
5. Open [docker playground](https://www.docker.com/play-with-docker/) and choose the "Lab Environment".
![image](https://github.com/tipofyzik/image_styling_tg_bot/assets/84290230/cba3d20b-e3e6-4d22-abe3-7d68bf67b93d)  
6. Log in (credentials from docker.com) and click on "add new instance".  
7. Finally, in appeared console, we write:  
**•** docker run -it <dockerhub_username>/<your_image_name>  
After this, your dicker image will be downloded on your server and will be run. That's all, you can use your bot!

**Important note:**  
When writing a project's dependency file, I strongly recommend installing only the bare minimum required for the bot (and for any other project) to function. It will significantly decrease your docker image size,  thus requiring fewer server resources. For example, initially I installed all torch library and my size of my docker file was 7.5GB. After I installed only torch-CPU, the essentials required to run Python, and cleared all cache, the size has been reduced to 1GB.



## 4. Usage restrictions
All limitations are related to small amounts of free memory on the server. So, it's more recommendations to using a bot:  
**•** The input images are resized to 512 * 512 pixels. Despite the fact that it reduces the quality of the resulting image, it also increases the speed of processing input images and obtaining the result. You can change this parameter int the **transform_image()** function in the **tgbot.py** file, but remember that it will extremely increase precessing time, so you should do it on your pc or on paid server.    
**•** As the resources of the server are poor, I wouldn't recommend to upload large-size photos. It should be max 5MBytes so as not to kill the server.   
**•** The docker playground server has only 4GB of memory and a limited 4-hour session, but that's enough to launch with our parameters.



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
[9] Creating dockerfile: https://www.educative.io/answers/how-do-you-write-a-dockerfile  
[10] Docker hub (to upload docker image): https://hub.docker.com/  
[11] Docker playground (to deploy telegram bot): https://www.docker.com/play-with-docker/

