import numpy as np
import matplotlib.pyplot as plt

# --- 飛機和環境參數設定 ---

# 假設重量 (需要您提供，這裡使用範例值)
# W = 飛機質量 * 重力加速度
M_aircraft = 20.0  # kg (飛機質量)
g = 9.81            # m/s^2 (重力加速度)
W = M_aircraft * g  # N (飛機重量)

# 機翼參數
S = 1.0            # m^2 (機翼面積)
AR = 15            # 弦長比 (Aspect Ratio, 翼展^2 / 面積)

# 空氣動力學參數 (可根據設計填寫)
CL_max = 1.5      # 最大升力係數 (用於計算最小速度 V_stall)
# 各部位零升力阻力係數
CD_0_wing = 0.012     # 機翼二維阻力
CD_0_fuselage = 0.015 # 機身阻力
CD_0_tail = 0.006     # 尾翼阻力
CD_0_misc = 0.007     # 其他/附加阻力（天線、起落架等）
CD_0_total = CD_0_wing + CD_0_fuselage + CD_0_tail + CD_0_misc
# 奧斯瓦爾德效率因子 (Oswald efficiency factor)
e = 0.8
# 阻力係數公式 CD = CD_0_total + k * CL^2
k = 1.0 / (np.pi * AR * e) # 誘導阻力因子

# 引擎參數
T_static_sea_level = 7.0 * g # N (地面靜推力)

# 飛行包絡線計算範圍
H_max = 5000.0       # m (預計使用的總高度)
altitudes = np.linspace(0, H_max, 50) # 50 個計算高度點

# --- 標準大氣模型 (簡化 ISA 模型) ---
rho_sl = 1.225      # kg/m^3 (海平面大氣密度)
T_sl = 288.15       # K (海平面溫度)
a_T = -0.0065       # K/m (溫度隨高度的梯度)
gamma = 1.4         # 熱容比 (for air)
R = 287.05          # 氣體常數 (J/kg·K)

def speed_of_sound(h):
    """計算給定高度的音速"""
    if h <= 11000:
        T_h = T_sl + a_T * h
        return np.sqrt(gamma * R * T_h)
    else:
        # 假設在平流層溫度恆定
        T_11km = T_sl + a_T * 11000
        return np.sqrt(gamma * R * T_11km)

def thrust_model(T_static_sl, altitude, velocity):
    """
    優化後的推力模型，同時考慮高度(密度)與速度(馬赫數)的影響。
    T = T_sl * (rho/rho_sl)^n * (1 + c1*M + c2*M^2)
    """
    density_ratio = rho_h(altitude) / rho_sl
    mach_number = velocity / speed_of_sound(altitude)
    # 經驗係數，此處設定為模擬典型高旁通比渦扇引擎，推力隨速度略微下降
    c1, c2 = -0.2, 0.1
    mach_correction = 1 + c1 * mach_number + c2 * mach_number**2
    T_available = T_static_sl * np.power(density_ratio, 0.7) * mach_correction
    return T_available

def rho_h(h):
    # 對流層 (h < 11000m) 的密度計算
    if h <= 11000:
        T_h = T_sl + a_T * h
        p_h = 101325.0 * (T_h / T_sl) ** (-g / (a_T * 287.05)) # 壓力
        rho = p_h / (287.05 * T_h) # 理想氣體定律
        return rho
    else:
        # 超出對流層的簡化處理 (實際應使用標準大氣表)
        return rho_sl * 0.25 # 粗略估計

# --- 飛行包絡線計算主體 ---

V_stall_list = []
V_max_list = []

for h in altitudes:
    # 獲取當前高度的空氣密度
    rho = rho_h(h)

    # 1. 計算失速速度 (左邊界)
    # V_stall = sqrt( (2 * W) / (rho * S * CL_max) )
    V_stall = np.sqrt((2 * W) / (rho * S * CL_max))
    V_stall_list.append(V_stall)

    # 2. 計算最大速度 (右邊界)
    # T_available = D = 1/2 * rho * V^2 * S * CD
    # 這是一個數值求解問題：T_available(V, h) = Drag(V, h)
    
    # 尋找平衡點的函數： f(V) = T_available - Drag = 0
    def equation_of_motion(V, h):
        if V == 0: return -1e9 # 避免除以零
        
        # a. 計算升力係數 CL
        CL = W / (0.5 * rho_h(h) * V**2 * S)
        
        # b. 計算阻力係數 CD (假設 CL 尚未超過線性範圍)
        CD = CD_0_total + k * CL**2
        
        # c. 計算阻力 D
        Drag = 0.5 * rho_h(h) * V**2 * S * CD
        
        # d. 計算可用推力 T_available
        T_available = thrust_model(T_static_sea_level, h, V)
        
        # e. 返回推力盈餘 (正值表示加速，零點為極限速度)
        return T_available - Drag

    # 使用數值方法 (例如簡單的二分法或根查找) 尋找 V_max
    # 這裡採用簡單的迭代搜索
    V_max_search = 1000.0 # 初始搜索上限
    V_step = 1.0          # 搜索步長
    V_current = V_stall * 1.05 # 從略高於失速速度開始搜索
    
    # 尋找推力盈餘變成負值 (阻力 > 推力) 的點
    while equation_of_motion(V_current, h) > 0 and V_current < V_max_search:
        V_current += V_step
    
    V_max_list.append(V_current)
    
# --- 繪圖 ---
plt.figure(figsize=(10, 6))

