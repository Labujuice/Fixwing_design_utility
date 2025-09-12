def calculate_wing_area(weight, lift_coefficient, air_density, velocity):
    """
    計算機翼面積
    :param weight: 重量 (N)
    :param lift_coefficient: 升力係數 (CL)
    :param air_density: 空氣密度 (kg/m^3)
    :param velocity: 速度 (m/s)
    :return: 機翼面積 (m^2)
    """
    wing_area = weight / (0.5 * air_density * velocity ** 2 * lift_coefficient)
    return wing_area

# 範例輸入
weight = float(input("請輸入重量 (N): "))
lift_coefficient = float(input("請輸入升力係數 (CL): "))
air_density = float(input("請輸入空氣密度 (kg/m^3): "))
velocity = float(input("請輸入速度 (m/s): "))

area = calculate_wing_area(weight, lift_coefficient, air_density, velocity)
print(f"計算得到的機翼面積為: {area:.2f} m^2")