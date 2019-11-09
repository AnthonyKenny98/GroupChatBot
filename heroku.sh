# @Author: AnthonyKenny98
# @Date:   2019-11-09 15:16:36
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-09 15:43:43

heroku login -i

heroku create --buildpack heroku/python

git push heroku master