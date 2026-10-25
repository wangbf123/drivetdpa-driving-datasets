# E/F/G 闭环实验完整结果（CARLA 实时 pipeline）

- 链路：语音 / 轨迹指令 → 真实 InternVL → RAT → YAML → ROS2 → Autoware E2E → CARLA 车辆
- 判定时钟：CARLA 仿真时钟（`sim_now()`），非墙钟
- E2E 控制链修复（composable→standalone）是 F/G 能跑通的前提，见 `autoware_carla_interface.launch.xml` 注释

## 实验 E：语音指令闭环（5 指令 × 10 trial = 50/50）

判定阈值：FORWARD `min_v≥0.3 ∧ |dyaw|≤0.2`；LEFT `dyaw≥0.1`；RIGHT `dyaw≤-0.1`；SPEED_UP `Δv≥0.25`；SLOW_DOWN `Δv≤-0.25`。

| 指令 | n | 成功率 | v_peak (m/s) | v_end (m/s) | dyaw (°) | 关键增量 |
|---|---|---|---|---|---|---|
| FORWARD | 10 | 1.00 | 2.246±0.011 | 2.214±0.030 | −0.015±0.052 | — |
| LEFT | 10 | 1.00 | 2.255±0.009 | 2.224±0.028 | **+37.633±0.469** | dyaw 范围 [36.63, 38.19] |
| RIGHT | 10 | 1.00 | 2.268±0.018 | 2.247±0.035 | **−36.910±0.561** | dyaw 范围 [−37.57, −35.75] |
| SPEED_UP | 10 | 1.00 | **2.895±0.001** | 2.873±0.028 | ≈0 | Δv(peak−base) **+1.777±0.037** |
| SLOW_DOWN | 10 | 1.00 | 1.693±0.011 | **0.429±0.046** | ≈0 | Δv(end−base) **−1.227±0.043** |

**对称性与可重复性**：LEFT 与 RIGHT 幅度高度对称（+37.63° / −36.91°，差异 <1°），各自 std <0.6°；SPEED_UP 峰值稳定在 2.895 m/s（std 0.001，疑似触达速度上限/限速）；SLOW_DOWN 末端稳定在 0.43 m/s（std 0.046）。

## 实验 F：环境鲁棒性闭环（5 场景 × 5 指令 = 25/25）

判定阈值与 E 完全相同。场景：clear_noon（晴空正午）/ rain（暴雨）/ fog（浓雾）/ night（夜晚）/ glare（日落逆光）。

### per-scene（每场景 5 条指令各 1 trial）

| 场景 | 成功率 | LEFT dyaw (°) | RIGHT dyaw (°) | SPEED_UP 峰值 | SLOW_DOWN 末端 | FORWARD base_v |
|---|---|---|---|---|---|---|
| clear_noon | 5/5 | 61.56* | −34.87 | 2.895 | 0.489 | **5.554*** |
| rain | 5/5 | 36.12 | −34.18 | 2.892 | 0.474 | 0.000 |
| fog | 5/5 | 35.74 | −35.31 | 2.895 | 0.373 | 0.000 |
| night | 5/5 | 36.30 | −33.86 | 2.891 | 0.470 | 0.000 |
| glare | 5/5 | 36.60 | −33.98 | 2.891 | 0.468 | 0.000 |

> `*`：clear_noon 场景的 FORWARD `base_v=5.554`、LEFT `dyaw=61.56°` 是**跨 trial 状态残留**（车辆未完全停下就进入下一 trial，且 clear_noon 排在首场景），非环境鲁棒性信号。剔除 clear_noon 的 LEFT 后，四场景 LEFT 均值 = **36.19±0.39°**，RIGHT 均值 = **−34.33±0.71°**。

### per-command（跨 5 场景）

