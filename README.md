# py-gmail
a handful gmail sender library

### Usage
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

----

*powered by Mou*