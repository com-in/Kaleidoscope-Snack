# 森罗物语：小吃（Kaleidoscope Snack）

为《森罗物语》(Kaleidoscope Cookery) 添加一系列街头小吃与制作它们的食材。

> [!IMPORTANT]
>
> 这是《森罗物语》的**附属模组**，必须与森罗物语一起安装才能使用。

> [!NOTE]
>
> 此模组处于**开发**阶段，当前版本不代表最终品质。

- **Mod ID**：`kaleidoscope_snack`
- **游戏版本**：Minecraft 1.21.1
- **加载器**：NeoForge 21.1.232+
- **前置**：Kaleidoscope Cookery（森罗物语）

## 主要内容

### 材料

| 物品 | 说明 |
| --- | --- |
| 肠衣 | 不可食用，用于合成香肠 |

### 制作方式

| 工作方块 | 产物 |
| --- | --- |
| 炒锅 | 狼牙土豆、煎饼、锅贴、铁板鱿鱼 |
| 砧板 | 土豆块、肉糜 |
| 汤锅 | 肠衣 |
| 营火/旋风烤肉塔 | 烤肠（由香肠烤制） |
| 工作台 | 香肠（肉糜 + 肠衣） |

配方均按森罗物语原有玩法设计，例如炒锅制作狼牙土豆需要：

- 载体：碗
- 材料：3 × 土豆块、2 × 红辣椒
- 产出：1 × 狼牙土豆

配方可以直接在 **EMI / JEI** 中查看。

## 安装

1. 安装 Minecraft 1.21.1 与 NeoForge（21.1.232 或更高）。
2. 下载 [Kaleidoscope Cookery](https://modrinth.com/mod/kaleidoscope-cookery)（森罗物语：厨房），放入 `mods/`。
3. 下载本模组（可在 [Actions](https://github.com/com-in/Kaleidoscope-Snack/actions) 找到最新以及还未正式发布的版本，或在 [Releases](https://github.com/com-in/Kaleidoscope-Snack/releases) 找到最新的稳定版本）`kaleidoscope_snack-<版本>.jar`，放入 `mods/`。
4. 启动游戏，创造模式物品栏中会多出一个「森罗物语：小吃」分类。

## 在服务器中使用

本模组添加了新方块和物品，在服务器中使用时，**服务端与客户端都需要安装**才能正常游玩。

## 链接

- 仓库：<https://github.com/com-in/Kaleidoscope-Snack>
- 作者：Ctoy
- 使用 [MCreator](https://mcreator.net/about) 制作

## 贡献指南

### 提交 Issue

前往 [New Issue](https://github.com/com-in/Kaleidoscope-Snack/issues/new) 提交问题、改进建议或新物品申请。

### 贡献配方（KubeJS 工作流）

模组配方以 KubeJS 脚本编写，推送后触发构建，自动转换为原生数据包 JSON 并内置进 JAR。

环境要求：Node.js 18+、Gradle。

```bash
# 1. 将 KubeJS 脚本转换为数据包 JSON
node tools/kubejs-to-datapack.mjs   # 读取 run/kubejs/server_scripts/*.js，生成 recipe/*.json

# 2. 构建模组
./gradlew build                     # 产物：build/libs/kaleidoscope_snack-<版本>.jar
```

新增配方时，在 `run/kubejs/server_scripts/` 下创建 `<item_id>.js`，参照现有脚本编写，然后执行上述两步。


### 开发计划

- [ ] 添加更多种类小吃
- [ ] 添加一些机器
- [ ] 优化模型贴图
- [ ] 脱离 MCreator 重构项目（远期）

## 许可证

本项目采用 MPL-2.0 许可证。详见 [LICENSE](LICENSE) 文件。