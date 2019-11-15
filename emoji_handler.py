emoji_databse = {"👍":"👍"}

def emoji_handler(bot, text, sender_id):
    if text in emoji_databse:
        response = emoji_databse[text]
        bot.send_text_message(sender_id, response)
        return True
        
    return False