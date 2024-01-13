## Here be dragons

github keeps asking me to add a readme so here it is just so that it stops pestering me

will add stuff later

## Later is now!!

excuse the english i'm too lazy to switch the keyboards to do journaling. "official" doc coming soon tho

### MySQL

The MySQL database is set up so that it's only accessible from localhost by admin and 'bot' the latter being the `info.py` file through `mysql.connector` library. The thing is imported through a different name so pylance or whatever is resolving the import names for vscode specifically gets confused. But the python file works fine.

### VK 

For the VK bot I'm using the official `vk_api` module that allows to control a group bot. Simple and effective.

### Telegram

Here's a good one. Besides simple bots there are mini apps in Telegram that are web based. So in order for it to work the good way there has to be a web server that does get and/or post as a bare minimum. Maybe will go with php for the time being. The server side of the app should be in `./web` sometime soon.