| 指令 | n | 成功率 | dyaw (°) 均值±std |
|---|---|---|---|
| FORWARD | 5 | 1.00 | −0.912±2.036（含 clear_noon 残留 −4.55） |
| LEFT | 5 | 1.00 | 41.27±11.35（含 clear_noon 残留 61.56） |
| RIGHT | 5 | 1.00 | −34.44±0.63 |
| SPEED_UP | 5 | 1.00 | 0.000±0.000 |
| SLOW_DOWN | 5 | 1.00 | 0.001±0.029 |

**稳健性要点**：SPEED_UP 峰值在所有 5 场景一致为 ≈2.89 m/s（std <0.002），SLOW_DOWN 末端一致为 ≈0.37–0.49 m/s，RIGHT 一致为 ≈−34°，说明天气/光照**不影响控制层执行幅度**。

## 实验 G：Talk2BEV 场景理解（54 条消息，审计 PASS）

| 审计字段 | 值 |
|---|---|
| 状态 | **PASS** |
| 消息总数 / 有效数 | 54 / 54 |
| 唯一图像 hash 数 | 54 |
| 唯一场景 hash 数 | 54 |
| 单一识别模型 | true（DriveTDPAPredictor） |
| `mock` | **false** |
| 模型 checkpoint | `smoke_dpo_single_a10_20260620_161511`（模型文件 2,121,876,280 B ≈ 2.12 GB） |
| 错误数 | 0 |
| 官方 Talk2BEV 上游 entrypoint | **BLOCKED_NOT_EXECUTED**（未执行官方 Talk2BEV 代码库，本实验为 Talk2BEV 兼容的 LVLM 融合） |

### 场景理解质量（抽样 `visual_description`）

5 场景（clear_noon/rain/fog/night/glare）下，模型均正确识别：
- **道路布局**：双黄线分隔的双向车道、道路延伸方向；
- **交通参与者**：人行道行人、公交站附近行人；
- **静态环境**：棕榈树、现代建筑、公交站、清晰天空 / 天气状态；
- **风险陈述**："no immediate hazards / no traffic lights / no obstacles on the road"。

## 定性分析

- **E 执行质量**：动作幅度与指令语义一一对应、且跨 trial 高度稳定（转向 std <0.6°、加减速 std <0.05 m/s），证明 RAT 输出的 YAML 被 Autoware E2E 控制链**忠实且确定地执行**。
- **F 场景稳健性**：4 个非基线场景（rain/fog/night/glare）的动作幅度与基线一致，证明控制层**对感知侧天气干扰不敏感**（因为闭环动作源自语音指令的离散解析，而非依赖天气敏感的感知模块）。
- **G 真实性**：`mock=false` + 单一 2.12GB checkpoint + 54/54 唯一 hash，证明场景理解**确由真实 InternVL 模型在 CARLA 实时图像上产生**，非模板/缓存/回放。

## 边界说明

- **无对照组**：E/F/G 均无"去 BEV / 去动作层 / 去 Talk2BEV / 文本替代语音"的闭环对照，无法隔离任何单组件的闭环贡献。
- **判据宽松**：FORWARD 阈值 `min_v=0.3`、LEFT/RIGHT `min_dyaw=0.1 rad≈5.7°`，而实际动作幅度远超阈值（转向 37°≈6.5×、加减速 1.2–1.8 m/s≈5–7×），100% 成功率含"判据宽松 + 控制层标定良好"的贡献。
- **词汇量极小**：5 个固定离散指令，非自由形式自然语言。
- **F 的 clear_noon 有状态残留**：FORWARD `base_v=5.55`、LEFT `dyaw=61.56°`，且每 (场景,指令) 格 n=1，**无统计功效**做"鲁棒性排序"，只能做"全通过"陈述。
- **G 非官方 Talk2BEV**：`official_talk2bev_upstream_entrypoint_status=BLOCKED_NOT_EXECUTED`；且 E2E 模式下 `/perception/object_recognition/objects` 无发布者（无 GT objects bridge），BEV 对象为空，LVLM 主要靠 CAM_FRONT 单目理解。
- **仿真闭环 ≠ 真实**：CARLA 合成、单 ego、无动态车流、5 秒时域。
