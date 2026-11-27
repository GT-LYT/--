# 鲸鱼暮色嵌景风格

本案例保存经调整的通用中英文 JSON。风格档案为 `SP-DUSK-INLAY@1.0`，统一数据结构版本为 1.0。

- `prompt.zh.json` 为中文通用提示词。
- `prompt.en.json` 为英文通用提示词。
- `prompt-spec.json` 为两种语言共用的数据源。
- `style-profile.json` 保存核心规则及参考来源。

使用时填写 carrier、identity_marks、inner_world、landmark、junction、receiver 六个变量，分别对应载体、识别特征、内部世界、地标、轮廓消隐接口和外部承接面。中英文变量及规则编号一致，已通过仓库提示词校验器。

## 参考原图

原图为用户在聊天中提供的黑底鲸腹村庄插画。当前可读文件未包含其原始图片字节，原图归档状态为待补。补齐后在此目录添加 reference-original 图片，并更新风格档案中的参考文件路径。

## 生成效果与适用范围

候选风格已试用于鲸腹灯塔和机车车站，各生成一次。鲸图的鲸头厚色更重，机车更偏实体剖面。跨模型和重复生成稳定性尚未验证。

[查看两张已生成插画及十三项分析](https://chatgpt.com/space/page_dd733f0f63288191891235a855672dbd)
