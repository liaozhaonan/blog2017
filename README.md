zhaonan.com 网站源码
=================

# 概述
zhaonan\_blog 是一个基于  **Django1.8**  跟  **Bootstrap3**  开发的 **博客系统**,
实现了一个博客完整的功能。https://liaozhaonan.heroku.com 就是基于zhaonan\_blog 搭建的。
# 功能
1. 文章,分类,专栏, 标签的添加，删除，修改以及文章按年度进行归档等。
2. 首页支持最新文章列表、热门文章列表、推荐文章**轮播**等。
3. 博客页支持根据关键词**搜索文章**, 支持显示随机色彩的**标签**，拥有一个非常酷炫的便签云。
4. 支持**评论**及**评论回复**，实现了一个独立的评论系统。
5. 支持**留言板**功能。
6. 支持留言表单、评论表单和评论回复表单的**异步提交**功能
7. 支持文章列表和评论列表的**分页**和**Ajax异步加载**功能。
9. 使用bootstrap3框架，很好地支持**移动设备浏览**。

# Demo
https://liaozhaonan.herokuapp.com

# 安装运行
安装virtualenv:

    sudo pip install virtualenv

创建并激活虚拟环境 :

    virtualenv www --python==python3
    cd www
    source bin/active

下载代码,切换目录 :
    
    git clone https://github.com/liaozhaonan/blog2017
    cd blog2017

首先安装相关python包:

    pip install -r requirements.txt

配置setting.py :

    使用文本编辑器打开 ./project/setting.py, 设置其中的:

       PAGE_NUM 每页显示文章数
       EMAIL_HOST(你用的邮箱的smtp)
       EMAIL_PORT(smtp端口)
       DEFAULT_FROM_EMAIL(邮件发送人名称)

    使用文本编辑器打开 ./project/local_setting.py, 设置其中的:

       EMAIL_HOST_USER(你的邮箱的用户名)
       EMAIL_HOST_PASSWORD(你的邮箱密码)

**注意**：如果想用使用ssl的邮箱（比如qq邮箱），请安装django-smtp-ssl
  （详见https://github.com/bancek/django-smtp-ssl）

```
    # 分页配置
    PAGE_NUM = 10

    # email配置
    EMAIL_HOST = ''                      # SMTP地址 例如: smtp.163.com
    EMAIL_PORT = 25                      # SMTP端口 例如: 25
    EMAIL_USE_TLS = True                 # 与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认false
    DEFAULT_FROM_EMAIL = ''              # 发件人名称，默认为EMAIL_HOST_USER
    EMAIL_HOST_USER = local_settings.email_address       # 帐号
    EMAIL_HOST_PASSWORD = local_settings.email_password  # 密码

    # local_setting.py
    email_address = ''                   # 我自己的邮箱 例如: xxxxxx@163.com
    email_password = ''                  # 我的邮箱密码 例如  xxxxxxxxx

    
    # 网站通知/欢迎内容配置
    NOTICE = "欢迎来到xx的博客"
```

    修改“关于”页面(about.html)中的相关信息,或将其修订为你自己的风格。

初始化数据库 :

    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    
运行 :
    
    python manage.py runserver
    
    
# 生产环境部署
	
使用gunicorn部署:
	
	gunicorn project.wsgi --log-file -
    
**环境变量**:
其中：EMAIL_HOST，EMAIL_PORT，EMAIL_HOST_USER，EMAIL_HOST_PASSWORD是必须的，如果不指定，用户注册不了

	NOTICE  首页显示的通知/欢迎消息
	
	EMAIL_BACKEND  email的引擎，默认是django.core.mail.backends.smtp.EmailBackend
    (如果想支持qq邮箱请使用django_smtp_ssl.SSLEmailBackend)
	EMAIL_HOST  SMTP地址
	EMAIL_PORT  SMTP端口
	EMAIL_HOST_USER  邮箱名称
	EMAIL_HOST_PASSWORD  邮箱密码
	EMAIL_SUBJECT_PREFIX  邮件Subject-line前缀
	
运行后，默认管理员用户名为 admin，密码为 password ， 请登录 http://your-domain/admin 更改密码。

# 接下来该干什么？
在浏览器中输入 http://127.0.0.1:8000/admin
输入前面初始化数据库时的用户名密码。
后台中，可以通过专栏、标签、文章、评论、评论回复、留言、留言回复等创建及管理相关内容


