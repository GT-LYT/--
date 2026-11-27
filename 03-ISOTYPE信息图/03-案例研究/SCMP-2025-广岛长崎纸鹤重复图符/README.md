# Visualising the human toll from the world’s first nuclear attacks

**原作入口：** [打开 SCMP 图文与原作图片](https://multimedia.scmp.com/infographics/news/world/article/3320825/hiroshima_nagasaki/index.html)

> ISOTYPE方法应用。**证据状态：原刊正文及方法学文字直接核实，作品图像由SCMP网页展示。** 本仓库只存研究文字和源站链接，未复制第三方版权图片。不同研究分类不可重复计同一作品。

## 0 元数据
- 来源平台：SCMP
- 来源作品 ID：3320825-hiroshima_nagasaki
- 作者或制图：Davies Christian Surya、Kaliz Lee、Victor Sanjinez、Eunice Tse
- 发表日期：2025-08-06
- 稳定原作网址：https://multimedia.scmp.com/infographics/news/world/article/3320825/hiroshima_nagasaki/index.html
- 主归档：`03-ISOTYPE信息图/03-案例研究/SCMP-2025-广岛长崎纸鹤重复图符`

## A 数据组织
SCMP原文写明每个纸鹤剪影代表1名伤亡者；每次印章印100只纸鹤，共印2,140次，最终呈现214,000个剪影。

## B 统计方法与计量边界
一只纸鹤剪影对应一名伤亡者；一次印章100个剪影；2,140次印章总计214,000剪影。此数量是作品所采用的估计总数，并非可分解的逐人原始记录。

## C 视觉编码
固定规格纸鹤剪影为基础符号，重复次数表示伤亡规模；纸鹤同时是和平与纪念的象征，数字与图符具有双重意义。

## D 数据架构及复现字段
建议记录 project_id, symbol_id, symbol_meaning, symbol_unit, stamp_count, symbols_per_stamp, symbol_total, source_url；印章数量与剪影数量须分列，计算值另设派生字段。

## E 视觉叙事
历史事件→伤亡的人类尺度→重复纸鹤的总量→纪念与反思。

## 误读风险与设计实践
纸鹤符号刻印表示作者选择的估计伤亡总数，不能分解成未经核实的逐人观测值；它是ISOTYPE方法级借鉴，不是20世纪历史原作。

建议实践：核对图面→确认对象与来源→分解字段和编码→绘制设计结构图→对照前后布局/符号方案→验证阅读理解→回写Gestalt或ISOTYPE方法，不伪造已开展的实验。

[原图与使用许可状态](./原图来源.md)
