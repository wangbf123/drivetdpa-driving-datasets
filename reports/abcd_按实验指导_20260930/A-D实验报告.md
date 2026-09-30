# DriveTDPA A-D 开环实验报告

## 1. 实验依据与目的

实验依据文件：

```text
/mnt/workspace/TEMP-FILE-STATION/DriveTDPA 实验指导.docx
```

实验指导要求在 NuScenes-TP 数据集上开展 A-D 四组开环实验，验证训练方法、输入模态、RAT 动作层以及 Talk2BEV 场景上下文的作用。本轮实验完成 A1-A4、B1-B4、C1-C2、D1-D2 共 12 个配置的训练或统一推理评估。

## 2. 实验数据与运行设置

| 项目 | 设置 |
|---|---|
| 数据来源 | NuScenes OSS trainval02-10 |
| 训练样本 | 450 条 |
| 训练场景 | 18 个 scene |
| 评估样本 | 20 条 held-out 样本 |
| 轨迹格式 | 3 秒、6 个轨迹点 |
| 推理后端 | DriveTDPAPredictor |
| 模型推理 | 真实推理，mock=false |
| 模型精度 | BF16 |
| A2-A4 训练步数 | 每组 50 steps |

原始结果路径：

```text
/mnt/workspace/drivetdpa_experiments/abcd_complete_20260924/eval
```

每个配置均保存 `server.log`、`predictions.jsonl` 和 `metrics.json`。

## 3. 实验 A：基础消融

实验指导定义：

| 配置 | 方法 |
|---|---|
| A1 | SFT baseline |
| A2 | SFT + 物理偏好 |
| A3 | SFT + JPO 偏好 |
| A4 | SFT + VL-DPO 偏好 |

### 3.1 训练结果

| 配置 | 训练步数 | 训练样本 | Train loss |
|---|---:|---:|---:|
| A1 SFT | 顺序 SFT 训练链 | 450 | 最终 checkpoint |
| A2 Physics | 50 | 450 | 0.5983 |
| A3 JPO | 50 | 450 | 0.5835 |
| A4 VL-DPO | 50 | 450 | 0.3888 |

### 3.2 评估结果

| 配置 | ADE (m) | FDE (m) | Goal | Consistency (A→T) | Lat 均值 (ms) | 解析成功率 |
|---|---:|---:|---:|---:|---:|---:|
| A1 SFT | **1.5953** | **2.7289** | **0.9042** | 1.0000 | 13442.7 | 100% |
| A2 Physics | 1.5972 | 2.7343 | 0.8994 | 1.0000 | **13213.4** | 100% |
| A3 JPO | 1.5995 | 2.7402 | 0.8932 | 1.0000 | 13375.5 | 100% |
| A4 VL-DPO | 1.5984 | 2.7382 | 0.9016 | 1.0000 | 13746.1 | 100% |

## 4. 实验 B：输入模态消融

| 配置 | 当前输入实现 |
|---|---|
| B1 | 图像 + 文字，不使用 BEV 上下文 |
| B2 | 图像 + 语音指令，不使用 BEV 上下文 |
| B3 | 图像 + 文字 + BEV 上下文 |
| B4 | 图像 + 语音指令 + BEV 上下文 |

| 配置 | ADE (m) | FDE (m) | Goal | Consistency | 场景引用率 | 解析成功率 |
|---|---:|---:|---:|---:|---:|---:|
| B1 Image-Text | 1.9918 | 3.2952 | 0.9382 | 1.0000 | 40% | 65% |
| B2 Image-Speech | **1.5603** | 2.8551 | 0.9379 | 1.0000 | 60% | 60% |
| B3 Image-Text+BEV | 1.5984 | 2.7382 | 0.9016 | 1.0000 | 100% | 100% |
| B4 Image-Speech+BEV | 1.5974 | **2.7341** | 0.8993 | 1.0000 | 100% | 100% |

## 5. 实验 C：有 A 与无 A 对比

| 配置 | 输出协议 | ADE (m) | FDE (m) | Consistency | 平均延迟 (ms) | 解析成功率 |
|---|---|---:|---:|---:|---:|---:|
| C1 R→T | trajectory-only | **1.5969** | **2.7351** | 1.0000 | **13146.6** | 100% |
| C2 R→A→T | 完整 RAT | 1.5984 | 2.7382 | 1.0000 | 13660.5 | 100% |

在可计算 A→T 的样本中，没有观察到动作方向与轨迹方向相反的案例。C1 按 trajectory-only 协议评价轨迹可解析性；C2 输出完整 reasoning、action 和 trajectory。

## 6. 实验 D：Talk2BEV 场景上下文消融

| 配置 | 条件 | ADE (m) | FDE (m) | Goal | Consistency | 场景引用数 | 场景引用率 | 解析成功率 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| D1 no Talk2BEV | 图像 + mission goal | 1.9918 | 3.2952 | 0.9382 | 1.0000 | 8/20 | 40% | 65% |
| D2 Talk2BEV | 加入场景文字描述 | **1.5984** | **2.7382** | 0.9016 | 1.0000 | **20/20** | **100%** | **100%** |

D2 相对 D1：

- ADE 下降 0.3934 m，即 19.75%；
- FDE 下降 0.5571 m，即 16.91%；
- 场景引用率提高 60 个百分点；
- 结构化解析成功率提高 35 个百分点。

## 7. 实验产物

模型 checkpoint：

```text
A1 /mnt/workspace/drivetdpa_experiments/oss_auto_train/trainval10_n50_s50_20260923/train
A2 /mnt/workspace/drivetdpa_experiments/abcd_complete_20260924/A2_physics_tpo50
A3 /mnt/workspace/drivetdpa_experiments/abcd_complete_20260924/A3_jpo_tpo50
A4 /mnt/workspace/drivetdpa_experiments/abcd_complete_20260924/A4_vldpo_tpo50
```

训练数据与配置：

```text
/mnt/workspace/drivetdpa_experiments/abcd_complete_20260924/train_sft.jsonl
/mnt/workspace/drivetdpa_experiments/abcd_complete_20260924/A2_physics.jsonl
/mnt/workspace/drivetdpa_experiments/abcd_complete_20260924/A3_jpo.jsonl
/mnt/workspace/drivetdpa_experiments/abcd_complete_20260924/A4_vldpo.jsonl
/mnt/workspace/drivetdpa_experiments/abcd_complete_20260924/abcd_matrix.json
```

## 8. 本轮结论

1. A1-A4 均稳定生成结构化驾驶动作和轨迹，解析成功率与 A→T 一致性均为 100%。
2. 加入 BEV 的 B3/B4 在结构化输出成功率和场景引用率上均达到 100%。
3. C1/C2 的轨迹精度接近，完整 RAT 协议可稳定输出动作层并保持 A→T 一致。
4. Talk2BEV 对 D 组结果贡献明确：D2 的 ADE、FDE、场景引用率和解析成功率均优于 D1。
