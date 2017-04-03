# -*- coding: utf-8 -*-
#更新文章阅读数据，目前一篇文章只监控24小时

# 导入包
from wechatsogou.tools import *
from wechatsogou import *
from PIL import Image
import datetime
import time
import logging
import logging.config


# 搜索API实例
wechats = WechatSogouApi()

#如果想使用外部cookie，主要是为了实现搜狗微信登录状态
#你需要安装chrom浏览器，然后给浏览器安装EditThisCooke这个插件
#1、使用Chrom浏览器登录搜狗微信
#2、使用EditThisCooke插件复制当前Cookie信息
#3、把cookie信息复制到代码目录下的cookies.txt文件
#4、开启下面这行语句
#wechats = WechatSogouApi(cookies_file={'file_name':'cookies.txt'})  #使用外部cookie


#数据库实例
mysql.order_sql = "order by _id desc"
mysql = mysql('publisher_info')

#循环获取数据库中所有公众号
publisher_list = mysql.find(0)


now_time = datetime.datetime.now()
yes_time = now_time + datetime.timedelta(days=-10) #只更新1天之内的数据，可以修改days=-2就是2天
succ_count = 1

for item in publisher_list:
    try:
        #为了效率，首先查看该公众号是否有24小时之内的文章
        print(item['publisher_id'])
        mysql.where_sql = "publisher_id=%d and date_time >'%s'" %(item['publisher_id'],yes_time)
        print(mysql.where_sql)
        newsfeed_time = mysql.table('newsfeed').find(1)
        if not newsfeed_time :
            continue

        print(item['name'])
        #print('1')
        newsfeed_url = ""
        if item.has_key('newsfeed_url') :
            newsfeed_url = item['newsfeed_url']
        else :
            wechat_info = wechats.get_gzh_info(item['publisher_id'])
            if not wechat_info.has_key('url') :
                continue
            newsfeed_url = wechat_info['url'];

        #print('2')
        newsfeed_list = wechats.get_gzh_message(url=newsfeed_url)
        if u'链接已过期' in newsfeed_list:
            wechat_info = wechats.get_gzh_info(item['publisher_id'])
            print(wechat_info)
            if not wechat_info.has_key('url') :
                continue
            print('guo qi sz chong xin huo qu success')
            newsfeed_url = wechat_info['url'];
            newsfeed_list = wechats.get_gzh_message(url=newsfeed_url)
            mysql.where_sql = " _id=%s" %(item['_id'])
            mysql.table('publisher_info').save({'newsfeed_url':wechat_info['url'],'logo_url':wechat_info['img'],'qr_url':wechat_info['qrcode']})
        #type==49表示是图文消息
        # print('3')
        for newsfeed_item in newsfeed_list:
            #只监控24小时之内的文章
            if(newsfeed_item['datetime'] < time.mktime(yes_time.timetuple())):
                break

            if newsfeed_item['type'] == '49':
                #获取文章数据
                time.sleep(0.5)
                article_info = wechats.deal_article(url=newsfeed_item['content_url'])
                mysql.where_sql = "publisher_id=%d and push_id=%d and msg_index=%d" %(item['publisher_id'],newsfeed_item['push_id'],newsfeed_item['main'])
                print(mysql.where_sql)
                # print('8')
                newsfeed_data = mysql.table('newsfeed').find(1)
                if not newsfeed_data :
                    print(u"公众号有新文章，请执行fetch_newsfeed.py进行抓取")
                    continue

                #获取当前的数据
                print(succ_count)
                succ_count += 1
                read_count = newsfeed_data['read_count']
                like_count = newsfeed_data['like_count']
                comment_count = newsfeed_data['comment_count']
                print "%d new_read:%d  new_like:%d read:%d  like:%d" %(newsfeed_data['_id'], article_info['comment']['read_num'],article_info['comment']['like_num'],read_count,like_count)
                #把文章写入数据库
                mysql.table('newsfeed_stats').add({'newsfeed_id':newsfeed_data['_id'],
                                                'create_time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),
                                                'read_count':int(article_info['comment']['read_num'])-read_count,
                                                'like_count':int(article_info['comment']['like_num'])-like_count,
                                                'comment_count': int(article_info['comment']['elected_comment_total_cnt'])-comment_count})
                print('5')
            #更新文章总阅读数
            mysql.where_sql = " _id=%s" %(newsfeed_data['_id'])
            mysql.table('newsfeed').save({'read_count':int(article_info['comment']['read_num']),
                                                                            'like_count':int(article_info['comment']['like_num']),
                                                                            'comment_count': int(article_info['comment']['elected_comment_total_cnt'])})
    except KeyboardInterrupt:
        break
    except: #如果不想因为错误使程序退出，可以开启这两句代码
        print u"出错，继续"
        continue
                
print('success')

