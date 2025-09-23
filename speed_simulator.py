import argparse

def calculate_flight_speed(weight, lift_coefficient, air_density, wing_area, takeoff_safe=1.0):
    """
    計算飛行速度
    :param weight: 重量 (N)
    :param lift_coefficient: 升力係數 (CL)
    :param air_density: 空氣密度 (kg/m^3)
    :param wing_area: 機翼面積 (m^2)
    :param takeoff_safe: 起飛安全倍率 (float)
    :return: 飛行速度 (m/s)
    """
    speed = (weight / (0.5 * air_density * wing_area * lift_coefficient)) ** 0.5
    return speed * takeoff_safe

def main():
    parser = argparse.ArgumentParser(
        description="計算飛行速度。可用選項帶入參數，或互動式輸入。"
    )
    parser.add_argument('--weight', type=float, help='重量 (N)')
    parser.add_argument('--cl', type=float, help='升力係數 (CL)')
    parser.add_argument('--density', type=float, help='空氣密度 (kg/m^3)')
    parser.add_argument('--area', type=float, help='機翼面積 (m^2)')
    parser.add_argument('--takeoff_safe', type=float, default=1.0, help='起飛安全倍率 (預設1.0)')

    args = parser.parse_args()

    if args.weight is not None:
        weight = args.weight
    else:
        weight = float(input("請輸入重量 (N): "))

    if args.cl is not None:
        lift_coefficient = args.cl
    else:
        lift_coefficient = float(input("請輸入升力係數 (CL): "))

    if args.density is not None:
        air_density = args.density
    else:
        air_density = float(input("請輸入空氣密度 (kg/m^3): "))

    if args.area is not None:
        wing_area = args.area
    else:
        wing_area = float(input("請輸入機翼面積 (m^2): "))

    takeoff_safe = args.takeoff_safe

    speed = calculate_flight_speed(weight, lift_coefficient, air_density, wing_area, takeoff_safe)
    print(f"計算得到的飛行速度為: {speed:.2f} m/s (起飛安全倍率: {takeoff_safe})")

if __name__ == "__main__":
    main()
