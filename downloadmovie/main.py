import guiClass

#获取guiClass.py文件内定义的GUI类
app = guiClass.GUI()

#对GUI类初始化
app.version = 'Video Downloader Beta 0.9.4 r(20161221)' #app的版本
app.appVer = 0.94
app.appUrl = 'http://evilcult.github.io/Video-Downloader'   #app连接
app.gitUrl = 'https://github.com/EvilCult/Video-Downloader' #git源码连接
app.feedUrl = 'https://github.com/EvilCult/Video-Downloader/issues' #问题解决记录

app.run()