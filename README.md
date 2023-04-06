
## 简介
本项目主要是为了管理EPEDAPro发布所用脚本及程序发布目录，但也包含epkernel目录与发布报告等其他文件。
## 文件
- pyScripts:发布程序脚本
- releaseIndex.txt:EPEDAPro程序发布目录
- releaseLog.md:发布目录修改日志

## 使用
关于发布脚本的使用，具体见[发布流程](https://github.com/wlawlawlawla/releaseIndex/blob/main/%E5%8F%91%E5%B8%83%E6%B5%81%E7%A8%8B.docx)。

发布流程：

1， 确认是否有新版本的CAMSDK与CAMGuide且本次发布版本是否需要使用；

SDK使用：将sdk中的文件复制到EDAPro项目trunk目录下EPEDAPro文件夹路径下。

2， 向EDAPro开发人员确认是否有代码更新及上传情况，是否有文件需要增加删除修改等；

3， 通过SVN拉取代码至最新版本；

4， 编译EPEDAPro项目；

5， 文件打包；

![程序截图](https://github.com/wlawlawlawla/releaseIndex/blob/main/pyScripts/%E5%8F%91%E5%B8%83%E7%A8%8B%E5%BA%8F.png)

（1）、第一行点击选择文件，定位到release目录上一级，会自动填写地址；

（2）、第二行填写本次发布版本的SVN版本；

（3）、第三行当需要打包的是EDAProSDK时，选择True，完整EDAPro程序时选择False； （4）、发布目录地址EPSemicon/releaseIndex (github.com)，下载到本地后使用，发布目录选择：

      测试版与官网版SDK选择EPEDAProSDK发布目录.txt；

      测试版与官网版程序选择releaseIndex.txt；

      本地版程序选择mongoReleaseIndex.txt；

（5）、前面四项填写完后，先点击文件汇总，再点击发布，就会有文件夹产生在桌面，该文件夹就是需要发布的SDK或程序，文件夹名就是本次发布版本号；

（6）、如果发布的是本地版，在第五步完成之后再点击按钮mongo版本就会将文件夹中的部分文件内容更改，改为本地版所需的内容，本地版打包完成
