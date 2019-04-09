# lockadb

lockable android debug bridge, for managing devices precisely and safely

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

### 基本功能

维持adb的所有功能的情况下，增加一些新的特性。

命令行CLI保持与adb所有的特性一致，并在此基础上加入耗时任务管制（例如利用adb shell执行某个耗时脚本，ladb会将该设备锁死避免被其他应用同时调用）。

### 进阶功能

ladb的最终目的是实现类似docker的设备沙盒（当然只是语法层面），让每个应用只能够接触到他当前可以接触的设备，以避免发生冲突。

## 使用

### 安装

```bash
pip install lockadb
```

### 启动服务端

```bash
python -m lockadb.server
```

## 协议

[MIT](LICENSE)
