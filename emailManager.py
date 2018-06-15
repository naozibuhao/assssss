# -*- coding: utf-8 -*-  
 
'''
发送邮件
'''
 
import smtplib  
import email.MIMEMultipart
import email.MIMEText
import email.MIMEBase
import os.path  
import mimetypes
import os  
from os.path import join, getsize    
import traceback
 
# 解决乱码问题
import sys  
reload(sys)  
SYS_ENCODING = 'cp936'  # 定义系统编码
sys.setdefaultencoding(SYS_ENCODING)  # 设置默认编码
 
class email_manager:
    '''
    send email to the given email address automatically
    '''
 
    def __init__(self, **kw):
        ' 构造函数 '
        self.kw = kw
 
        self.smtp_server = "smtp.163.com"
        self.MAX_FILE_SIZE = 10 * 1024 * 1024 # 10M
 
    def run(self):
        # 总入口
        try:
            # 初始化
            self.__my_init()
            # 登录SMTP服务器，验证授权
            server = self.get_login_server()
            # 生成邮件主体内容
            main_msg = self.get_main_msg()
            # 生成邮件附件内容
            #file_msg = self.get_attach_file_msg()
            
            
            for x in range(len(self.attach_file)):
                file_msg = self.get_attach_file_msg_filename(self.attach_file[x])
                if file_msg is not None:
                    main_msg.attach(file_msg)
 
            # 得到格式化后的完整文本  
            fullText = main_msg.as_string()  
 
            # 发送邮件
            server.sendmail(self.msg_from, self.receiver, fullText)  
 
        except Exception, e:
            print e
 
            exstr = traceback.format_exc()
            print exstr
 
            server.quit()
            exit()
 
    def get_main_msg(self):
        ' 生成邮件主体内容 '
        # 构造MIMEMultipart对象做为根容器  
        main_msg = email.MIMEMultipart.MIMEMultipart()  
 
        # 构造MIMEText对象做为邮件显示内容并附加到根容器  
        text_msg = email.MIMEText.MIMEText(self.msg_content, _charset="utf-8")  
        main_msg.attach(text_msg)  
 
        # 设置根容器属性  
        main_msg['From'] = self.msg_from  
        main_msg['To'] = self.msg_to  
        main_msg['Subject'] = self.msg_subject
        main_msg['Date'] = self.msg_date
 
        return main_msg
 
    def get_attach_file_msg(self):
        ' 生成邮件附件内容 '
        if self.attach_file is not None and self.attach_file != "":
            try:
#                 self.validate_file_size()
#                 self.validate_file_size_by_name()
                data = open(self.attach_file, 'rb')  
                ctype,encoding = mimetypes.guess_type(self.attach_file)  
                if ctype is None or encoding is not None:  
                    ctype = 'application/octet-stream'  
                maintype,subtype = ctype.split('/',1)  
                file_msg = email.MIMEBase.MIMEBase(maintype, subtype)  
                file_msg.set_payload(data.read())  
                data.close()  
 
                email.Encoders.encode_base64(file_msg) #把附件编码  
 
                ## 设置附件头  
                basename = os.path.basename(self.attach_file)  
                file_msg.add_header('Content-Disposition','attachment', filename = basename) #修改邮件头
 
                return file_msg
            except Exception, e:
                print '108  : '+str(e)
                return None
 
        else:
            return None
 
 
    def get_attach_file_msg_filename(self,filenamepath):
        ' 生成邮件附件内容 '
        if filenamepath is not None and filenamepath != "":
            try:
#                 self.validate_file_size()
                self.validate_file_size_by_name(filenamepath)
                data = open(filenamepath, 'rb')  
                ctype,encoding = mimetypes.guess_type(filenamepath)  
                if ctype is None or encoding is not None:  
                    ctype = 'application/octet-stream'  
                maintype,subtype = ctype.split('/',1)  
                file_msg = email.MIMEBase.MIMEBase(maintype, subtype)  
                file_msg.set_payload(data.read())  
                data.close()  
 
                email.Encoders.encode_base64(file_msg) #把附件编码  
 
                ## 设置附件头  
                basename = os.path.basename(filenamepath)  
                file_msg.add_header('Content-Disposition','attachment', filename = basename) #修改邮件头
 
                return file_msg
            except Exception, e:
                print e
                return None
 
        else:
            return None
 
 
    def get_login_server(self):
        ' 登录SMTP服务器，验证授权信息 '
        server = smtplib.SMTP(self.smtp_server)
        print u'登录成功'
        try:
            server.ehlo('HELO')  
            server.login(self.server_username, self.server_pwd) #仅smtp服务器需要验证时
        except Exception ,es:
            print str(es)
        return server  
 
    def validate_file_size(self):
        ' 验证文件大小是否合法 '
        if getsize(self.attach_file) > self.MAX_FILE_SIZE:
            raise Exception(u'附件过大，上传失败')
    def validate_file_size_by_name(self,filenamepath):
        ' 验证文件大小是否合法 '
        if getsize(filenamepath) > self.MAX_FILE_SIZE:
            raise Exception(u'附件过大，上传失败')
    def __my_init(self):
        ' 配置初始化 '
        # 邮箱登录设置
        self.server_username = self.__get_cfg('server_username')
        self.server_pwd = self.__get_cfg('server_pwd')
 
        # 邮件内容设置
        self.receiver = self.__get_cfg('msg_to')
 
        self.msg_from = self.server_username
        self.msg_to = ','.join(self.__get_cfg('msg_to'))
        self.msg_subject = self.__get_cfg('msg_subject')
        self.msg_date = self.__get_cfg('msg_date')
        self.msg_content = self.__get_cfg('msg_content')
 
        # 附件
        self.attach_file = self.__get_cfg('attach_file', throw=False)
 
    def __get_cfg(self, key, throw=True):
        ' 根据key从**kw中取得相应的配置内容 '
        cfg = self.kw.get(key)
        if throw == True and (cfg is None or cfg == ''):
            raise Exception(unicode("配置不能为空！", 'utf-8'))
 
        return cfg
 
 
