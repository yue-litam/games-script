# 碧蓝航线辅助脚本

本Repo最初直接fork自[UltimatePea/AzureLaneGame_AutomationScript](https://github.com/UltimatePea/AzureLaneGame_AutomationScript)，后在原Repo基础上做了资源的调整和部分判定逻辑的改动，遂对原fork仓库进行Archived、另行新建了一个Repo进行保存。<br/>

主要改动

- 适配了自己的iphoneSE
- 根据python-cv-agent的DPI缩放，调整了wda模拟触摸时的坐标值
- 调整了判断界面状态的相似度阈值，优化std输出内容

感谢原作者的奉献，本Repo请勿用于商业行为。

## 使用方法

本软件依赖WebDriverAgent及其Python Binding, Opencv-Python Binding, 请自行搜索安装。具体安装方法请参见[这里](https://github.com/wangshub/wechat_jump_game/wiki/Android-和-iOS-操作步骤#二ios-手机操作步骤)

安装好依赖后运行

```
python3 start.py
```

如果有特征图无法识别的，建议根据自己的设备，重新截取对应特征，最后用detect-test.py进行验证。验证通过，会在原图以绿色边框框处目标。

## 软件协议

本软件以Apache-2.0协议开源。除此以外，本软件仅授权以程序开发，手游自动化等为目的的交流学习。本软件**不授权在碧蓝航线的服务器上以不正当手段获取任何形式利益的行为。**本软件不得被用于商业目的。

## 软件原理

本软件通过截图与图片库中的图片比对判断游戏状态并操作。
