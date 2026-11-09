# sizetree

**以树状结构展示目录占用，按大小排序。**

`du` 的输出是平的，`ncdu` 需要交互。`sizetree` 取中间：一条命令给出可读的树、占比和排序，输出可以是文本，也可以是 JSON。

[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![Zero deps](https://img.shields.io/badge/dependencies-0-brightgreen)](#设计取舍)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)
[![CI](https://github.com/eathink/sizetree/actions/workflows/ci.yml/badge.svg)](https://github.com/eathink/sizetree/actions/workflows/ci.yml)

## 快速开始

```bash
pipx install git+https://github.com/eathink/sizetree

sizetree ~/workspace/projects --depth 1 --min-size 100K
```

```console
$ sizetree ~/workspace/projects --depth 1 --min-size 100K
 917.9 KiB  100.0%  projects/
├──  179.0 KiB   19.5%  envdiff/
├──  157.9 KiB   17.2%  mockd/
├──  123.3 KiB   13.4%  skills-lite/
└──  109.7 KiB   11.9%  crondoc/
```

每一行是「大小、占根目录的百分比、名称」；目录以 `/` 结尾，按大小从大到小排列。

## 用法

```bash
sizetree [PATH] [--depth N] [--min-size SIZE] [--sort size|name] [--format tree|json]
```

| 参数 | 说明 |
| --- | --- |
| `PATH` | 要扫描的目录，默认当前目录 |
| `--depth N` | 展开层数，默认 `2`；`0` 只显示根目录 |
| `--min-size SIZE` | 只显示不小于该大小的条目，支持 `10K` / `1.5M` / `2G`（1024 进制） |
| `--sort` | `size`（默认，从大到小）或 `name` |
| `-f, --format` | `tree`（默认）或 `json` |
| `--version` | 版本号 |

### JSON 输出

```bash
sizetree . --depth 1 --format json
```

```json
{
  "name": "projects",
  "path": "/home/me/projects",
  "size": 939961,
  "human_size": "917.9 KiB",
  "percent": 100.0,
  "is_dir": true,
  "children": [
    {
      "name": "envdiff",
      "size": 183296,
      "human_size": "179.0 KiB",
      "percent": 19.5,
      "is_dir": true,
      "children": []
    }
  ]
}
```

`--depth` 与 `--min-size` 同样作用于 JSON 的嵌套结构，方便直接喂给脚本。

## 统计口径

- 使用文件的**表观大小**（`st_size`），不是磁盘块占用；稀疏文件会显得比 `du` 小
- **跳过符号链接**，不跟随，避免重复计算和环
- **不合并硬链接**：同一个 inode 被多个路径引用时会重复计入（与 `du` 的默认行为不同）
- 无权限读取的目录按空目录处理，不中断扫描

## 设计取舍

- **不做交互式 TUI**：`ncdu` 已经做得很好；这里要的是可管道、可脚本、可进 CI 的静态快照
- **零依赖**：只用 `os.scandir`，不引入 curses/rich
- **先建完整树再渲染**：`--depth` 只影响输出，不影响统计；换深度不需要重新扫描
- **大小与占比同时给**：只给绝对值很难判断"这个目录大不大"

## 开发

```bash
git clone https://github.com/eathink/sizetree
cd sizetree

# 仅用标准库，无需安装依赖
PYTHONPATH=src python3 -m unittest discover -s tests -v

# 本地运行
PYTHONPATH=src python3 -m sizetree . --depth 2
```

## License

[MIT](LICENSE)
