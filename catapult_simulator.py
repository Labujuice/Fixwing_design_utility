import math

def calculate_takeoff_speed(weight, lift_coefficient, air_density, wing_area):
    """
    計算起飛所需速度
    """
    return (weight / (0.5 * air_density * wing_area * lift_coefficient)) ** 0.5

def simulate_catapult(initial_speed, angle_deg, weight, wing_area, lift_coefficient, air_density, thrust, target_speed=None):
    """
    模擬彈射起飛過程
    :param initial_speed: 彈射初速 (m/s)
    :param angle_deg: 彈射角度 (度)
    :param weight: 飛機重量 (N)
    :param wing_area: 翼面積 (m^2)
    :param lift_coefficient: 升力係數 (CL)
    :param air_density: 空氣密度 (kg/m^3)
    :param thrust: 推力 (N)
    :param target_speed: 目標起飛速度 (m/s)，若無則自動計算
    :return: 達到起飛速度所需時間 (s), 水平距離 (m), 對地下滑距離 (m), 起飛速度 (m/s)
    """
    g = 9.81  # 重力加速度 (m/s^2)
    mass = weight / g  # 質量 (kg)
    angle_rad = math.radians(angle_deg)
    v0 = initial_speed * math.cos(angle_rad)  # 水平分量
    v0_vertical = initial_speed * math.sin(angle_rad)  # 垂直分量

    if target_speed is None:
        # 失速速度
        stall_speed = calculate_takeoff_speed(weight, lift_coefficient, air_density, wing_area)
        target_speed = 1.2 * stall_speed  # 起飛速度為失速速度的1.2倍

    # 假設推力恆定，阻力忽略
    acceleration = thrust / mass  # a = F/m

    if acceleration <= 0 or target_speed <= v0:
        return 0, 0, 0, target_speed  # 無法加速或已達到目標速度

    # 運動學公式：v = v0 + a*t  =>  t = (v - v0)/a
    time_needed = (target_speed - v0) / acceleration
    # 水平距離：s = v0*t + 0.5*a*t^2
    horizontal_distance = v0 * time_needed + 0.5 * acceleration * time_needed ** 2

    # 計算對地下滑距離
    # 1. 分別計算初始與最終升力
    lift_0 = 0.5 * air_density * (initial_speed ** 2) * wing_area * lift_coefficient
    lift_1 = 0.5 * air_density * (target_speed ** 2) * wing_area * lift_coefficient
    avg_lift = (lift_0 + lift_1) / 2
    net_vertical_acc = (avg_lift - weight) / mass  # 淨垂直加速度 (近似)
    # 2. 垂直位移
    vertical_displacement = v0_vertical * time_needed + 0.5 * net_vertical_acc * time_needed ** 2
    # 3. 對地距離
    # ground_distance = math.sqrt(horizontal_distance ** 2 + vertical_displacement ** 2)

    # 計算最低高度
    min_height = 0  # 預設起點為0
    if net_vertical_acc != 0:
        t_vertex = -v0_vertical / net_vertical_acc
        if 0 < t_vertex < time_needed:
            vertex_height = v0_vertical * t_vertex + 0.5 * net_vertical_acc * t_vertex ** 2
            min_height = min(0, vertical_displacement, vertex_height)
        else:
            min_height = min(0, vertical_displacement)
    else:
        min_height = min(0, vertical_displacement)

    return time_needed, horizontal_distance, vertical_displacement, target_speed, min_height

if __name__ == "__main__":
    initial_speed = float(input("請輸入彈射初速 (m/s): "))
    angle_deg = float(input("請輸入彈射角度 (度): "))
    weight = float(input("請輸入飛機重量 (N): "))
    wing_area = float(input("請輸入翼面積 (m^2): "))
    lift_coefficient = float(input("請輸入升力係數 (CL): "))
    air_density = float(input("請輸入空氣密度 (kg/m^3): "))
    thrust = float(input("請輸入推力 (N): "))

    t, s_h, s_g, v, min_h = simulate_catapult(initial_speed, angle_deg, weight, wing_area, lift_coefficient, air_density, thrust)
    print(f"達到起飛速度({v:.2f} m/s)所需時間: {t:.2f} 秒")
    print(f"水平距離: {s_h:.2f} 公尺")
    print(f"對地下滑距離: {s_g:.2f} 公尺")
    print(f"最低高度: {min_h:.2f} 公尺")
