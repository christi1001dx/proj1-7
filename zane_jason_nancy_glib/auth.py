from pymongo import MongoClient
from bson.objectid import ObjectId

connection = MongoClient()
db = connection.database

def getStories(order):
    stories = [s for s in db.story.find()]
    return stories

def getStory(eyeD):
    story = [s for s in db.story.find({'_id':ObjectId(eyeD)})]
    story = story[0]
    return story[u'author'], story[u'title'], story[u'story']

def getStoryID(eyeD):
    story = db.story.find_one({'_id':eyeD})
    return story

def create(author, title, story):
    return db.story.insert({'author':author, 'title':title, 'story':story})

def register(user, pw):
    if not checkuser(user):
        db.login.insert({'user':user, 'pass':pw})
        return True
    else:
        return False
    
def checkuser(user):
    users = [user for user in db.login.find({'user':user},
                                            fields={'_id':False,'user':True})]
    return len(users)!=0

def changePass(user, pw, npw):
    if login(user,pw):
        db.login.update({'user':user}, {'$set': {'pass':npw}})
        return True
    else:
        return False

def login(user, pw):
    users = [user for user in db.login.find({'user':user}, 
                                           fields={'_id':False,'user':True, 'pass':True})]
    if len(users) != 0:
        return users[0]['pass'] == pw
    else:
        return False
