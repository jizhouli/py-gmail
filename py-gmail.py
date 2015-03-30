#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Justin<justinli.ljt@gmail.com>
# 2015-03-30

import email.Header
import email.MIMEBase
import email.MIMEMultipart
import email.MIMEText

import smtplib
import socket
import string
import time
import traceback

class PyGmail(object):
    '''
    a handful email sending lib for gmail
    '''
    def __init__(self, name="My Gmail Proxy"):
        # email server config
        self.name = name
        self.smtp_server = ''
        self.smtp_port = 0

        # sender config
        self.from_account = ''
        self.from_password = ''

        # receiver config
        self.to = ''
        self.cc = ''
        self.bcc = ''

        # email config
        self.subject = ''
        self.content = ''
        self.subtype = ''
        self.attachfile = ''

    def conf(self, smtp_server, smtp_port, timeout=60):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.timeout = timeout

    def set_from(self, account, password):
        self.from_account = account
        self.from_password = password

    def set_to(self, to, cc='', bcc=''):
        self.to = to
        self.cc = cc
        self.bcc = bcc

    def set_mail(self, subject, content, subtype='', attachfile=''):
        self.subject = subject
        self.content = content
        self.subtype = subtype
        self.attachfile = attachfile

    def send(self):
        print 'sending start'
        # set socket timeout
        socket.setdefaulttimeout(self.timeout)

        # construct email message
        msg = email.Message.Message()
        msg['to'] = self.to
        msg['cc'] = self.cc
        msg['date'] = time.ctime()
        msg['subject'] = email.Header.Header(self.subject,'utf8')
        if self.subtype:
            body=email.MIMEText.MIMEText(self.content, _subtype=self.subtype, _charset='utf8')
        else:
            body=email.MIMEText.MIMEText(self.content, _charset='utf8')

        # add attach file
        if self.attachfile != "" :
            attach = email.MIMEMultipart.MIMEMultipart()
            attach.attach(body)
            
            contype = 'application/octet-stream'
            maintype, subtype = contype.split('/', 1)

            pf=open(self.attachfile,'rb')
            file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
            file_msg.set_payload(pf.read( ))
            pf.close()

            email.Encoders.encode_base64(file_msg)
            file_msg.add_header('Content-Disposition', 'attachment', filename=self.attachfile[self.attachfile.rfind('/')+1:] )
            attach.attach(file_msg)

        try:
            server = smtplib.SMTP(self.smtp_server,self.smtp_port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.from_account,self.from_password)

            if self.attachfile == "":
                server.sendmail(
                        self.from_account,
                        string.split(recp+';'+cc+';'+self.bcc,";"),
                        msg.as_string()[:-1]+body.as_string(),
                        )
            else:
                server.sendmail(self.from_account,
                        string.split(recp+';'+cc+';'+self.bcc,";"),
                        msg.as_string()[:-1]+attach.as_string(),
                        )
            print '%s send to %s ok' % (self.name, self.to)
        except Exception, e:
            print traceback.format_exc()
            print '%s send to %s error \n%s' % (self.name, self.to, str(e))
        print 'end'

    def __str__(self):
        s = ''
        s += '[%s] dump\n' % self.name
        s += '-'*40 + '\n'
        s += '\tsmtp: %s:%s\n' % (self.smtp_server, self.smtp_port)
        s += '\tfrom: <%s>\n' % self.from_account
        s += '\tto: <%s>\n' % self.to
        s += '\tcc: <%s>\n' % self.cc
        s += '\tbcc: <%s>\n' % self.bcc
        s += '\tsubject: %s\n' % self.subject
        s += '\tcontent: %s\n' % self.content
        s += '\tattachment: "%s"\n' % self.attachfile
        s += '-'*40
        return s

if __name__ == '__main__':
    gmail = PyGmail("Justin's Baymax")
    gmail.conf(smtp_server="smtp.gmail.com", smtp_port=587, timeout=60)
    gmail.set_from(account="xxxx@gmail.com", password="xxxxxxxx")
    gmail.set_to(to='bbbb@xxxx.com', cc='cccc@xxxx.com', bcc='dddd@xxxx.com')
    gmail.set_mail(
            subject='这是一封测试邮件',
            content='该测试邮件包含附件信息',
            attachfile='README.md',
            )
    print gmail
    gmail.send()

