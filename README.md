#### 前言

这个仓库整合了之前写的**碧蓝航线**复读机脚本和**明日方舟**复读机脚本，同时提供了ios平台和android平台的python执行脚本，对其中代码做了一番整理，抽出公共的代码到common文件夹中。

使用复读机脚本需要一些额外的支持，例如ios的脚本需要装有macos的电脑 + xcode-tools + libimobiledevice(部分国行设备可能需要)；android则需要提前安装adb sdk的相关命令行工具，总得来说初次配置可能比较麻烦；

使用复读机脚本，可能还需要自行更新一下素材，不同设备的分辨率、屏幕比例不一致可能导致 OpenCV 在比对图片时失败。笔主使用的手机还是老古董 iphone SE ，也会使用安卓模拟器。如果出现脚本不能正常运作，可**先尝试替换项目中assets的素材**（文件名注意要一致，或者自己改进代码也可以的）。

感谢提供了复读机思路的作者 [UltimatePea](https://github.com/UltimatePea) 。其实初次写脚本的时候使用了面向过程编程，代码中充斥了第一步判断xx、第二步判断xx之类的逻辑代码，如果中间某一步出错，流程就无法进行下去而需要重头来一遍。U大的脚本令我眼前一亮，他把游戏中可能出现的所有场景及场景出现后应该执行的操作，封装到一个一个的实例中，最后主线程执行一个`While(True)`查询游戏当前状态并执行相应的操作。

> 不知为何让我联想到了Reactor模式、同步非阻塞(NIO)以及NIO框架中著名的Netty中的boss线程等一些概念，主线程不停查询 handle 并获得当前最新的状态（State），然后执行对应（handler）的逻辑。
>
> 这里，游戏本身就是一个handle，游戏的各个场景就是各种的state，每个state对应的操作就是一个handler。这里可能表述得不是特别好，究其所以 Reactor 模式和 NIO 本人也并未有过特别深入，仍需继续给自己充电呢
>
> 我觉得我可能是一个假的面向对象编程程序猿，所以没有对象……（苦笑）

U大写的脚本请看 [这里 - AzureLaneGame_AutomationScript](https://github.com/UltimatePea/AzureLaneGame_AutomationScript) ，可惜脚本最后一次更新已经是2年前了，可能已经退坑了吧。我也希望自己能早日退坑成功（两次退坑失败的提督又被另一位刀客特拖进了方舟的深渊）。如果这个项目得到同行（无论是提督还是刀客特）的使用，也希望各位护肝成功。

也感谢另一位作者提供了 `auto_adb.py` 连接操作安卓模拟器的方法，笔主在其基础上修改以支持了远程连接模拟器进行操作（笔者使用了MacBook Pro去控制一台windows10下的安卓模拟器，MacBook跑模拟器实在太卡了……苦笑+1）。但是因为一不注意没有留下该作者的 Github 仓库地址，非常抱歉！！！后面笔主会继续尝试寻找并补到该README中的。非常抱歉！！！

> 其实，大部分都会用按键精灵或者其他屏幕录制工具吧，像这样搞那么复杂的可能只有笔主一个了（苦笑+2）

​        

最后

- 本软件遵从 Apache-2.0 开源协议，仅授权以程序开发，手游自动化等为目的的交流学习！
- 本软件**不授权在碧蓝航线的服务器上以不正当手段获取任何形式利益的行为。**
- 本软件不得被用于商业目的。



#### 树形目录

- `arknights` - 明日方舟复读所需的文件

  - `assets` - 素材&截图

    - `640x1136` - 适用于 iphone SE 分辨率的素材

    - `1125x2436` - 适用于 iphone 11 Pro 分辨率的素材 

      > 空的，暂时买不起:-)

  - `loadscene.py` - 加载游戏中需要识别的场景特征文件

- `azurelane` - 碧蓝航线复读所需的文件

  > 内部结构和明日方舟大同小异

- `common`

  - `device` - 对ios和安卓设备的获取截图、点击等操作进行抽象和封装
  - `i_device.py` - 抽象的接口
    - `c_ios.py` - ios平台的接口实现
    - `c_android.py` - 安卓平台的接口实现
  - `auto_adb.py` - 对安卓平台的adb调用的封装
  - `eventloop.py` - 复读机核心
  - `scene.py` - 对复读机可能遇到的场景的封装类
  - `tool.py` - 工具类，提供判断一张图片中是否包含另一张图片、所在位置的方法

- `temp` - 复读期间生成的截屏图片临时存放目录

- `default-config.ini` - 默认配置文件

- `config.ini` - 该文件由上面的 default-config.ini 修改而来，用于指定复读哪个游戏、游戏复读时可选的额外配置等

- `start@ios.py` & `start@android.py` - 对应 ios平台/安卓平台的执行文件

- `detect-test@ios.py` & `detect-test@android.py` - 用来测试 OpenCV 识别特征图片在设备截屏中的具体位置用的脚本

- 其它一些文件，如`README.md`，`LICENSE`等



#### 运行环境要求

- Python 3.x
- iOS
  - 一台 iPhone 或 iPad（建议根据实际设备重新截取场景特征）
  - 一台装有macOS的电脑
  - Xcode.app
  - WebDriverAgent [Github地址](https://github.com/appium/WebDriverAgent)，[iOS设备安装引导](https://testerhome.com/topics/7220)
  - openatx/facebook-wda [Github地址](https://github.com/openatx/facebook-wda)
  - libimobiledevice（可选，使用homebrew安装）
- 安卓
  - 安卓模拟器（mumu、夜神或其它）
  - Putty（可选）



#### 运行步骤

1. 首次使用，将目录下的`default-config.ini`改为`config.ini`

   1. 在 `config.ini` 文件中配置好需要复读的游戏字段 `game_name=azurelane` 或 `game_name=arknights`
   2. （可选）其它一些配置

2. iOS平台
   1. 启动 Xcode.app 并打开 WebDriverAgent 项目，连接手机后在 Xcode 中选中对应的手机，手机需要和电脑位于同一个局域网

   2. Command + U 启动 Test ，Xcode 会将 WebDriverAgent 安装到设备上（此时手机会出现一个无图标的应用程序）

      > 如果Xcode提示Could not launch，根据提示判断是否需要到 设置 -> 通用 执行信任开发者证书操作

   3. 观察 Xcode 的 Console 控制台输出（快捷键 Shift+Command+C 打开），最底部会有一串访问地址

      ```
      ServerURLHere->http://${ip地址}:8100<-ServerURLHere
      ```

   4. 取出上面的地址`http://${ip地址}:8100`到浏览器访问
      如果可以获得一个json响应，打开文件 start@ios.py ，找到 main 方法，编辑 device 的构建参数 address 为实际的ip加端口，保存文件并退出

      ``` python
      if __name__ == '__main__':
          ...
          # 3. init device
          dpi = 2  # iphone SE 的屏幕DPI为2，使用wda发送触摸指令时坐标(x,y)需要除以相应的dpi
          device = IOSDevice(dpi, log_level=cfg.log_level, address='http://127.0.0.1:8100')
          ...
      ```

      如果无法获得json响应

      1. 新开一个终端，任意目录下，输入 `brew install libimobiledevice --HEAD` 安装 libimobiledevice

         > 如果提示 brew command not found 请先百度或谷歌安装 homebrew

      2. 新开一个终端，任意目录下，输入 `iproxy 8100 8100` 

   5. 如果使用的设备存放的素材路径不一致，打开文件 start@ios.py 在 `main` 方法中编辑对应的素材位置前缀，保存文件退出

      ``` python
      if __name__ == '__main__':
          ...
          # 2. init scenes
          prefix = rt.game + '/assets/640x1136/feature/'
          ...
      ```

   6. 新开一个终端，切换到项目目录下，输入 `python3 start@ios.py`

3. Android平台（以网易mumu模拟器为例）
   1. 将模拟器分辨率设置为 640x1136 （或者根据实际分辨率重新截取特征素材）
     
   2. 新开一个终端/命令行，输入 `adb connect 127.0.0.1:7555`

      > 7555是网易mumu模拟器的ADB监听端口，其它模拟器的adb端口建议自行百度/谷歌

   3. 输入 `adb devices` 列出当前所有设备，如果有多个，需要打开文件 start@android.py ，找到 `main()` 方法，在创建设备对象时传入对应的设备地址与端口号，如下，保存文件退出

      ``` python
      if __name__ == '__main__':
          ...
      		# 3. init device
          device = AndroidDevice(log_level=cfg.log_level, address='http://127.0.0.1:7555')
          ...
      ```

   4. 如果使用的设备存放的素材路径不一致，打开文件 start@android.py 在最底部的 `main()` 方法中编辑对应的素材位置前缀，保存文件退出

      ``` python
      if __name__ == '__main__':
          ...
          # 2. init scenes
          prefix = rt.game + '/assets/640x1136/feature/'
          ...
      ```

   5. 新开一个终端，切换到项目目录下，输入 `python3 start@android.py`


#### 参考资料

- [ADB命令参考1](https://www.wanandroid.com/blog/show/2309)
- [ADB命令参考2](http://wl9739.github.io/2017/05/22/ADB-%E5%B8%B8%E7%94%A8%E5%91%BD%E4%BB%A4/)
- [macOS 远程连接windows的Android模拟器](https://nicoster.github.io/%E8%BF%9C%E7%A8%8B%E8%BF%90%E8%A1%8C-android-%E6%A8%A1%E6%8B%9F%E5%99%A8/)
- [macOS 平台上通过 Xcode 使用 wda 以及 libimobiledevice 安装说明](https://github.com/wangshub/wechat_jump_game/wiki/Android-和-iOS-操作步骤#二ios-手机操作步骤)