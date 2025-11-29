# epauto

epauto是一个非常简单，针对下面界面网页登录的校园网的全自动登录工具

![banner.png](res/banner.png)

你只需要在`config.toml`中输入校园网登陆网址、用户名和密码，然后运行epauto即可无需担心校园网的登录问题

虽然不敢保证所有类似的校园网能使用epauto，但根据维护者的身边统计学，至少不止维护者的高校使用该校园网系统，故可以暂时推断类似界面的校园网使用同一个系统

> epauto主要针对使用路由器等工具应付校园网检查，且存在可作为服务器的设备无间断运行的情况，因为维护者的使用情况就是这样

# 优势

- 使用Python开发，简单易懂，~~方便维护者跑路有后人接手~~

- 服务端友好，不需要配置GUI

- 通过Websocket检测连接情况，无需担心中断

> 在维护者简单搜索Github的相关关键词后，搜索Eportal无关信息太多不好整理，而搜索维护者高校时，不乏存在校园网登录工具，但基本都是GUI和简单脚本，并没有一个长时间维持校园网存在的工具，所以epauto还是有存在的必要的，虽然似乎找不到第二个和维护者环境差不多的

# 如何使用

```
$ epauto --help

Usage: epauto [OPTIONS]

Options:
  --config PATH  Path to configuration file.
  --version      Print epauto version.
  --help         Show this message and exit.
```

要使用epauto，你需要提供校园网的登录网址、用户名和密码来让epauto通过模拟浏览器网页登陆的方式来登录校园网

epauto使用[TOML](https://toml.io/cn/v1.0.0)作为配置文件，默认读取当前目录下的`config.toml`，你可以使用`--config PATH`参数来自定义配置文件的地址

> epauto使用标准库`tomllib`解析TOML文件，`tomllib`只能解析TOML而无法写入，故epauto无法创建默认配置；epauto仓库提供了一份默认的`config.toml`，请根据该配置文件自行更改

# 安装

## 准备工作

你需要安装下面的依赖:

- [Python](https://www.python.org/downloads/) 3.11或更新
- (可选) [uv](https://docs.astral.sh/uv/) 0.9或更新
- (可选) [Docker](https://www.docker.com/) 28.0或更新
- (可选) [Podman](https://podman.io/) 5.0或更新

> 实际上uv和docker/podman的版本维护者也不确定，维护者按正在使用的工具链版本选了个大版本作为最低要求

## 方法1: 使用pip安装

> 暂未发布到[PyPI](https://pypi.python.org/)

## 方法2: 使用`git clone`

这个方法适合所有想要更改代码的用户:

`$ git clone https://github.com/rintim/epauto.git`

然后进入epauto的目录，修改`config.toml`的配置，然后执行:

```
$ uv sync
$ ./.venv/bin/epauto
```
## 方法3: 使用Docker/Podman

该方法是维护者使用的方法，但维护者并非Docker领域大神，因此只提供最基础的Dockerfile，未来考虑通过Github Action自动发布Docker镜像

要使用该方法，你需要安装Docker和Podman中的任何一个来构建容器

请执行:

```
-- 克隆epauto仓库
$ git clone https://github.com/rintim/epauto.git

-- 进入epauto目录
$ cd epauto

-- 开始打包
$ docker/podman build . -t "epauto:0.3.0"

-- 等待打包完后运行
$ docker/podman run -it "epauto:0.3.0" -v $config.toml:/app/config.toml
```

# 贡献

该项目暂时没有什么贡献准则，不过最好遵循下面的规定:

- Python代码请遵循[PEP-8](https://peps.python.org/pep-0008/)，且经过[black](https://github.com/psf/black)格式化

- issues是用来提交Bug或征询意见的，而discussions是用来提问题的

- epauto主要聚焦于自动维护校园网的登录，而不是校园网网页的逆向；你可以等待维护者的下一个项目，不过维护者应该会使用C#

- ~~维护者也没啥经验，甚至对Python的理解严重不足，对于铸币代码请理解~~

# 版权

epauto is licensed under the MIT license.
