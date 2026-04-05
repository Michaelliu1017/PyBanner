import os
import time
import random
import datetime
import platform

# ─────────────────────────────────────────────
# banner(para) — ASCII logo
#   0 : 噪点浮现效果 (orange █)
#   1 : 菱形字符 (orange ◆)
#   2 : 原版星号 (*)
#   3 : 噪点浮现效果 ◆ (orange  ◆)
#   4 : 颜色渐变

# ─────────────────────────────────────────────
# 忠橙\o/  "\033[38;5;202m"
# 亮橙：   "\033[38;5;208m"

def banner(para=0):
    seed = "00080909000409490251409504612094067110920007719200086183000950930009923300095273000940940008454500080909"
    #**********************
    #*   1   噪点浮现效果   *
    #**********************
    if para == 0:
        # ── 噪点浮现效果 ──────────────────────────────
        ORANGE="\033[38;5;202m" # "\033[38;5;208m" brighter
        DIM, RESET ="\033[38;5;202m", "\033[0m"

       ## noise = ["░", "▒", "▓", "·", ":", " "]
        noise = ["░",  "▒", "▒"," "]

        lines = []
        for i in range(13):
            s = int(seed[-8*(i+1):-8*i or None])
            lines.append("".join(" "*(s//10**j%10) + "█"*(s//10**(j+1)%10) for j in range(0,8,2)))

        width = max(len(l) for l in lines)

        for frame in range(20):
            output = []
            for line in lines:
                row = ""
                for ch in line.ljust(width):
                    if ch == "█":
                        if random.random() < frame / 19:
                            row += f"{ORANGE}█{RESET}"
                        else:
                            row += f"{DIM}{random.choice(noise)}{RESET}"
                    else:
                        if random.random() < (1 - frame / 19) * 0.4:
                            row += f"{DIM}{random.choice(noise)}{RESET}"
                        else:
                            row += " "
                output.append(row)

            print("\n".join(output))
            time.sleep(0.06)
            print(f"\033[{len(lines)}A", end="")

        for line in lines:
            s_clean = "".join(f"{ORANGE}█{RESET}" if c == "█" else " " for c in line.ljust(width))
            print(s_clean)
    # **********************
    # *     2   菱形字符    *
    # **********************
    elif para == 1:
        # ── 菱形字符 ─────────────────────────────────
        ORANGE, RESET = "\033[38;5;202m", "\033[0m"
        for i in range(13):
            s = int(seed[-8*(i+1):-8*i or None])
            line = "".join(" "*(s//10**j%10) + f"{ORANGE}◆{RESET}"*(s//10**(j+1)%10) for j in range(0,8,2))
            print(line)
            time.sleep(0.05)
    # **********************
    # *     3    原版       *
    # **********************
    elif para == 2:
        # ── 原版星号 ─────────────────────────────────
        for i in range(13):
            s = int(seed[-8*(i+1):-8*i or None])
            line = "".join(" "*(s//10**j%10) + "*"*(s//10**(j+1)%10) for j in range(0,8,2))
            print(line)
            time.sleep(0.05)
    # **********************
    # *  4 噪点浮现效果 ◆    *
    # **********************
    elif para ==3 :
        # ── 噪点浮现效果 ──────────────────────────────
        ORANGE, DIM, RESET = "\033[38;5;208m", "\033[38;5;202m", "\033[0m"
        noise = ["░", "▒", "▓", "·", ":", " "]

        lines = []
        for i in range(13):
            s = int(seed[-8 * (i + 1):-8 * i or None])
            lines.append("".join(" " * (s // 10 ** j % 10) + "◆" * (s // 10 ** (j + 1) % 10) for j in range(0, 8, 2)))

        width = max(len(l) for l in lines)

        for frame in range(20):
            output = []
            for line in lines:
                row = ""
                for ch in line.ljust(width):
                    if ch == "◆":
                        if random.random() < frame / 19:
                            row += f"{ORANGE}◆{RESET}"
                        else:
                            row += f"{DIM}{random.choice(noise)}{RESET}"
                    else:
                        if random.random() < (1 - frame / 19) * 0.4:
                            row += f"{DIM}{random.choice(noise)}{RESET}"
                        else:
                            row += " "
                output.append(row)

            print("\n".join(output))
            time.sleep(0.06)
            print(f"\033[{len(lines)}A", end="")

        for line in lines:
            s_clean = "".join(f"{ORANGE}◆{RESET}" if c == "◆" else " " for c in line.ljust(width))
            print(s_clean)
    # **********************
    # *     5    渐变色     *
    # **********************
    elif para == 4:
        # 橙色梯度从暗到亮：52 → 166 → 202 → 208
        GRADIENT = [
            "\033[38;5;52m",  # 极暗棕红
            "\033[38;5;88m",  # 暗红
            "\033[38;5;130m",  # 暗橙
            "\033[38;5;166m",  # 中橙
            "\033[38;5;202m",  # 标准橙
            "\033[38;5;208m",  # 亮橙
        ]
        RESET = "\033[0m"

        lines = []
        for i in range(13):
            s = int(seed[-8 * (i + 1):-8 * i or None])
            lines.append("".join(" " * (s // 10 ** j % 10) + "█" * (s // 10 ** (j + 1) % 10) for j in range(0, 8, 2)))

        width = max(len(l) for l in lines)
        steps = len(GRADIENT)

        for frame in range(steps):
            color = GRADIENT[frame]
            output = []
            for line in lines:
                row = "".join(f"{color}█{RESET}" if c == "█" else " " for c in line.ljust(width))
                output.append(row)
            print("\n".join(output))
            time.sleep(0.08)
            print(f"\033[{len(lines)}A", end="")

        # 最终定格亮橙
        for line in lines:
            row = "".join(f"\033[38;5;208m█{RESET}" if c == "█" else " " for c in line.ljust(width))
            print(row)
    # **********************
    # *     6   渐变色 ◆    *
    # **********************
    elif para == 5:
        # 橙色梯度从暗到亮：52 → 166 → 202 → 208
        GRADIENT = [
            "\033[38;5;52m",  # 极暗棕红
            "\033[38;5;88m",  # 暗红
            "\033[38;5;130m",  # 暗橙
            "\033[38;5;166m",  # 中橙
            "\033[38;5;202m",  # 标准橙
            "\033[38;5;208m",  # 亮橙
        ]
        RESET = "\033[0m"

        lines = []
        for i in range(13):
            s = int(seed[-8 * (i + 1):-8 * i or None])
            lines.append("".join(" " * (s // 10 ** j % 10) + "◆" * (s // 10 ** (j + 1) % 10) for j in range(0, 8, 2)))

        width = max(len(l) for l in lines)
        steps = len(GRADIENT)

        for frame in range(steps):
            color = GRADIENT[frame]
            output = []
            for line in lines:
                row = "".join(f"{color}◆{RESET}" if c == "◆" else " " for c in line.ljust(width))
                output.append(row)
            print("\n".join(output))
            time.sleep(0.08)
            print(f"\033[{len(lines)}A", end="")

        # 最终定格亮橙
        for line in lines:
            row = "".join(f"\033[38;5;208m◆{RESET}" if c == "◆" else " " for c in line.ljust(width))
            print(row)
    # **********************
    # *     7    从上到下   *
    # **********************
    elif para == 6:
        ORANGE, DIM, RESET = "\033[38;5;202m", "\033[38;5;202m", "\033[0m"

        lines = []
        for i in range(13):
            s = int(seed[-8 * (i + 1):-8 * i or None])
            lines.append("".join(" " * (s // 10 ** j % 10) + "█" * (s // 10 ** (j + 1) % 10) for j in range(0, 8, 2)))

        width = max(len(l) for l in lines)
        H = len(lines)

        # 从上往下逐行揭开
        for reveal in range(H + 1):
            output = []
            for row_i, line in enumerate(lines):
                row = ""
                for ch in line.ljust(width):
                    if ch == "█":
                        if row_i < reveal:
                            row += f"{ORANGE}█{RESET}"
                        else:
                            row += f"{DIM} {RESET}"
                    else:
                        row += " "
                output.append(row)
            print("\n".join(output))
            time.sleep(0.08)
            print(f"\033[{H}A", end="")

        for line in lines:
            print("".join(f"{ORANGE}█{RESET}" if c == "█" else " " for c in line.ljust(width)))

    # **********************
    # *     8  扫描    *
    # **********************
    elif para == 7:

        #ORANGE="\033[38;5;208m" # Bright Orange
        ORANGE="\033[38;5;202m" # Mid Orange
        SCAN="\033[38;5;226m" # yellow
        RESET ="\033[0m"

        lines = []
        for i in range(13):
            s = int(seed[-8 * (i + 1):-8 * i or None])
            lines.append("".join(" " * (s // 10 ** j % 10) + "█" * (s // 10 ** (j + 1) % 10) for j in range(0, 8, 2)))

        width = max(len(l) for l in lines)
        H = len(lines)

        # 扫描线从上到下扫两遍
        for _ in range(1):
            for scan_row in range(H):
                output = []
                for row_i, line in enumerate(lines):
                    row = ""
                    for ch in line.ljust(width):
                        if ch == "█":
                            if row_i == scan_row:
                                row += f"{SCAN}█{RESET}"  # 扫描线亮黄
                            elif row_i < scan_row:
                                row += f"{ORANGE}█{RESET}"  # 已扫描橙色
                            else:
                                row += f"\033[38;5;238m█{RESET}"  # 未扫描暗色
                        else:
                            row += " "
                    output.append(row)
                print("\n".join(output))
                time.sleep(0.06)
                print(f"\033[{H}A", end="")

        for line in lines:
            print("".join(f"{ORANGE}█{RESET}" if c == "█" else " " for c in line.ljust(width)))



    # **********************
    # *     9  — 波浪闪烁  *
    # **********************
    elif para == 8:
        import math
        RESET = "\033[0m"

        lines = []
        for i in range(13):
            s = int(seed[-8 * (i + 1):-8 * i or None])
            lines.append("".join(" " * (s // 10 ** j % 10) + "█" * (s // 10 ** (j + 1) % 10) for j in range(0, 8, 2)))

        width = max(len(l) for l in lines)
        H = len(lines)

        # 橙色梯度
        palette = [166, 172, 178, 202, 208, 214, 220, 214, 208, 202]
        # 灰色梯度
        #palette = [236, 238, 240, 242, 244, 246, 244, 242, 240, 238]
        for frame in range(30):
            print(f"\033[{H}A" if frame > 0 else "", end="")
            for row_i, line in enumerate(lines):
                row = ""
                for col_i, ch in enumerate(line.ljust(width)):
                    if ch == "█":
                        wave = math.sin(frame * 0.1 + col_i * 0.4 + row_i * 0.5)
                        idx = int((wave + 1) / 2 * (len(palette) - 1))
                        color = f"\033[38;5;{palette[idx]}m"
                        row += f"{color}█{RESET}"
                    else:
                        row += " "
                print(row)
            time.sleep(0.06)

        # 定格在最后一帧波动的样子（不重置为纯色）
        last_frame = 29
        print(f"\033[{H}A", end="")
        for row_i, line in enumerate(lines):
            row = ""
            for col_i, ch in enumerate(line.ljust(width)):
                if ch == "█":
                    wave = math.sin(last_frame * 0.3 + col_i * 0.4 + row_i * 0.5)
                    idx = int((wave + 1) / 2 * (len(palette) - 1))
                    color = f"\033[38;5;{palette[idx]}m"
                    row += f"{color}█{RESET}"
                else:
                    row += " "
            print(row)

        # **********************
        # *     10  — 波浪闪烁  *
        # **********************
    elif para == 9:
        import math
        RESET = "\033[0m"

        lines = []
        for i in range(13):
            s = int(seed[-8 * (i + 1):-8 * i or None])
            lines.append("".join(" " * (s // 10 ** j % 10) + "█" * (s // 10 ** (j + 1) % 10) for j in range(0, 8, 2)))

        width = max(len(l) for l in lines)
        H = len(lines)

        # 橙色梯度
        # palette = [166, 172, 178, 202, 208, 214, 220, 214, 208, 202]
        # 灰色梯度
        palette = [236, 238, 240, 242, 244, 246, 244, 242, 240, 238]
        for frame in range(30):
            print(f"\033[{H}A" if frame > 0 else "", end="")
            for row_i, line in enumerate(lines):
                row = ""
                for col_i, ch in enumerate(line.ljust(width)):
                    if ch == "█":
                        wave = math.sin(frame * 0.1 + col_i * 0.4 + row_i * 0.5)
                        idx = int((wave + 1) / 2 * (len(palette) - 1))
                        color = f"\033[38;5;{palette[idx]}m"
                        row += f"{color}█{RESET}"
                    else:
                        row += " "
                print(row)
            time.sleep(0.06)

        # 定格在最后一帧波动的样子（不重置为纯色）
        last_frame = 29
        print(f"\033[{H}A", end="")
        for row_i, line in enumerate(lines):
            row = ""
            for col_i, ch in enumerate(line.ljust(width)):
                if ch == "█":
                    wave = math.sin(last_frame * 0.3 + col_i * 0.4 + row_i * 0.5)
                    idx = int((wave + 1) / 2 * (len(palette) - 1))
                    color = f"\033[38;5;{palette[idx]}m"
                    row += f"{color}█{RESET}"
                else:
                    row += " "
            print(row)
    else:
        print(f"[ERROR] banner({para}) — valid options: 0, 1, 2, 3,...")


# ─────────────────────────────────────────────
# info(para) — program info block
#   0 : RRAgent 项目信息
#   1 : 最简版（只显示项目名和时间）
# ─────────────────────────────────────────────

def info(para=0, **kwargs):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os_info      = platform.platform()
    ORANGE, RESET, BOLD = "\033[38;5;208m", "\033[0m", "\033[1m"

    fields = [
        ("PROJECT", kwargs.get("project",     "Project XX")),
        ("VERSION", kwargs.get("version",     "1.0")),
        ("ENV",     kwargs.get("environment", "Development")),
        ("OS",      os_info),
        ("INFO",    kwargs.get("extra",       "Project Information")),
    ]

    description = kwargs.get("description", "Program Description")
    status      = kwargs.get("status",      "Initializing... ")

    icon = "█" if para == 0 else "◆"

    print()
    for label, value in fields:
        print(f"  {ORANGE}{BOLD}{icon}{RESET}  {label:<10}{value}")
    print()

    for char in description:
        print(f"{ORANGE}{char}{RESET}", end="", flush=True)
        time.sleep(0.03 if char != " " else 0.01)
    print("\n")

    for char in status:
        print(f"{ORANGE}{char}{RESET}", end="", flush=True)
        time.sleep(0.03 if char != " " else 0.01)
    print("\n")

# ─────────────────────────────────────────────
# other(para) — decorative elements
#   0 : 竖条从中间展开
#   1 : 文字从噪点中浮现（显示项目名）
# ─────────────────────────────────────────────

def effect(para=0, **kwargs):

    if para == 0:
        # ── 竖条从中间展开 ────────────────────────────
        width = kwargs.get("width", 36)
        for i in range(width // 2):
            left  = width // 2 - i
            right = width // 2 + i
            line  = " " * left + "\033[38;5;208m" + "█" * (right - left) + "\033[0m"
            print(f"\r{line}", end="", flush=True)
            time.sleep(0.03)
        print()

    elif para == 1:
        # ── 文字从噪点中浮现 ──────────────────────────
        title = kwargs.get("description", "RRAgent")
        chars = "▓▒░·:"
        for step in range(15):
            line = ""
            for c in title.center(30):
                if random.random() < step / 14:
                    line += f"\033[38;5;208m{c}\033[0m"
                else:
                    line += f"\033[38;5;238m{random.choice(chars)}\033[0m"
            print("\r" + line, end="", flush=True)
            time.sleep(0.05)
        print()
    elif para == 2:
        # ── 竖条从中间展开 ────────────────────────────
        width = kwargs.get("width", 36)
        for i in range(width // 2):
            left = width // 2 - i
            right = width // 2 + i
            line = " " * left + "\033[38;5;214m" + "◆" * (right - left) + "\033[0m"
            print(f"\r{line}", end="", flush=True)
            time.sleep(0.03)
        print()
    elif para == 3:
        width = kwargs.get("width", 40)
        ORANGE, RESET = "\033[38;5;208m", "\033[0m"
        for i in range(width + 1):
            line = "─" * i + ("►" if i < width else "─")
            print(f"\r{ORANGE}{line}{RESET}", end="", flush=True)
            time.sleep(0.02)
        print()
    elif para == 4:
        width = kwargs.get("width", 40)
        ORANGE, RESET = "\033[38;5;208m", "\033[0m"
        for i in range(width + 1):
            line = "░" * i + ("█" if i < width else "░")
            print(f"\r{ORANGE}{line}{RESET}", end="", flush=True)
            time.sleep(0.02)
        print()
    elif para == 5:
        width = kwargs.get("width", 40)
        ORANGE, RESET = "\033[38;5;208m", "\033[0m"
        for i in range(width // 2 + 1):
            left = "─" * i
            right = "─" * i
            mid = " " * (width - i * 2)
            print(f"\r{ORANGE}{left}{mid}{right}{RESET}", end="", flush=True)
            time.sleep(0.03)
        print()
    elif para == 6:
        import math
        width = kwargs.get("width", 40)
        ORANGE, RESET = "\033[38;5;208m", "\033[0m"
        chars = "·∙●∙·"
        for frame in range(20):
            line = ""
            for x in range(width):
                wave = math.sin(x * 0.4 + frame * 0.3)
                idx = int((wave + 1) / 2 * (len(chars) - 1))
                line += chars[idx]
            print(f"\r{ORANGE}{line}{RESET}", end="", flush=True)
            time.sleep(0.05)
        print()
    elif para == 7:
        width = kwargs.get("width", 40)
        ORANGE, RESET = "\033[38;5;208m", "\033[0m"
        # 先打点
        dots = ""
        for _ in range(width):
            dots += "·"
            print(f"\r{ORANGE}{dots}{RESET}", end="", flush=True)
            time.sleep(0.02)
        # 再变实线
        for i in range(width):
            line = "━" * i + "·" * (width - i)
            print(f"\r{ORANGE}{line}{RESET}", end="", flush=True)
            time.sleep(0.02)
        print()
    elif para == 8:
        title = kwargs.get("title", "RRAgent")
        chars = "▓▒░ "
        for step in range(15):
            line = ""
            for c in title.center(30):
                if random.random() < step / 14:
                    line += f"\033[38;5;208m{c}\033[0m"
                else:
                    line += f"\033[38;5;238m{random.choice(chars)}\033[0m"
            print("\r" + line, end="", flush=True)
            time.sleep(0.05)
        print()
    elif para == 9:
        ORANGE, RESET, BOLD = "\033[38;5;208m", "\033[0m", "\033[1m"
        description = kwargs.get("description", "Program Description")
        for char in description:
            print(f"{ORANGE}{char}{RESET}", end="", flush=True)
            time.sleep(0.03 if char != " " else 0.01)
        print("\n")
    else:
        print(f"[ERROR] other({para}) — valid options: 0, 1")

