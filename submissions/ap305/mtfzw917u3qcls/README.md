# 目标检测对抗贴片 · 样例工程（patch_attack）

## 场景简介

攻击方生成一张 Universal 对抗贴片（3×32×32，数值 0~1），贴在目标对象上使目标检测器漏检；
防御方实现纯图像二分类器，区分「正常图」与「含攻击贴片图」。

## 目录结构

```
patch_attack_submission_example/
├── solution.py        # 标准入口（Solution 类，含 attack / defend）
├── requirements.txt   # 依赖声明（numpy）
└── README.md
```

## 使用方法（对战大厅 → 工程上传）

1. 下载本 zip，解压后确认根目录含 solution.py；
2. 在对战大厅选择「对抗贴片」场景与角色（攻击方/防御方均可，本样例两种方法都实现了）；
3. 切换到「工程上传」，填写你的 GitHub 账号，上传本 zip；
4. 平台自动解压 → 接口预检 → 预检通过后点击「执行攻击/防御」开始对战。

## 评分说明（教学简化仿真）

- 攻击：HideRate 提升超越自然遮挡基线 → AttackGain；本样例 AttackGain ≈ 100%。
- 防御：FPR ≤ 10% 硬约束 + BalancedAccuracy + AUROC；本样例 FPR = 0%，得分 100。