from decimal import Decimal, getcontext

# ====================== 超高精度配置 ======================
getcontext().prec = 60   # 底层运算60位精度
OUTPUT_DECIMAL = 50      # 固定输出50位小数
C = Decimal("299792458") # 真空光速 精确定义值 m/s

def lorentz_full_calc(v_input: str):
    # 读取速度并校验
    v = Decimal(v_input)
    if v >= C:
        raise ValueError("错误：物体速度不可达到或超过真空光速！")
    if v < 0:
        raise ValueError("错误：请输入非负速率大小")

    # 基础相对论参数
    beta = v / C                    # 速度因子 β = v/c
    beta_sq = beta * beta           # β² = v²/c²
    gamma = Decimal(1) / ((Decimal(1) - beta_sq).sqrt())  # 洛伦兹因子 γ

    # 核心相对论系数
    time_dilation_ratio = Decimal(1) / gamma    # 固有时/坐标时 Δτ/Δt
    length_contraction_ratio = Decimal(1) / gamma # 长度收缩 L/L0

    # 【你最需要的核心结果】地球经过1秒，运动物体流逝的时间
    earth_1s_proper_time = time_dilation_ratio * Decimal("1.0")

    # 微小差值（专业分析用）
    gamma_minus_1 = gamma - Decimal("1.0")

    return {
        "v": v,
        "beta": beta,
        "beta_sq": beta_sq,
        "gamma": gamma,
        "gamma-1": gamma_minus_1,
        "time_ratio": time_dilation_ratio,
        "length_ratio": length_contraction_ratio,
        "earth_1s_obj_time": earth_1s_proper_time
    }

if __name__ == "__main__":
    print("=" * 90)
    print("          超高精度 狭义相对论计算器｜洛伦兹因子 · 时间膨胀 · 长度收缩")
    print("=" * 90)
    print("【参考系规则】")
    print("  地球 = 静止惯性参考系（坐标时）")
    print("  运动物体 = 动参考系（固有时，自身真实时间）")
    print("【核心结论前置】运动物体时间永远比地球时间流逝更慢")
    print("=" * 90)

    while True:
        print("\n请输入物体速度 (单位：m/s)，输入 q 退出程序")
        inp = input("速度：").strip()
        if inp.lower() == "q":
            print("\n程序结束")
            break

        try:
            res = lorentz_full_calc(inp)

            print("\n—————————— 【基础运动参数】——————————")
            print(f"物体运动速率 v = {res['v']} m/s")
            print(f"速度因子 β = v/c = {res['beta']:.15e}")
            print(f"速度平方比 β² = v²/c² = {res['beta_sq']:.15e}")

            print("\n—————————— 【专业核心物理量｜50位超高精度】——————————")
            print(f"洛伦兹因子 γ = {res['gamma']:.50f}")
            print(f"γ 偏离1的增量 = {res['gamma-1']:.50f}")

            print("\n—————————— 【时间膨胀效应｜通俗+专业双解释】——————————")
            print(f"时间膨胀比（物体时间 / 地球时间）= {res['time_ratio']:.50f}")
            print(f"✅ 【最直观结果】地球时间流逝 1.0 秒")
            print(f"✅ 运动物体真实流逝时间 = {res['earth_1s_obj_time']:.50f} 秒")

            print("\n—————————— 【长度收缩效应】——————————")
            print(f"长度收缩比（运动长度 / 静止长度）= {res['length_ratio']:.50f}")

            print("\n—————————— 【物理通俗释义】——————————")
            print("1. 洛伦兹因子 γ 永远 ≥ 1，速度越快 γ 越大")
            print("2. 时间膨胀：地球过1秒，高速物体不足1秒，运动者时间变慢")
            print("3. 低速场景（如旅行者1号）γ≈1，效应极微弱，但真实存在")
            print("4. 固有时是所有参考系中最短的时间，绝对真实")

            print("\n" + "=" * 90)

        except Exception as e:
            print(f"\n输入异常：{str(e)}，请输入合法数字！")
