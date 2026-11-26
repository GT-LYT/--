# 03 数据搜集

## 公共数据集：世界银行WDI

- 唯一数值来源：[World Bank Gross domestic product 2024（PDF）](https://datacatalogfiles.worldbank.org/ddh-published/0038130/DR0046441/GDP.pdf)。
- 原表发布日期：**2025-12-15**；统计年度**2024**。
- 原表单位：**millions of US dollars**。
- 机器字段参考：[World Bank NY.GDP.MKTP.CD](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD)，但本次**没有从实时API混入新版本数值**。
- 已人工核对：前十名与World汇总行。另存为[原始摘录.csv](./原始摘录.csv)，保留世界总量独立记录。

## 文献理解与数据边界

世界银行指标NY.GDP.MKTP.CD表示按现价美元衡量的GDP，不能替代实际GDP增长率、购买力平价GDP、人均GDP。美元汇率波动可能影响国际名义规模比较。

## 自建数据

本项目没有实施问卷或采集新的一手经济数据。自建部分是前十总和、世界其他地区合计及占比；均标`derived`，保留计算公式。
