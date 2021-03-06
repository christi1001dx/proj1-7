from pymongo import MongoClient
client = MongoClient()
users = client.db.users
users.remove()

def authenticate(username,pw):
    return users.find({"username":username,"pw":pw},field={"_id":False}).count() != 0

def changepw(username,pw):
    users.update({'username':username},{"$set":{'pw':pw}},upsert=False)

def register(fname,lname,username,pw):
    if users.find({}).count() == 0:
        users.insert({"username":username,"pw":pw,'fname':fname,'lname':lname,"ADMIN":True})
    elif users.find({"username":username}).count() == 0:
        users.insert({"username":username,"pw":pw,'fname':fname,'lname':lname,"ADMIN":False})
    else: return False
    return True

def admin(username):
    return users.find({"username":username,"ADMIN":True}).count() != 0

def getName(username):
    l = [x for x in users.find({"username":username},fields={'_id':False,'username':False,'pw':False,'ADMIN':False})][0]
    name = l['fname'] + " " +l['lname']
    return name
    
if __name__ == "__main__":
    register('kevin','lin','kevinlin','asd','asd')
    register('brian','liu','brianliu','zxc','zxc')
    register('jason','chen','jasonchen','qwe','qwe')

    if authenticate('kevinlin','asd'):
        print("kevinlin passed \n")
    if not authenticate('kevinlin','qwe'):
        print('kevinlin did not pass \n')

    changepw('kevinlin','qwe')
    if authenticate('kevinlin','qwe'):
        print('kevinlin"s pw is now qwe \n')

    if admin('kevinlin'):
        print('kevinlin is the admin \n')
    if not admin('brianliu'):
        print('brianliu is not the admin \n')
        
    print("name: %s \n" %(getName('jasonchen')))

        

