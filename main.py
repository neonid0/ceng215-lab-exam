import matplotlib

try:
    matplotlib.use("QtAgg")
except ImportError:
    print("QtAgg not found. Falling back to default backend.")

R_LOAD = 50e3  # 50 kOhm
C_FILTER = 1e-6  # 1 uF
DT = 1e-4  # 0.1 ms
T_END = 2.0
V_INIT = 3.0


def main(): ...


if __name__ == "__main__":
    main()
