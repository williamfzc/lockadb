# lockadb

[![PyPI version](https://badge.fury.io/py/lockadb.svg)](https://badge.fury.io/py/lockadb)

lockable android debug bridge, for managing devices precisely and safely

维持adb的所有功能的情况下，增加全局的设备锁。

## 使用

### 安装

python3+

```bash
pip install lockadb
```

### 启动服务端

```bash
ladb.start-server
```

### 像adb一样操作

在命令行中，直接用 ladb 替代 adb 。

lockadb是adb的超集，保留了所有的adb功能。理论上所有adb支持的功能都可以无缝切换到ladb。

### 防冲突机制

lockadb最关键的特性就是从adb层面避免了设备操作冲突。

连入一个设备`123456F`，我们先让该设备忙碌20秒：

```bash
ladb -s 123456F shell sleep 20
```

这样做之后，该设备将被标记为BUSY状态。此时你如果想操作它是被禁止的：

```text
ladb -s 123456F shell echo hello

Traceback (most recent call last):
  File "C:\Python37\Scripts\ladb-script.py", line 11, in <module>
    load_entry_point('lockadb', 'console_scripts', 'ladb')()
  File "f:\lockadb\lockadb\client.py", line 106, in main
    LockAdbRunner.run(command)
  File "f:\lockadb\lockadb\client.py", line 95, in run
    with lock_device(device_id):
  File "c:\python37\lib\contextlib.py", line 112, in __enter__
    return next(self.gen)
  File "f:\lockadb\lockadb\client.py", line 39, in lock_device
    assert acquire_device(device_id), 'device {} is busy'.format(device_id)
AssertionError: device 123456F is busy
```

### 主动锁定

除了自动模式，你也可以手动给设备加锁，更加自由地管理设备。

```bash
# 上锁
ladb acquire 123456F
# 解锁
ladb release 123456F
```

在你上锁之后，除了主动释放设备，该设备将一直保持在BUSY状态。

### python API

除了命令行的模式，你也可以直接调用python API来管理设备。

```python
from lockadb.client import LockAdbRunner, acquire_device, release_device


DEVICE_ID = '123456F'

acquire_result = acquire_device(DEVICE_ID)
print('acquire result is: {}'.format(acquire_result))
LockAdbRunner.run(['devices'])

release_result = release_device(DEVICE_ID)
print('release result is: {}'.format(release_result))
LockAdbRunner.run(['devices'])
```

## 目标

在全自动化管理中，对于adb的依赖程度是非常高的。然而，一般来说我们将设备管理逻辑放在比较高的层级来解决：

- 应用
    - 具体业务
    - 设备管理
- adb
- 设备

但显而易见的，由应用来管控adb命令实际上是非常软性的（很可能会因为疏忽而影响到其他设备），并没有硬性隔离设备。软件操作的边界不明显将很容易导致管理的越界与混乱。在jenkins构建中官方推荐用 lockable resource 来管理资源而不是流水线中用代码进行管理已经说明了很多问题。

然而在日常开发中，使用场景远不局限于jenkins。那么，有没有一种更加通用的方案？答案就是lockadb。

## 设计

使用C/S架构，S端启动常驻服务器用于设备的管理，通过API提供给C端使用。

提供两种形式的CLI用法：

- 命令行CLI
- python API

## 协议

[MIT](LICENSE)
