1. clone webdriveragent
2. xcode打开webdriveragent，xcode preferences 选择account登陆开发者账号
4. 安装carthage
5. webdriveragent目录下运行./Script/bootstrap.sh
6. 遇到unable to find utility "simctl", not a developer tool or in PATH，xcode preferences Location选择CommandLineTools的提供方，参考sof(https://stackoverflow.com/questions/29108172/xcrun-unable-to-find-simctl)
7. xcode 点选项目 setting signing&capabilities webdriveragentlib 选择 team为自己的account
8. xcode 点选项目 setting signing&capabilities webdriveragentrunner 选择 team为自己的account，注意更改bundleid（在info、build settings里搜索bundle，修改对应位置）
9. xcode 点选项目 setting signing&capabilities integrationApp 选择 team为自己的account，注意更改bundleid（在info、build settings里搜索bundle，修改对应位置）
10. xcode 使用 webdriveragentrunner 模式，切换指定设备，cmd+u运行test
11. iphone 信任证书，test 启动成功
12. 安装 libimobiledevice 运行 iproxy 8100 8100
13. clone game-script & pip3 install -r requirements.txt
14. python3 start.py -h