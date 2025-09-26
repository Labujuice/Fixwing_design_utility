# Wing Simulator

本專案提供飛機機翼設計與彈射起飛模擬的簡易工具，適合用於基礎航空工程計算與教學。

## 目錄結構

- `wing_simulator.py`：計算機翼面積，根據重量、升力係數、空氣密度與速度。
- `speed_simulator.py`：計算飛行所需速度，根據重量、升力係數、空氣密度、機翼面積與起飛安全倍率。
- `catapult_simulator.py`：模擬彈射起飛過程，計算達到起飛速度所需時間、水平距離、對地下滑距離與最低高度。
- `flight_envelope.py`：計算並繪製飛行包絡線，顯示不同高度下的失速速度與最大速度。

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

### 4. 飛行包絡線繪製（Flight Envelope）
執行：
```bash
python flight_envelope.py
```
依照提示輸入飛機參數（如重量、升力係數、空氣密度、機翼面積等），程式會計算不同高度下的失速速度與最大速度，並繪製出飛行包絡線（V-h Diagram）。

- 藍線：失速速度（V_stall）
- 紅線：最大速度（V_max）
- 綠色區域：安全飛行包絡範圍

可用於分析不同高度下的安全飛行速度範圍。

## 依賴
- Python 3.x
- 無需額外第三方套件

## 版權
本專案僅供學術與教學用途。
