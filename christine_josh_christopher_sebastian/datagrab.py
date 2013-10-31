import sqlite3

def addUser(username, password):
    #used in the register page to create accounts
    #returns False if the username already exists
    connection = sqlite3.connect('OnceUponData.db')
    q = "select * from account_info where username=?"
    cursor = connection.execute(q, [username])
    results = [line for line in cursor]
    if len(results) == 0:
        q = "insert into account_info values(?, ?, 0, '', '', '', '', '')"
        connection.execute(q, [username, password])
        connection.commit()
        return True
    else:
        return False


def authenticate(username, password):
    #used when logging in to verify account info
    #returns whether or not the username/password combo is valid
    connection = sqlite3.connect('OnceUponData.db')
    q = "select password from account_info where username=?"
    cursor = connection.execute(q, [username])
    results = [line for line in cursor]
    if len(results) == 1 and password == results[0][0]:
        return True
    else:
        return False
    


def likeEdit(editID, sourceUser):
    #sourceUser is adding one to the karma of edit with editID
    #returns False if a user tries to like their own edit or like an edit twice
    connection = sqlite3.connect('OnceUponData.db')
    q = "select user from edits where id=?"
    cursor = connection.execute(q, [editID])
    targetUser = [line for line in cursor]
    targetUser = targetUser[0][0].encode('ascii','inore')
    if targetUser == sourceUser:
        return False
    q = "select liked_edits from account_info where username=?"
    cursor = connection.execute(q, [sourceUser])
    likedEdits = [line for line in cursor]
    q = "select disliked_edits from account_info where username=?"
    cursor = connection.execute(q, [sourceUser])
    dislikedEdits = [line for line in cursor]
    if likedEdits[0][0] != '':
        likedEdits = likedEdits[0][0].split(',')
        for edit in likedEdits:
            if edit == "%i"%(editID):
                return False
        updatedLikedEdits = ",".join(likedEdits) + ",%i"%(editID)
    else:        
        updatedLikedEdits = "%i"%(editID)

    if dislikedEdits[0][0] != '':
        dislikedEdits = dislikedEdits[0][0].split(',')
        for edit in dislikedEdits:
            if edit == "%i"%(editID):
                return False
            
    q = "select karma from account_info where username=?"
    cursor = connection.execute(q, [targetUser])
    currentKarma = [line for line in cursor]
    q = "update account_info set karma=? where username=?"
    connection.execute(q, [currentKarma[0][0]+1, targetUser])
    q = "update account_info set liked_edits=? where username=?"
    connection.execute(q, [updatedLikedEdits, sourceUser])
    connection.commit()
    return True


def dislikeEdit(editID, sourceUser):
    #sourceUser is subtracting one from the karma of edit with editID
    #returns False if a user tries to dislike their own edit or dislike an edit twice
    connection = sqlite3.connect('OnceUponData.db')
    q = "select user from edits where id=?"
    cursor = connection.execute(q, [editID])
    targetUser = [line for line in cursor]
    targetUser = targetUser[0][0].encode('ascii','inore')

    if targetUser == sourceUser:
        return False
    q = "select liked_edits from account_info where username=?"
    cursor = connection.execute(q, [sourceUser])
    likedEdits = [line for line in cursor]
    q = "select disliked_edits from account_info where username=?"
    cursor = connection.execute(q, [sourceUser])
    dislikedEdits = [line for line in cursor]

    
    if likedEdits[0][0] != '':
        likedEdits = likedEdits[0][0].split(',')
        for edit in likedEdits:
            if edit == "%i"%(editID):
                return False

    if dislikedEdits[0][0] != '':
        dislikedEdits = dislikedEdits[0][0].split(',')
        for edit in dislikedEdits:
            if edit == "%i"%(editID):
                return False
        updatedDislikedEdits = ",".join(dislikedEdits) + ",%i"%(editID)
    else:
        updatedDislikedEdits = "%i"%(editID)

    q = "select karma from account_info where username=?"
    cursor = connection.execute(q, [targetUser])
    currentKarma = [line for line in cursor]
    q = "update account_info set karma=? where username=?"
    connection.execute(q, [currentKarma[0][0]-1, targetUser])
    q = "update account_info set disliked_edits=? where username=?"
    connection.execute(q, [updatedDislikedEdits, sourceUser])
    connection.commit()
    return True


