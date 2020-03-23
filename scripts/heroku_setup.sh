# @Author: AnthonyKenny98
# @Date:   2019-11-09 15:16:36
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2020-03-23 19:59:57

heroku login -i

echo Please enter your desired heroku appname
read appName

heroku create $appName --buildpack heroku/python

git init .
git add -A
git commit -am "Heroku Commit"
heroku git:remote -a $appName
git push heroku master

echo Please enter Reddit Client ID
read RedditClientID
echo Please enter Reddit Client Secret
read RedditClientSecret

heroku config:set RedditClientID=$RedditClientID
heroku config:set RedditClientSecret=$RedditClientSecret