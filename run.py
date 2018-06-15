#coding=utf-8
 
"""
 
codeManager，自动把本机指定目录下的文件夹打成压缩包，并且作为附件发邮件给指定邮箱，作为备份
2016-06-29 by ruansz
 
"""
 
# 解决乱码问题
import sys  
reload(sys)  
SYS_ENCODING = 'cp936'  # 定义系统编码
sys.setdefaultencoding(SYS_ENCODING)  # 设置默认编码
 
import email.MIMEBase
import time
import urllib2

# 自定义包导入
from emailManager import email_manager
 
# 定义一个log函数
def log(msg):
    print time.strftime('%Y-%m-%d %H:%M:%S'), ': ', msg
 

#判断获取的Ip 和本地存储的IP是否一致,如果以返回0001 否则就返回0002
def readorwirtefile(file,ip):
    str = '0001';
    f = open(file,'r')
    print f.readline()
    if ip != f.readline():
        wf = open(file,'w+')
        wf.write(ip)
        wf.close()
        str = '0002'
    f.close()
    return str
    


# run
if __name__ == '__main__':
    strHtml = urllib2.urlopen('http://2018.ip138.com/ic.asp').read()
    print strHtml
    ip = strHtml.split("[")[1]
    ip = strHtml.split("]")[0]
    #ip = '192.168.1.101'
    status = readorwirtefile("tmp.txt",ip)
    # 只有IP发生变化的时候才发送邮件进行告知
    if status == '0002':
        
        print ip
        strHtml = strHtml.split("<center>")[1];
        strHtml = strHtml.split("</center>")[0];
        print strHtml
        log(u'进入run函数')
     
     
        log(u'开始读取压缩配置参数')
        # 定义配置参数
        # 1、压缩配置
        timestr = time.strftime('%Y%m%d%H%M%S')   # 生成日期时间字符串，作为压缩文件的版本号
    #     folder = ['/home/jenkins/codescan/fireline/report','/home/jenkins/codescan/godeyes/report']   # 压缩目标文件夹
    #     target = ['/home/jenkins/codescan/fireline/report/mod1_v'+timestr+r'.zip','/home/jenkins/codescan/godeyes/report/mod2_v'+timestr+r'.zip']   # 压缩后的名称
     
        target = ['E:/testzip/1.txt']   # 压缩后的名称
     
    #     log(u'压缩源文件夹：' + folder)
    #     log(u'压缩输出路径：' + target)
    #  
        log(u'开始读取邮件发送配置参数')
        # 2、发送邮件配置
        mail_cfg = {
            # 邮箱登录设置，使用SMTP登录
            'server_username': 'frommail', 
            'server_pwd': 'password',
     
            # 邮件内容设置
            'msg_to': ['tomail'],  # 可以在此添加收件人
            'msg_subject': u'最新IP',
            'msg_date': email.Utils.formatdate(),
            'msg_content': u""+strHtml,
     
            # 附件
            #'attach_file': target[0]
            'attach_file': target
            }
        log(u'读取邮件发送配置参数：')
        log(u'server_username：' + str(mail_cfg.get('server_username')))
        #log(u'server_pwd：' + str(mail_cfg.get('server_pwd')))
        log(u'msg_to：' + str(mail_cfg.get('msg_to')))
        log(u'msg_subject：' + str(mail_cfg.get('msg_subject')))
        log(u'msg_date：' + str(mail_cfg.get('msg_date')))
        log(u'msg_content：' + str(mail_cfg.get('msg_content')))
        #不发送附件
        #log(u'attach_file：' + str(mail_cfg.get('attach_file')))
        #/html/body/center
     
        # 实例化manager对象
        log(u'开始创建EmailManager')
        email_manager = email_manager(**mail_cfg)
        log(u'开始发送邮件')
        email_manager.run()
        log(u'发送完成')
        log(u'程序结束')
 