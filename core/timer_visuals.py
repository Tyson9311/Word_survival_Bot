def generate_timer_bar(seconds_left, total=20):
    blocks = 7
    ratio = max(0, min(1, seconds_left / total))
    filled = int(ratio * blocks)
    bar = ""
    for i in range(blocks):
        if i < filled:
            bar += "🟩" if filled / blocks > 0.6 else "🟨"
        else:
            bar += "⬛"
    return bar
