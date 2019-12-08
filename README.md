# TOC Project 2020
## Language: Python3 
## Usage
Get particular game informations from tos.fandom.com.
The website has too many useless informations and ads. It takes a long time for loading.
Sometimes I just want to take a look for part of the information, and it takes a long time too.
As a result, I take the informations I need, and arrange them in my favor.
Helping me from ads and long waiting time.
## Code decription
Main process I write is in "work.py" and in part of "app.py". Other codes are the same as the assistant's. 
In "work.py", there is a class named "StateMachine". 
It is used to get input and automatically transform to the state it should be. Then return 
a list of string for printing out. The functions in "StateMachine" are not for user except "get_text()". 
Throw any input in "get_text()", and it will return the string you should print out. 
There are four states in "StateMachine", and they are "start", "web", "hell", "info". 
As the "get_text()" being activated, the "StateMachine" check the and respond. Clearly, in "web" state 
called "web_state()", in "hell" state called "hell_state()".
* Function description:
THE FUNCTIONS NEED TO MAINTAIN!!</br>
Functions are based on regular expression module and urllib module. First I get all the website
 content, and I use "re.findall()" to get the information I need. Like, name of the stage, url 
 of the inormation page. Because the information I need always locates between some particular words, I 
 can find the information I need. But once the web page change their web style, my function here my not
 work.</br>
* app.py changes:
-The reply lines are deleted.</br>
+Add global dict to store many "StateMachine". (Dependents on user_id)</br>
+In "callback()", I get the user_id first. In order to reply the users personally.</br>
+Create a new "StateMachine" if the user_id has no "StateMachine" yet.</br>
+Throw the user input to "StateMachine", and reply to user what "StateMachine" return.</br>
## Notice
1. This code cannot run locally (Myabe it is because of my computer). Push to heroku, and connect with Line to test it.
2. DO NOT touch the "StateMachine". It is horrible! Write another one if you need it!
3. All the skills in this project is "regular expression", "urllib". The "StateMachine" is a mess. No need to understand "StateMachine"
4. The functions may not work after the website changes.












# Below is assistant's README
--------------------------------------------------------------------------------------------------------------

[![Maintainability](https://api.codeclimate.com/v1/badges/dc7fa47fcd809b99d087/maintainability)](https://codeclimate.com/github/NCKU-CCS/TOC-Project-2020/maintainability)

[![Known Vulnerabilities](https://snyk.io/test/github/NCKU-CCS/TOC-Project-2020/badge.svg)](https://snyk.io/test/github/NCKU-CCS/TOC-Project-2020)


Template Code for TOC Project 2020

A Line bot based on a finite state machine

More details in the [Slides](https://hackmd.io/@TTW/ToC-2019-Project#) and [FAQ](https://hackmd.io/s/B1Xw7E8kN)

## Setup

### Prerequisite
* Python 3.6
* Pipenv
* Facebook Page and App
* HTTPS Server

#### Install Dependency
```sh
pip3 install pipenv

pipenv --three

pipenv install

pipenv shell
```

* pygraphviz (For visualizing Finite State Machine)
    * [Setup pygraphviz on Ubuntu](http://www.jianshu.com/p/a3da7ecc5303)
	* [Note: macOS Install error](https://github.com/pygraphviz/pygraphviz/issues/100)


#### Secret Data
You should generate a `.env` file to set Environment Variables refer to our `.env.sample`.
`LINE_CHANNEL_SECRET` and `LINE_CHANNEL_ACCESS_TOKEN` **MUST** be set to proper values.
Otherwise, you might not be able to run your code.

#### Run Locally
You can either setup https server or using `ngrok` as a proxy.

#### a. Ngrok installation
* [ macOS, Windows, Linux](https://ngrok.com/download)

or you can use Homebrew (MAC)
```sh
brew cask install ngrok
```

**`ngrok` would be used in the following instruction**

```sh
ngrok http 8000
```

After that, `ngrok` would generate a https URL.

#### Run the sever

```sh
python3 app.py
```

#### b. Servo

Or You can use [servo](http://serveo.net/) to expose local servers to the internet.


## Finite State Machine
![fsm](./img/show-fsm.png)

## Usage
The initial state is set to `user`.

Every time `user` state is triggered to `advance` to another state, it will `go_back` to `user` state after the bot replies corresponding message.

* user
	* Input: "go to state1"
		* Reply: "I'm entering state1"

	* Input: "go to state2"
		* Reply: "I'm entering state2"

## Deploy
Setting to deploy webhooks on Heroku.

### Heroku CLI installation

* [macOS, Windows](https://devcenter.heroku.com/articles/heroku-cli)

or you can use Homebrew (MAC)
```sh
brew tap heroku/brew && brew install heroku
```

or you can use Snap (Ubuntu 16+)
```sh
sudo snap install --classic heroku
```

### Connect to Heroku

1. Register Heroku: https://signup.heroku.com

2. Create Heroku project from website

3. CLI Login

	`heroku login`

### Upload project to Heroku

1. Add local project to Heroku project

	heroku git:remote -a {HEROKU_APP_NAME}

2. Upload project

	```
	git add .
	git commit -m "Add code"
	git push -f heroku master
	```

3. Set Environment - Line Messaging API Secret Keys

	```
	heroku config:set LINE_CHANNEL_SECRET=your_line_channel_secret
	heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
	```

4. Your Project is now running on Heroku!

	url: `{HEROKU_APP_NAME}.herokuapp.com/callback`

	debug command: `heroku logs --tail --app {HEROKU_APP_NAME}`

5. If fail with `pygraphviz` install errors

	run commands below can solve the problems
	```
	heroku buildpacks:set heroku/python
	heroku buildpacks:add --index 1 heroku-community/apt
	```

	refference: https://hackmd.io/@ccw/B1Xw7E8kN?type=view#Q2-如何在-Heroku-使用-pygraphviz

## Reference
[Pipenv](https://medium.com/@chihsuan/pipenv-更簡單-更快速的-python-套件管理工具-135a47e504f4) ❤️ [@chihsuan](https://github.com/chihsuan)

[TOC-Project-2019](https://github.com/winonecheng/TOC-Project-2019) ❤️ [@winonecheng](https://github.com/winonecheng)

Flask Architecture ❤️ [@Sirius207](https://github.com/Sirius207)

[Line line-bot-sdk-python](https://github.com/line/line-bot-sdk-python/tree/master/examples/flask-echo)
