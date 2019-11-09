# @Author: AnthonyKenny98
# @Date:   2019-11-09 15:57:07
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-09 16:10:49

heroku login -i

echo Please enter the name of the heroku app you would like to destroy
read appName

heroku apps:destroy $appName --confirm $appName

env -i
git remote remove heroku