def likeStory(storyID, user):
    #user is adding one to the karma of story with storyID
    #returns False if a user tries to like their own story or like a story twice
    connection = sqlite3.connect('OnceUponData.db')
    q = "select user from stories where id=?"
    cursor = connection.execute(q, [storyID])
    targetUser = [line for line in cursor]
    targetUser = targetUser[0][0].encode('ascii','inore')

    if targetUser == user:
        return False
    q = "select liked_stories from account_info where username=?"
    cursor = connection.execute(q, [user])
    likedStories = [line for line in cursor]
    q = "select disliked_stories from account_info where username=?"
    cursor = connection.execute(q, [user])
    dislikedStories = [line for line in cursor]

    
    if likedStories[0][0] != '':
        likedStories = likedStories[0][0].split(',')
        for story in likedStories:
            if story == "%i"%(storyID):
                return False
        updatedLikedStories = ",".join(LikedStories) + ",%i"%(storyID)
    else:
        updatedLikedStories = "%i"%(storyID)


    if dislikedStories[0][0] != '':
        dislikedStories = dislikedStories[0][0].split(',')
        for story in dislikedStories:
            if story == "%i"%(storyID):
                return False
        

    q = "select karma from account_info where username=?"
    cursor = connection.execute(q, [targetUser])
    currentKarma = [line for line in cursor]
    q = "update account_info set karma=? where username=?"
    connection.execute(q, [currentKarma[0][0]+1, targetUser])

    q = "select karma from stories where id=?"
    cursor = connection.execute(q, [storyID])
    currentStoryKarma = [line for line in cursor]
    q = "update stories set karma=? where id=?"
    connection.execute(q, [currentStoryKarma[0][0]+1, storyID])

    q = "update account_info set liked_stories=? where username=?"
    connection.execute(q, [updatedLikedStories, user])
    connection.commit()
    return True

def dislikeStory(storyID, user):
    #user is subtracting one from the karma of story with storyID
    #returns False if a user tries to dislike their own story or dislike a story twice
    connection = sqlite3.connect('OnceUponData.db')
    q = "select user from stories where id=?"
    cursor = connection.execute(q, [storyID])
    targetUser = [line for line in cursor]
    targetUser = targetUser[0][0].encode('ascii','inore')

    if targetUser == user:
        return False
    q = "select liked_stories from account_info where username=?"
    cursor = connection.execute(q, [user])
    likedStories = [line for line in cursor]
    q = "select disliked_stories from account_info where username=?"
    cursor = connection.execute(q, [user])
    dislikedStories = [line for line in cursor]

    
    if likedStories[0][0] != '':
        likedStories = likedStories[0][0].split(',')
        for story in likedStories:
            if story == "%i"%(storyID):
                return False

    if dislikedStories[0][0] != '':
        dislikedStories = dislikedStories[0][0].split(',')
        for story in dislikedStories:
            if story == "%i"%(storyID):
                return False
        updatedDislikedStories = ",".join(dislikedStories) + ",%i"%(storyID)
    else:
        updatedDislikedStories = "%i"%(storyID)

    q = "select karma from account_info where username=?"
    cursor = connection.execute(q, [targetUser])
    currentKarma = [line for line in cursor]
    q = "update account_info set karma=? where username=?"
    connection.execute(q, [currentKarma[0][0]-1, targetUser])
    q = "update account_info set disliked_stories=? where username=?"
    connection.execute(q, [updatedDislikedStories, user])
    connection.commit()
    return True


def newEdit(storyID, text, user):
    #user adds a new edit (text) to the story with ID storyID
    #returns False if trying to edit root story ('Once upon a time')
    connection = sqlite3.connect('OnceUponData.db')
    if storyID == 0:
        return False
    q = "select id from edits"
    cursor = connection.execute(q)
    existingIDs = [x for x in cursor]
    maxID = -1
    for x in range (0,len(existingIDs)):
        if existingIDs[x][0] > maxID:
            maxID = existingIDs[x][0]
    editID = maxID + 1
    q = "insert into edits values(?,?,?)"
    connection.execute(q,[editID,text,user])
    q = "select edits from stories where id=?"
    cursor = connection.execute(q,[storyID])
    edits = [x for x in cursor]
    edits = edits[0][0].encode('ascii','ignore')
    edits = edits + ",%i"%(editID)
    q = "update stories set edits=? where id=?"
    connection.execute(q,[edits,storyID])
    connection.commit()


def newStory(name, storyID, user):
    #user forks the story with ID storyID and calls it name
    connection = sqlite3.connect('OnceUponData.db')    
    pass

def getStory(storyID):
    #returns the story with ID storyID as a single string
    connection = sqlite3.connect('OnceUponData.db')
    q = "select edits from stories where id=?"
    cursor = connection.execute(q,[storyID])
    editIDs = [x for x in cursor]
    editIDs = editIDs[0][0].encode('ascii','ignore')
    editIDs = editIDs.split(',')
    story = ""
    for editID in editIDs:
        q = "select sentence from edits where id=?"
        cursor = connection.execute(q,[editID])
        edit = [x for x in cursor]
        edit = edit[0][0].encode('ascii','ignore')
        story = story + " " + edit
    return story[1:]

def getUserKarma(user):
    #returns the karma of user
    connection = sqlite3.connect('OnceUponData.db')
    q = "select karma from account_info where username=?"
    cursor = connection.execute(q,[user])
    karma = [x for x in cursor]
    karma = karma[0][0]
    return karma

def getStoryKarma(storyID):
    #returns the karma of story with ID storyID
    connection = sqlite3.connect('OnceUponData.db')
    q = "select karma from stories where id=?"
    cursor = connection.execute(q,[storyID])
    karma = [x for x in cursor]
    karma = karma[0][0]
    return karma
        