# -*- coding: utf-8 -*-
"""目标检测对抗贴片（patch_attack）样例工程 —— 可上传、可预检、可直接对战

攻击契约:  def attack(env, task) -> dict
    task 内含 images / annotations / target_class / patch_size / max_patch_area_ratio / detector
    返回 {"patch": ndarray (3, 32, 32)，0 <= patch <= 1}（Universal 对抗贴片）

防御契约:  def defend(env, images) -> dict
    返回 {"patch_probability": float 或 [N]}（纯图像二分类：正常图 vs 含贴片图）

本样例同时实现 attack 与 defend，上传后无论选择攻击方还是防御方，
均可通过接口预检并直接进入对战。
"""

import numpy as np

IMG = 32
# 引擎教学简化仿真：目标对象为图像中央 8x8 高亮块，
# 规则检测器以中央区域平均亮度 0.6 为检测阈值。
TARGET_SLICE = slice(12, 20)


class Solution:
    """标准入口：平台以 Solution(work_dir) 实例化后调用规定方法。"""

    def __init__(self, work_dir: str):
        self.work_dir = work_dir

    def attack(self, env, task):
        """生成 Universal 对抗贴片：暗色贴片覆盖目标，使检测器漏检。

        返回的 patch 形状必须为 (3, 32, 32) 且数值在 0~1 之间。
        """
        patch = np.full((IMG, IMG, 3), 0.10, dtype=np.float32)
        # 中央目标块进一步压暗，确保贴片叠加后中央亮度低于 0.6 检测阈值
        patch[TARGET_SLICE, TARGET_SLICE, :] = 0.02
        # 引擎要求通道在前 (C, H, W)
        patch = patch.transpose(2, 0, 1)
        return {"patch": patch}

    def defend(self, env, images):
        """朴素贴片检测器：贴片 = 中央暗且均匀（低亮度 + 低方差）；
        正常目标中央亮（高亮度），背景为噪声（高方差），据此区分。
        """
        probs = []
        for img in images:
            arr = np.asarray(img, dtype=np.float32)
            center = arr[TARGET_SLICE, TARGET_SLICE, :]
            mean = float(center.mean())
            std = float(center.std())
            probs.append(1.0 if (mean < 0.35 and std < 0.04) else 0.0)
        return {"patch_probability": probs}