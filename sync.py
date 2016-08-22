#coding:utf8
import re
import os
import sys

from api import *
from configure import *

#设置系统默认编码模式
reload(sys)
sys.setdefaultencoding('utf-8')

def verify_url(url,url_type):
    pattern = re.compile(r'http:\/\/music\.163\.com\/#\/' + url_type + '\?id=[0-9]+')#判断输入的url符合规则
    pattern2 = re.compile(r'http:\/\/music\.163\.com\/#\/' + url_type + '\?id=[0-9]+[^\d]+')#如果正常url后面跟有非数字的字符>
    if re.match(pattern,url) and not re.match(pattern2,url):
        return True
    else:
        return False

def url_split(url):
    pattern = re.compile(r'=')
    return re.split(pattern,url)[1]

def play_list(url):
    ne = NetEase()
    url_valid = verify_url(url, 'playlist')
    id_legal =True
    if url_valid:
        playlist_id = url_split(url)
        valid = True
        url_legal = True
    else:
        valid = False
        url_legal = False
        playlist_id = 0
    song_list = []
    if valid and url_legal:
        try:
            for i in ne.playlist_detail(playlist_id):
                song_item = {
                        'id':i['id'],
                        'title':i['name'],
                        'artist':i['artists'][0]['name'],
                        'album':i['album']['name'],
                        'cover_url':i['album']['picUrl'],
                        'mp3_url':ne.songs_detail_new_api([i['id']])[0]['url']
                        }
                song_list.append(song_item)
                mp3_path_name = mp3_path + i['artists'][0]['name'] + ' - ' + i['name'] + '.mp3'
                cover_path_name = cover_path + i['artists'][0]['name'] + ' - ' + i['name'] + '.jpg'
                print mp3_path_name
                print ne.songs_detail_new_api([i['id']])[0]['url']
                if  os.path.exists(mp3_path_name) == False and ne.songs_detail_new_api([i['id']])[0]['url'] != None:
                    try:
                        os.system('wget \'' + convert_url(ne.songs_detail_new_api([i['id']])[0]['url']) + '\' -O \'' + mp3_path_name + '\'')
                        os.system('wget \'' + i['album']['picUrl'] + '\' -O \'' + cover_path_name + '\'')
                        write_file(song_item)
                        print 'downloaded.'
                    except:
                        print 'error while download.'
                elif ne.songs_detail_new_api([i['id']])[0]['url'] == None:
                    print 'resouce not found'
                else:
                    print 'already exists, skip'
        except:
            id_legal = False
            valid = False
            return False
        print 'Done, exiting.'
        return True

def write_file(i):
    jswrite = "{title:'"+ i['title'] +"',artist:'"+ i['artist'] +"',album:'"+ i['album'] +"',cover:'http://nyandn.b0.upaiyun.com/cover/"+ i['artist'] + ' - ' + i['title'] + ".jpg',mp3:'http://nyandn.b0.upaiyun.com/mp3/"+ i['artist'] + ' - ' + i['title'] + ".mp3',ogg:'http://nyandn.b0.upaiyun.com/mp3/"+ i['artist'] + ' - ' + i['title']  +".mp3',},"
    print (jswrite)
    filein = js_path
    fileout = filein
    f = open(filein,'r')
    filedata = f.read()
    f.close()
    newdata = filedata.replace("//ENDOFLIST","//ENDOFLIST\n"+jswrite)
    f = open(fileout,'w')
    f.write(newdata)
    f.close()
    return True

def convert_url(url):
    new_url = 'http://' + m10_ip + '/' + url.split('http://')[1]
    return new_url


play_list(url)



