# @Author: AnthonyKenny98
# @Date:   2019-11-09 15:16:36
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-09 16:10:40

heroku login -i

echo Please enter your desired heroku appname
read appName

heroku create $appName --buildpack heroku/python

heroku git:remote -a $appName

git init .
git push heroku master