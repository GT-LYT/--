# 04｜统计图形分析

此处研究数据结构、统计计算、图形选择与视觉变量，不增加第六种基础数据逻辑。对照参考仓库 [04-统计图形分析](https://github.com/fengbaifan/Infographic-Style-Repository/tree/main/04-统计图形分析)。

## 来源数据到统计图形的审查
| 环节 | 关键问题 |
|---|---|
| 记录粒度 | 一行是企业、地区还是年度？分类和计量字段分别是什么？ |
| 统计变换 | 计数、求和、平均、占比、分母、异常值和缺失如何处理？ |
| 图形选择 | 比较、趋势、组成、分布、空间、关联分别用哪个图表？ |
| 视觉编码 | 位置/长度/面积/色彩映射哪个变量？基线、色标和单位何在？ |
| 解释限制 | 相关≠因果，时间先后≠依赖，引线≠流向，圆半径≠圆面积。 |

## 统计图可选工具
- RAWGraphs App: https://github.com/rawgraphs/rawgraphs-app
- RAWGraphs Charts: https://github.com/rawgraphs/rawgraphs-charts
- RAWGraphs Core: https://github.com/rawgraphs/rawgraphs-core

## 已有分析：Fortune 500 营收比例圆
[图形分析](../02-信息图形类型案例/01-混合型-Mixed-Charts/案例/FORTUNE-2020-Power-Centers/分析.md) · [转录基础CSV](../02-信息图形类型案例/01-混合型-Mixed-Charts/案例/FORTUNE-2020-Power-Centers/基础数据.csv)。地图的小点提供都市区空间位置，圆形用于累计营收的规模比较；曲线为标注引线，不承担贸易或资金流量编码。重绘时建议圆面积而非半径与值线性成正比，**原图没有可核实的面积图例，不能断言作者采用了特定数学公式**。

[统一统计分析模板](./统计图形分析记录模板.md) · [02案例索引](../02-信息图形类型案例/案例索引.md)
