# coding:utf8
import re
import os
import sys

from api import *
from configure import *
from db import *

import requests

# 设置系统默认编码模式
reload(sys)
sys.setdefaultencoding('utf-8')


def verify_url(url, url_type):
    pattern = re.compile(r'http:\/\/music\.163\.com\/#\/' + url_type + '\?id=[0-9]+')  # 判断输入的url符合规则
    pattern2 = re.compile(r'http:\/\/music\.163\.com\/#\/' + url_type + '\?id=[0-9]+[^\d]+')  # 如果正常url后面跟有非数字的字符>
    if re.match(pattern, url) and not re.match(pattern2, url):
        return True
    else:
        return False

def url_split(url):
    pattern = re.compile(r'=')
    return re.split(pattern, url)[1]


def write_db(i):
    '''
    song = Song(
        song_id=i['id'],
        title=i['title'],
        artist=i['artist'],
        album=i['album'],
        cover='http://static.guoduhao.cn/nyanfm/cover/' +
        i['artist'] + ' - ' + i['title'] + '.jpg!nyanfm.cover',
        mp3='http://static.guoduhao.cn/nyanfm/mp3/' +
        i['artist'] + ' - ' + i['title'] + '.mp3',
        ogg='http://static.guoduhao.cn/nyanfm/mp3/' +
        i['artist'] + ' - ' + i['title'] + '.mp3'
    )
    try:
        song.save()
        print '**db succeed**'
    except:
        print '!!!db error!!!'
    '''
    r = requests.post(nyanfm_url,
    json={
        'song_id':i['id'],
        'title':i['title'],
        'artist':i['artist'],
        'album':i['album'],
        'cover':'http://static.guoduhao.cn/nyanfm/cover/' + i['artist'] + ' - ' + i['title'] + '.jpg!nyanfm.cover',
        'mp3':'http://static.guoduhao.cn/nyanfm/mp3/' + i['artist'] + ' - ' + i['title'] + '.mp3',
        'lyric':i['lyric'],
        'key':nyanfm_apikey
    })
    if r.json()['code'] == 0:
        print 'Data writen'
    else:
        print 'Write data error'
    return True


def play_list(url):
    wget_prefix = "wget --header='Connection: keep-alive' "\
        + "--header='Pragma: no-cache'"\
        + "--header='Cache-Control: no-cache'"\
        + "--header='Upgrade-Insecure-Requests: 1'"\
        + "--header='User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3070.0 Safari/537.36'"\
        + "--header='Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'"\
        + "--header='Accept-Encoding: gzip, deflate' --header='Accept-Language: zh-CN,zh;q=0.8,en;q=0.6' \'"
    ne = NetEase()
    url_valid = verify_url(url, 'playlist')
    id_legal = True
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
                    'id': i['id'],
                    'title': i['name'],
                    'artist': i['artists'][0]['name'],
                    'album': i['album']['name'],
                    'cover_url': i['album']['picUrl'],
                    'mp3_url': ne.songs_detail_new_api([i['id']])[0]['url'],
                    'lyric': ne.song_lyric(i['id']),
                }
                song_list.append(song_item)
                mp3_path_name = mp3_path + \
                    i['artists'][0]['name'] + ' - ' + i['name'] + '.mp3'
                cover_path_name = cover_path + \
                    i['artists'][0]['name'] + ' - ' + i['name'] + '.jpg'
                print '------------'
                print mp3_path_name
                if os.path.exists(mp3_path_name) == False and ne.songs_detail_new_api([i['id']])[0]['url'] != None:
                    try:
                        os.system(wget_prefix + convert_url(ne.songs_detail_new_api([i['id']])[0]['url']) + '\' -O \'' + mp3_path_name + '\'')
                        os.system(wget_prefix + i['album']['picUrl'] + '\' -O \'' + cover_path_name + '\'')
                        #write_file(song_item)
                        write_db(song_item)
                        print '**downloaded.**'
                    except Exception, e:
                        print e
                        print '!!!error while download.!!!'
                elif ne.songs_detail_new_api([i['id']])[0]['url'] == None:
                    print '!!!resouce not found!!!'
                else:
                    print 'exists, skip'
        except:
            id_legal = False
            valid = False
            return False
        print 'Done, exiting.'
        return True

def convert_url(url):
    #new_url = 'http://' + m10_ip + '/' + url.split('http://')[1]
    return url

play_list(url)
