def calculate_flight_speed(weight, lift_coefficient, air_density, wing_area):
    """
    計算飛行速度
    :param weight: 重量 (N)
    :param lift_coefficient: 升力係數 (CL)
    :param air_density: 空氣密度 (kg/m^3)
    :param wing_area: 機翼面積 (m^2)
    :return: 飛行速度 (m/s)
    """
    speed = (weight / (0.5 * air_density * wing_area * lift_coefficient)) ** 0.5
    return speed

# 範例輸入
weight = float(input("請輸入重量 (N): "))
lift_coefficient = float(input("請輸入升力係數 (CL): "))
air_density = float(input("請輸入空氣密度 (kg/m^3): "))
wing_area = float(input("請輸入機翼面積 (m^2): "))

speed = calculate_flight_speed(weight, lift_coefficient, air_density, wing_area)
print(f"計算得到的飛行速度為: {speed:.2f} m/s")
