# 《大雨》海报的风格分析与原创换题克隆

风格档案 `SP-STORM-001@0.1`，单图候选。参考图由用户在对话中提供，作为风格与版式参考。仓库保留可重用档案和本次原创生成图。原海报图像没有在此目录重新分发。

## 分析顺序

1. 观察整体。深靛蓝与墨绿环境包围一块接近画幅宽度的朱红橙金近圆主形。上方白色书写标题，下方小型双角色和白色文案。
2. 分辨层次。外围冷色与雨痕，中央伞面及细线装饰，偏下的放射汇聚点和浅色扇形，下方相互靠近且仰视的两人，顶部与底部文字。
3. 记录十三个观察项。见 `style-profile.json` 中 `analysis` 数组，逐项区分可见证据和情绪推断。
4. 提取规则。R01 冷暖分工，R02 放射构图，R03 尺度与关系，R04 绘画及纹理，R05 运动与疏密。R06 为有图文海报时生效的文字层级。
5. 换题适配。巨型红伞由巨型植物种盘承担视觉功能，伞骨与伞轴由植物脉络及种盘中心承担，浅色扇形由种絮承担，雨线由风痕和飞散种子承担，小型双角色改为采种者与狐狸。
6. 从同一结构导出中英文 JSON、中文简易提示词和完整自然语言提示词。`universal-template.json` 使用变量，`task-prompt-spec.json` 保存本次绑定值。
7. 生成 `windborne-seeds.png`，1024×1536 像素。按 `review-status.json` 记录可见结果与待人工确认项。

## 文件

- `style-profile.json` 记录逐项证据、规则、可变范围和检查办法。
- `universal-template.json` 为可换主题的双语通用提示词数据。
- `theme-bindings.json` 和 `task-prompt-spec.json` 为《风里的种子》任务。
- `prompts/` 与 `task-prompts/` 各有四版导出结果。
- `windborne-seeds.png` 是本次生成的原创换题海报。
- `review-status.json` 记录实际生成与视觉验收状态。

## 复用与验证

从 `universal-template.json` 复制新任务，替换 `theme`、`focus`、`characters`、`setting`、`motion`、`title` 和 `tagline`。主体应承担同样的视觉功能，角色关系要清楚。运行仓库工具验证结构：

```bash
python3 风格分析与克隆系统/tools/prompt_package.py \
  风格分析与克隆系统/案例/大雨海报-风里的种子/task-prompt-spec.json \
  --profile 风格分析与克隆系统/案例/大雨海报-风里的种子/style-profile.json
```

当前档案基于一张参考图，适用范围为巨型主形与双角色关系的幻想叙事海报。画面纹理与中文文字在其他生成后端需要再次验收。具体纸张、工艺和物理光源未由参考图确认。
