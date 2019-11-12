# @Author: AnthonyKenny98
# @Date:   2019-11-09 17:42:17
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-11 19:49:04

echo Please enter GroupMe Access Token
read GroupMeAccessToken
heroku config:set GroupMeAccessToken=$GroupMeAccessToken
python3 setup.py 'GroupMe'