# 將速度轉換為 km/h 或 kts 方便閱讀
V_stall_kmh = np.array(V_stall_list) * 3.6
V_max_kmh = np.array(V_max_list) * 3.6

# 繪製包絡線的邊界
plt.plot(V_stall_kmh, altitudes / 1000, color='blue', linestyle='--', label='min velocity (stall) $V_{stall}$')
plt.plot(V_max_kmh, altitudes / 1000, color='red', linestyle='--', label='max velocity $V_{max}$')

# 填充包絡線區域
plt.fill_betweenx(altitudes / 1000, V_stall_kmh, V_max_kmh, color='green', alpha=0.3, 
                 label='Flight Envelope')

# --- Dive Speed 計算 ---
def calc_dive_speed(h0, V0, dive_angle_deg):
    """
    h0: 初始高度 (m)
    V0: 初始速度 (m/s)
    dive_angle_deg: 俯衝角度 (負值, ex: -30)
    return: 到達地表時的最大速度 (m/s)
    """
    dt = 0.05  # 時間步長 (s)
    h = h0
    V = V0
    theta = np.radians(dive_angle_deg)
    while h > 0:
        rho = rho_h(h)
        CL = 0.0  # 俯衝時假設升力近似為零
        CD = CD_0_total + k * CL**2
        D = 0.5 * rho * V**2 * S * CD
        T = thrust_model(T_static_sea_level, h, V)
        # 速度分量沿飛行方向
        a = (T - D + W * np.sin(-theta)) / (M_aircraft)
        V += a * dt
        h -= V * np.sin(-theta) * dt
        if V < 0: V = 0.1
    return V

# 計算三條 dive speed 曲線
V_dive_30 = []
V_dive_45 = []
V_dive_60 = []
for i, h in enumerate(altitudes):
    V0 = V_stall_list[i]
    V_dive_30.append(calc_dive_speed(h, V0, -30))
    V_dive_45.append(calc_dive_speed(h, V0, -45))
    V_dive_60.append(calc_dive_speed(h, V0, -60))
V_dive_30_kmh = np.array(V_dive_30) * 3.6
V_dive_45_kmh = np.array(V_dive_45) * 3.6
V_dive_60_kmh = np.array(V_dive_60) * 3.6

# 在繪圖區塊加上 dive speed 曲線
plt.plot(V_dive_30_kmh, altitudes / 1000, color='orange', linestyle='-', label='Dive speed -30°')
plt.plot(V_dive_45_kmh, altitudes / 1000, color='purple', linestyle='-', label='Dive speed -45°')
plt.plot(V_dive_60_kmh, altitudes / 1000, color='brown', linestyle='-', label='Dive speed -60°')

plt.title('Flight Envelope (V-h Diagram)')
plt.xlabel('velocity (km/h)')
plt.ylabel('altitude (km)')
plt.grid(True)
plt.legend()
plt.ylim(0, H_max / 1000 * 1.1)
plt.show(block=False)

# --- 速度-推力曲線 (不同高度下的巡航速度 vs 推力) ---
# 選取 H_max 五等分的高度（包含地表與頂端）
n_levels = 5
alt_levels = np.linspace(0, H_max, n_levels)

# 優化：反向計算。掃描速度，計算所需推力(阻力)，而非掃描推力找速度。
def calculate_required_thrust(h, V):
    """在給定高度h和速度V下，計算平飛所需的推力(等於阻力)。"""
    if V <= 0:
        return np.nan
    rho = rho_h(h)
    CL = W / (0.5 * rho * V**2 * S)
    # 如果計算出的CL超過CL_max，代表此速度低於失速速度，物理上不可行
    if CL > CL_max:
        return np.nan
    CD = CD_0_total + k * CL**2
    Drag = 0.5 * rho * V**2 * S * CD
    return Drag

# 繪圖
plt.figure(figsize=(10, 6))
colors = plt.cm.viridis(np.linspace(0, 1, len(alt_levels)))

for idx, h in enumerate(alt_levels):
    # 1. 確定該高度的速度掃描範圍
    V_stall_h = np.sqrt((2 * W) / (rho_h(h) * S * CL_max))
    # 從V_max_list中找到對應高度的最大速度作為掃描上限
    V_max_h = np.interp(h, altitudes, V_max_list)
    V_scan = np.linspace(V_stall_h, V_max_h, 100) # 掃描至該高度的最大速度截止點

    # 2. 計算每個速度點所需的推力
    T_required = [calculate_required_thrust(h, V) for V in V_scan]

    # 3. 繪製所需推力曲線
    plt.plot(T_required, V_scan, color=colors[idx], label=f'h = {int(h)} m (Required)')

    # 4. 標示出該高度的最大可用推力
    #    此處的 V_max_h 是推力與阻力曲線的交點，對應的推力即為最大可用推力
    T_max_at_h = calculate_required_thrust(h, V_max_h)
    if T_max_at_h is not None and not np.isnan(T_max_at_h):
        plt.axvline(x=T_max_at_h, color=colors[idx], linestyle='--', linewidth=1.5, 
                    label=f'Max Thrust @ {int(h)} m')

plt.xlabel('Required Thrust (N)')
plt.ylabel('Cruise speed (m/s)')
plt.title('Cruise Speed vs. Required Thrust at Selected Altitudes')
plt.grid(True)
# 將圖例放到圖外右側
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.show(block=True)

# 由於您的問題涉及工程計算的複雜性，
# 在實際應用中，會需要一個更精確的標準大氣模型和推力模型。