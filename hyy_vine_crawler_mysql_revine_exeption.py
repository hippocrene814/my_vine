'''
This script is writen by Bowei Zhang at 3/31/2015 for scraping vine data and
put them into MySQL database
'''
import peewee
import MySQLdb
import urllib2
import json
import time

# Get JSON file for specific Vine account page from internet which contains all the account information

def getJSON(user_name):
    try:
        response = urllib2.urlopen('https://vine.co/api/users/profiles/' + user_name)
        res = json.load(response)
    except urllib2.HTTPError as e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
    except urllib2.URLError as e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
    return res


# Get Vine account profile information from previous JSON file

def get_user_data(res):
    user_data = {}
    user_data['username'] = (res['data']['username'].encode('utf-8'))
    user_data['date'] = (time.strftime('%Y-%m-%d'))
    user_data['user_id'] = (str(res['data']['userId']))
    user_data['post_count'] = (res['data']['postCount'])
    user_data['follower_count'] = (res['data']['followerCount'])
    user_data['following_count'] = (res['data']['followingCount'])
    user_data['loop_count'] = (res['data']['loopCount'])
    user_data['like_count'] = (res['data']['likeCount'])
    #print user_data
    #print type(user_data)
    user_data_list = []
    user_data_list.append(user_data)
    #print user_data_list
    return user_data_list

# Get each post information for a specific Vine account from timeline JSON file

def get_post_data(res):
    user_id = res['data']['userId']
    #print user_id,user_name
    post_count = res['data']['postCount']
    #print post_count
    user_name = res['data']['username'].encode('utf-8')
    #print user_name

    try:
        response2 = urllib2.urlopen('https://vine.co/api/timelines/users/' + str(user_id) + '?size=' + str(post_count))
    except urllib2.HTTPError as e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
    except urllib2.URLError as e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason


    json_post_data = json.load(response2)

    record = json_post_data['data']['records']

    post_data = {}
    post_data_list = []
    for x in range(0, len(record)):
        if record[x]['userId'] != user_id:

            post_data['username'] = res['data']['username'].encode('utf-8')
            post_data['created'] = (record[x]['created'].encode('utf-8'))
            post_data['likes'] = (record[x]['likes']['count'])
            post_data['reposts'] = (record[x]['reposts']['count'])
            post_data['loops'] = (record[x]['loops']['count'])
            post_data['comments'] = (record[x]['comments']['count'])
            post_data['description'] = (record[x]['description'].encode('unicode-escape'))
            post_data['video_link'] = (record[x]['videoUrl'])
            post_data['revine_check'] = 1
            post_data['revined_user'] = (record[x]['username'].encode('utf-8'))
            post_data_list.append(post_data)
            post_data = {}
        elif record[x]['userId'] == user_id:
            post_data['username'] = res['data']['username'].encode('utf-8')
            post_data['created'] = (record[x]['created'].encode('utf-8'))
            post_data['likes'] = (record[x]['likes']['count'])
            post_data['reposts'] = (record[x]['reposts']['count'])
            post_data['loops'] = (record[x]['loops']['count'])
            post_data['comments'] = (record[x]['comments']['count'])
            post_data['description'] = (record[x]['description'].encode('unicode-escape'))
            post_data['video_link'] = (record[x]['videoUrl'])
            post_data['revine_check'] = 0
            # post_data['revined_user'] = (record[x]['username'].encode('utf-8'))
            post_data_list.append(post_data)
            post_data = {}

    #print post_data_list
    return post_data_list


# Connecting MySQL and insert Vine data into the databases
def connection(user_data_list,post_data_list):

    # database name, user name, pw
    mysql_db = peewee.MySQLDatabase('social', user='bowei', password ='R0chester!')

    class MySQLModel(peewee.Model):
        """A base model that will use our MySQL database"""

        class Meta:
            database = mysql_db

    class vine_post_test(MySQLModel):
        username = peewee.CharField()
        created = peewee.DateTimeField()
        likes = peewee.IntegerField()
        reposts = peewee.IntegerField()
        loops = peewee.IntegerField()
        comments = peewee.IntegerField()
        description = peewee.CharField()
        video_link = peewee.CharField()
        revine_check = peewee.IntegerField()
        revined_user = peewee.CharField()

    class vine_page_test(MySQLModel):
        username = peewee.CharField()
        date = peewee.DateField()
        user_id = peewee.CharField()
        post_count = peewee.IntegerField()
        follower_count = peewee.IntegerField()
        following_count = peewee.IntegerField()
        loop_count = peewee.IntegerField()
        like_count = peewee.IntegerField()



    mysql_db.connect()


    for each in user_data_list:
        try:
            peewee.DeleteQuery(vine_page_test).where((vine_page_test.user_id == each['user_id']) &
            (vine_page_test.date == each['date'])).execute()

        finally:
            peewee.InsertQuery(vine_page_test, each).execute()

    for each in post_data_list:
        try:
            peewee.DeleteQuery(vine_post_test).where(vine_post_test.video_link == each['video_link']).execute()

        finally:
            peewee.InsertQuery(vine_post_test, each).execute()




if __name__ == "__main__":
    user_name = "vanity/kf"     # Insert the specific brand name here
    # res = getJSON(user_name)
    # user_data_list = get_user_data(res)
    # post_data_list = get_post_data(res)
    # connection(user_data_list,post_data_list)
    try:
        response = urllib2.urlopen('https://vine.co/api/users/profiles/' + user_name)
        res = json.load(response)
        user_data_list = get_user_data(res)
        post_data_list = get_post_data(res)
        connection(user_data_list,post_data_list)
    except urllib2.HTTPError as e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
    except urllib2.URLError as e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason


