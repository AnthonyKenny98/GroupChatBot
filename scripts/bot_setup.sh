# @Author: AnthonyKenny98
# @Date:   2019-11-09 17:42:17
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-11 19:35:05

python3 setup.py 
echo Please enter GroupMe Access Token again
read GroupMeAccessToken
heroku config:set GroupMeAccessToken=$GroupMeAccessToken


