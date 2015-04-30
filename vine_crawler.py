'''
This script is writen by Bowei Zhang at 3/31/2015 for scraping vine data and
put them into MySQL database
'''
import peewee
import MySQLdb
import urllib2
import json
import time

from time import gmtime, strftime
import sqlite3

# Get Vine account profile information from previous JSON file
def get_user_data(res):
    user_data = {}
    user_data['username'] = (res['data']['username'].encode('utf-8'))
    user_data['date'] = (time.strftime('%Y-%m-%d %H:%M:%S'))
    user_data['user_id'] = (str(res['data']['userId']))
    user_data['post_count'] = (res['data']['postCount'])
    user_data['follower_count'] = (res['data']['followerCount'])
    user_data['following_count'] = (res['data']['followingCount'])
    user_data['loop_count'] = (res['data']['loopCount'])
    user_data['like_count'] = (res['data']['likeCount'])
    # print user_data
    user_data_list = []
    user_data_list.append(user_data)
    # print user_data_list
    # for user_data in user_data_list:
    #     print user_data['username']
    return user_data_list

# Get each post information for a specific Vine account from timeline JSON file
def get_post_data(res):
    user_id = res['data']['userId']
    #print user_id,user_name
    post_count = res['data']['postCount']
    #print post_count
    # user_name = res['data']['username'].encode('utf-8')
    #print user_name

    new_url = 'https://vine.co/api/timelines/users/' + str(user_id) + '?size=' + str(post_count)
    response2 = urllib2.urlopen(new_url)
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
            post_data['revined_user'] = user_id
            # post_data['revined_user'] = (record[x]['username'].encode('utf-8'))
            post_data_list.append(post_data)
            post_data = {}
    # print post_data_list
    return post_data_list

def connect_db():
    return sqlite3.connect('database/flaskr.db')

# Connecting MySQL and insert Vine data into the databases
# def connection(user_data_list, post_data_list):
def connection(user_data_list, post_data_list):
    # connect to sqlite
    db = connect_db()

    for user_data in user_data_list:
        username = user_data['username']
        date = user_data['date']
        user_id = user_data['user_id']
        post_count = user_data['post_count']
        follower_count = user_data['follower_count']
        following_count = user_data['following_count']
        loop_count = user_data['loop_count']
        like_count = user_data['like_count']
        db.execute('INSERT INTO vine_page_test (username, date, user_id, post_count, follower_count, following_count, loop_count, like_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [username, date, user_id, post_count, follower_count, following_count, loop_count, like_count])
        db.commit()

    for post_data in post_data_list:
        username2 = post_data['username']
        created = post_data['created']
        likes = post_data['likes']
        reposts = post_data['reposts']
        loops = post_data['loops']
        comments = post_data['comments']
        description = post_data['description']
        video_link = post_data['video_link']
        revine_check = post_data['revine_check']
        revined_user = post_data['revined_user']
        # db.execute('insert into vine_post_test (username, created, likes, reposts, loops, comments, description, video_link, revine_check, revined_user) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [username2, created, likes, reposts, loops, comments, description, video_link, revine_check, revined_user])
        db.execute('INSERT OR REPLACE INTO vine_post_test (username, created, likes, reposts, loops, comments, description, video_link, revine_check, revined_user) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [username2, created, likes, reposts, loops, comments, description, video_link, revine_check, revined_user])
        db.commit()

    # close the connect
    if db is not None:
        db.close()

if __name__ == "__main__":
    user_name = "vanity/cocacola"     # Insert the specific brand name here
    print 'At ' + strftime("%Y-%m-%d %H:%M:%S", gmtime())
    try:
        response = urllib2.urlopen('https://vine.co/api/users/profiles/' + user_name)
        res = json.load(response)
        user_data_list = get_user_data(res)
        post_data_list = get_post_data(res)
        connection(user_data_list, post_data_list)
        print 'Success!'
    except urllib2.HTTPError as e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
    except urllib2.URLError as e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason


