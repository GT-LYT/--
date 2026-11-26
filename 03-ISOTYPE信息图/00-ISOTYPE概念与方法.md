# ISOTYPE｜概念、方法和设计边界

## 概念与历史
ISOTYPE 是国际图像文字教育系统，建立于 Otto Neurath 等人推进的维也纳图像统计方法基础之上。Marie Reidemeister（Marie Neurath）负责重要的信息转译工作，Gerd Arntz 为图像词汇提供了系统化的视觉语言。它不仅是图标风格，更是**面向公众解释资料的转译过程**。

## 设计语法
1. **信息转译**：先有证据、明确受众问题，再决定图形与必要说明。
2. **图符词汇**：同类对象保持轮廓、比例、简化程度、方向与语义一致。
3. **固定单位重复**：如涉及数量，`number_of_symbols = value / symbol_unit`；量值变大时增加**等尺寸图符的数量**，而不是任意放大单个符号。
4. **余量处理**：非整除数值须说明部分图符、单独注释或舍入方式；不能悄悄取整。
5. **版式与文本**：通过对齐、间距、类别色、标题和图例建立阅读顺序，保留来源、单位和统计口径。

## 与仓库分类关系
作品仍需先判 01 五种数据逻辑，再判 02 表现形式；03 只作为跨类型**方法证据**。视觉上像 Gerd Arntz 不等于属于历史原作。区分 **历史 Isotype / 可核验当代方法应用 / Isotype-inspired**。

## 基础数据字段
建议 `record_id,category_id,value,unit,symbol_id,symbol_unit,source_id`；各列独立、一格一值；多值关联用另一张关系表。

## 核查与反例
- 图例是否明确“每个符号等于多少单位”？
- 是否存在同一主题不同符号尺度冲突？
- 图符是否因风格而错误暗示数量或类别？
- 单个 ISO 标准化导视标志不自动算 ISOTYPE。

## 可复用制作流程
研究→清洗数据→定义语义→统一符号→单位换算→网格布局→图例/文字→核对数据→版本保存与用户验证。流程为本仓库推荐方法，不冒称所有历史设计者的实际流程。

[历史入口](./01-历史与文献/README.md) · [视觉编码](./02-图符语言与视觉编码/README.md) · [案例归档](./03-案例研究/README.md)

## 参考
- [维也纳大学](https://isotype.univie.ac.at/en/)
- [Isotype Revisited](https://isotyperevisited.org/2012/08/introduction.php)
- [斯坦福哲学百科：Neurath](https://plato.stanford.edu/entries/neurath/)
