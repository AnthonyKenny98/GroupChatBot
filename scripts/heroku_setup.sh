# @Author: AnthonyKenny98
# @Date:   2019-11-09 15:16:36
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2020-03-23 19:28:22

heroku login -i

echo Please enter your desired heroku appname
read appName

heroku create $appName --buildpack heroku/python

heroku git:remote -a $appName

echo Please enter Reddit Client ID
read RedditClientID
echo Please enter Reddit Client Secret
read RedditClientSecret

heroku config:set RedditClientID=$RedditClientID
heroku config:set RedditClientSecret=$RedditClientSecret

git init .
git push heroku master