def build_turn_prompt(player_name, mode, context):
    if mode == "snake":
        return f"🐍 Snake Mode!\nStart with '{context['last_letter']}'\n{player_name}, your turn!"
    elif mode == "ladder":
        return f"🪜 Ladder Mode!\nWord longer than {context['last_length']} letters\n{player_name}, your turn!"
    elif mode == "category":
        return f"🧠 Category Mode!\nCategory: {context['category']}\n{player_name}, your turn!"
    elif mode == "stopword":
        return f"⛔ Stop-the-Word Mode!\nAvoid letter '{context['banned_letter']}'\n{player_name}, your turn!"
    return f"🎮 Your turn, {player_name}!"
