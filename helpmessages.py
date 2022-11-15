help_create="""This will prompt the Stable Horde network to create an image with the prompt
-h/-w # where # is an integer divisible by 64, max 1024, default 512
-steps # where # is an integer between 1 and 150, this determines in how many steps the model will create the image (default 50)
-cfg # where # is a float between 0 and 40 and it determines how strictly it will try to follow the prompt (default 7)
-seed # where # is an integer and it determines which seed will be used (default random between 0 10000)
-model ["model"] where "model" is the model you want to use to create the image, use /status and /models to get options
Example /create Photo of Werewolf eating broccoli, beautiful render, photorealistic, 4k -steps 60 -cfg 15 -model [Robo-Diffusion]"""

help_status="""This will return information of the current default model and sampler and also information about the number of tokens owned by the bot and the current queue"""

help_setsamplerglobal="""Changes the default sampler, do /setsamplerglobal "sampler"
to get all the options do /setsamplerglobal"""

help_setmodelglobal="""Changes the default sampler, do /setmodelglobal "model"
to get all the available models do /models"""

help_models = """Returns all the available models"""

help_github = """Returns link to github for this bot"""

help_info = """Returns information about a model
Example: /info -Microworlds"""