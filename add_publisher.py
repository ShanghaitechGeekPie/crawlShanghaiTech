# -*- coding: utf-8 -*-
# 添加指定公众号到爬虫数据库
# 需要在mysql数据库中先手动添加公众号的publisher_id
# insert into publisher_list set publisher_id="shtech2013"

# 导入包
from wechatsogou.tools import *
from wechatsogou import *
from PIL import Image
import datetime
import time
import sys,locale
import logging
import logging.config

# 搜索API实例
wechats = WechatSogouApi()

#数据库实例
mysql = mysql('publisher_list')
add_list = mysql.find(0)
succ_count = 0
for add_item in add_list :
    try:
        print(add_item)
        if add_item['publisher_id']:
            print("add by publisher_id")
            mysql.where_sql = "publisher_id ='" + add_item['publisher_id'] + "'"
            mp_data = mysql.table('publisher_info').find(1)
            if not mp_data :
                wechat_info = wechats.get_gzh_info(add_item['publisher_id'])
                time.sleep(1)
                #print(wechat_info)
                if(wechat_info != ""):
                    mysql.table('publisher_info').add({'name':wechat_info['name'],
                                                'publisher_id':wechat_info['wechatid'],
                                                'company':wechat_info['renzhen'],
                                                'description':wechat_info['jieshao'],
                                                'logo_url':wechat_info['img'],
                                                'qr_url': wechat_info['qrcode'],
                                                'newsfeed_url': wechat_info['url'],
                                                'last_push_id': 0,
                                                'create_time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))})
            else:
                print(u"已经存在的公众号")
        elif add_item['name']:
            #获取对应信息
            print("add by name")
            wechat_infos = wechats.search_gzh_info(add_item['name'].encode('utf8'))
            time.sleep(1)
            #print(wechat_infos)
            for wx_item in wechat_infos :
                #公众号数据写入数据库
                #搜索一下是否已经存在
                print(wx_item['name'])
                mysql.where_sql = "publisher_id ='" + wx_item['wechatid'] + "'"
                print(mysql.where_sql)
                mp_data = mysql.table('publisher_info').find(1)
                if not mp_data :
                    print(wx_item['name'].decode("utf-8"))
                    mysql.table('publisher_info').add({ 'name':wx_item['name'],
                                'publisher_id':wx_item['wechatid'],
                                'company':wx_item['renzhen'],
                                'description':wx_item['jieshao'],
                                'logo_url':wx_item['img'],
                                'qr_url': wx_item['qrcode'],
                                'newsfeed_url': wx_item['url'],
                                'last_push_id': 0,
                                'create_time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))})
                else:
                    print(u"已经存在的公众号")
                
        #删除已添加项
        mysql.table('publisher_list').where({'_id':add_item['_id']}).delete()
    except:
        print(u"出错，继续")
        continue


print("success")

    

