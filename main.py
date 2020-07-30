file_input = open('data.txt', 'r')
lines = file_input.readlines()

userFriendList = {}
sumUser = sum(1 for _ in file_input)
for line in lines:
    user,friendListString = line.split('\t')
    user = int(user)
    if len(friendListString) != 1: # bo nhung id nao ko co ban
        removeddownline, downline = friendListString.split('\n') #tach ki tu xuong dong \n
        friends = removeddownline.split(',') #bo dau ,   
        friendList = []
        for i in friends:
            friendList.append(i)
        if friendList:
            userFriendList[user] = friendList #tao mot dic chua friend
        

file_input.close()

U = int(input())
N = int(input())

recommentFriend = {} #tao hang cho

output = open('output.txt','w')
if U not in userFriendList: # neu ko co ban hoac ko ton tai
    output.write("Not have a friend or this id is not exist")
else: 
    for i in userFriendList:
        if( i != U):
            setUser = set(userFriendList[U]) 
            setOtherUser = set(userFriendList[i])
            mutualFriend = setUser.intersection(setOtherUser) #tim so ban giong nhau
            if len(recommentFriend) < N : #neu hang cho chua day
                recommentFriend[i] = len(mutualFriend)
            else:
                minval = min(recommentFriend.values()) #tim value nho nhat trong hang cho
                if len(mutualFriend) >= minval :
                    res = [k for k, v in recommentFriend.items() if v==minval] #tim list key co value be nhat
                    res.sort()
                    recommentFriend[i] = len(mutualFriend) 
                    del recommentFriend[res.pop()] #xoa phan tu 
    
    rcmtFriendList = [str(interger) for interger in recommentFriend.keys()]
    string_rcmtFriendList = "\n".join(rcmtFriendList)
    output.write(string_rcmtFriendList)
    


