import tkinter as tk
from tkinter import ttk

def calculate_profit(*args):
    try:
        V = float(entry_vars["名义资金 V (USDT)"].get())
        S_open = float(entry_vars["当前价差 % (S_open)"].get())
        S_close = float(entry_vars["假设收敛价差 % (S_close)"].get())

        low_rate = float(entry_vars["价低方资金费率 %/结算"].get())
        low_hours = float(entry_vars["价低方结算周期 (小时)"].get())
        high_rate = float(entry_vars["价高方资金费率 %/结算"].get())
        high_hours = float(entry_vars["价高方结算周期 (小时)"].get())

        hold_hours = float(entry_vars["持仓时长 (小时)"].get())
        fee_low = float(entry_vars["价低方手续费 % (单次)"].get())
        fee_high = float(entry_vars["价高方手续费 % (单次)"].get())
        slippage = float(entry_vars["滑点估计 %"].get())

        # === Calculation ===
        price_spread = S_open - S_close
        n_low = hold_hours / low_hours
        n_high = hold_hours / high_hours
        funding_diff = high_rate * n_high - low_rate * n_low
        total_fee = 2 * (fee_low + fee_high)
        net_percent = price_spread + funding_diff - total_fee - slippage
        profit_usdt = V * net_percent / 100

        label_result.config(
            text=(
                f"💰 预计利润: {profit_usdt:.4f} USDT\n"
                f"📊 净收益率: {net_percent:.4f}%\n\n"
                f"价差收益: {price_spread:.4f}%\n"
                f"资金费差: {funding_diff:.4f}%\n"
                f"手续费合计: {total_fee:.4f}%"
            ),
            foreground="white"   # ✅ 改为白色
        )
    except ValueError:
        label_result.config(text="⚠️ 输入格式错误，请检查数值。", foreground="red")

root = tk.Tk()
root.title("跨所套利收益实时计算器（价低方做多 / 价高方做空）")

mainframe = ttk.Frame(root, padding="12")
mainframe.grid(row=0, column=0, sticky="nsew")

fields = [
    ("名义资金 V (USDT)", "100"),
    ("当前价差 % (S_open)", "3.0"),
    ("假设收敛价差 % (S_close)", "0.0"),
    ("价低方资金费率 %/结算", "-1.2145"),
    ("价低方结算周期 (小时)", "4"),
    ("价高方资金费率 %/结算", "0.0"),
    ("价高方结算周期 (小时)", "1"),
    ("持仓时长 (小时)", "4"),
    ("价低方手续费 % (单次)", "0.05"),
    ("价高方手续费 % (单次)", "0.055"),
    ("滑点估计 %", "0.0")
]

entry_vars = {}
for i, (label, default) in enumerate(fields):
    ttk.Label(mainframe, text=label).grid(row=i, column=0, sticky="w")
    var = tk.StringVar(value=default)
    entry = ttk.Entry(mainframe, textvariable=var)
    entry.grid(row=i, column=1, sticky="ew")
    entry_vars[label] = var
    # 实时更新
    var.trace_add("write", calculate_profit)

# 输出结果（白色文字）
label_result = ttk.Label(
    mainframe,
    text="",
    font=("Helvetica", 12, "bold"),
    justify="left",
    foreground="white"   # ✅ 白色文字
)
label_result.grid(row=len(fields)+1, column=0, columnspan=2, pady=(10, 0))

# 初次计算
calculate_profit()

root.mainloop()
