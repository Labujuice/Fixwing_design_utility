# Wing Simulator

本專案提供飛機機翼設計與彈射起飛模擬的簡易工具，適合用於基礎航空工程計算與教學。

## 目錄結構

- `wing_simulator.py`：計算機翼面積，根據重量、升力係數、空氣密度與速度。
- `speed_simulator.py`：計算飛行所需速度，根據重量、升力係數、空氣密度、機翼面積與起飛安全倍率。
- `catapult_simulator.py`：模擬彈射起飛過程，計算達到起飛速度所需時間、水平距離、對地下滑距離與最低高度。
- `flight_envelope.py`：計算並繪製飛行包絡線與多種關鍵飛行性能圖表。

## 使用方式

### 1. 計算機翼面積
執行：
```bash
python wing_simulator.py
```
依照提示輸入：
- 重量 (N)
- 升力係數 (CL)
- 空氣密度 (kg/m^3)
- 速度 (m/s)

### 2. 計算飛行速度
執行：
```bash
python speed_simulator.py [options]
```
可用選項帶入參數，或依照提示輸入：
- `--weight`：重量 (N)
- `--cl`：升力係數 (CL)
- `--density`：空氣密度 (kg/m^3)
- `--area`：機翼面積 (m^2)
- `--takeoff_safe`：起飛安全倍率（預設 1.0）

範例（帶入所有參數）：
```bash
python speed_simulator.py --weight 100 --cl 1.2 --density 1.225 --area 2.5 --takeoff_safe 1.1
```
或直接執行，依提示輸入數值。

查看說明：
```bash
python speed_simulator.py --help
```

### 3. 彈射起飛模擬
執行：
```bash
python catapult_simulator.py
```
依照提示輸入：
- 彈射初速 (m/s)
- 彈射角度 (度)
- 飛機重量 (N)
- 翼面積 (m^2)
- 升力係數 (CL)
- 空氣密度 (kg/m^3)
- 推力 (N)

輸出內容包含：
- 達到起飛速度所需時間
- 水平距離
- 對地下滑距離（以垂直位移為主）
- 最低高度（模擬過程中最低點）

### 4. 飛行包絡線與性能分析 (Flight Envelope & Performance)
執行：
```bash
python flight_envelope.py
```

此腳本會產生多張圖表，視覺化飛機的各項性能指標。所有參數（如重量、翼面積、氣動係數等）皆可在腳本開頭直接修改。

**產生的圖表包含：**

1.  **飛行包絡線 (Flight Envelope, V-h Diagram)**
    - 顯示不同高度下的失速速度、最大速度與安全飛行區域。
    - 額外繪製了三種俯衝角度（-30°, -45°, -60°）下的終端速度曲線。

2.  **巡航推力需求圖 (Cruise Speed vs. Required Thrust)**
    - 在數個代表性高度下，繪製維持平飛所需的推力與對應巡航速度的關係。

3.  **俯衝加速度圖 (Acceleration vs. Speed during Dive)**
    - 模擬飛機在不同俯衝角度下，其飛行路徑加速度隨速度變化的情況。

4.  **俯衝改出G力圖 (Potential G-force during Pull-out)**
    - 分析在特定俯衝速度下，執行對稱拉升（Symmetric Pull-up）或帶坡度轉彎（Banked Turn）時所產生的潛在G力（負載因子）。

5.  **爬升率圖 (Rate of Climb vs. Velocity)**
    - 顯示在海平面高度，飛機的爬升率隨速度的變化曲線。
    - 圖中標示了可達到最大爬升率的速度（Vy）。

6.  **升阻比圖 (L/D Ratio vs. Velocity)**
    - 顯示在海平面高度，飛機的氣動效率（升阻比）隨速度的變化。
    - 圖中標示了可達到最大升阻比的最佳滑翔速度。

## 依賴
- Python 3.x
- Matplotlib
- NumPy

## 版權
本專案僅供學術與教學用途。