# main.py - ربات ترید IBKR 24/7 - @Hoseinyazdi3
from ib_insync import *
import time
from datetime import datetime
import telebot
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
QUANTITY = 0.01

ib = IB()
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def send(msg):
    bot.send_message(CHAT_ID, "🤖 ربات بیت‌کوین:\n" + msg)

ib.connect('127.0.0.1', 7497, clientId=1)
send("ربات 24/7 روی سرور روشن شد! 🔥")

contract = Crypto('BTC', 'PAXOS', 'USD')
ib.qualifyContracts(contract)

BUY_LOW, BUY_HIGH = 94000, 95000
TARGET, STOP = 114500, 92000
position = 0.0

while True:
    try:
        ticker = ib.reqMktData(contract, '', False, False)
        time.sleep(1)
        price = ticker.last or ticker.close
        if not price: continue

        if position == 0 and BUY_LOW <= price <= BUY_HIGH:
            order = MarketOrder('BUY', QUANTITY)
            ib.placeOrder(contract, order)
            send(f"خرید در ${price:,.0f}")
            position = QUANTITY

        elif position > 0 and (price >= TARGET or price <= STOP):
            order = MarketOrder('SELL', position)
            ib.placeOrder(contract, order)
            profit = (price - 94500) * position
            send(f"فروش در ${price:,.0f}\nپروفیت: ${profit:,.2f}")
            position = 0

        print(f"[{datetime.now().strftime('%H:%M:%S')}] BTC: ${price:,.0f}")
        time.sleep(5)

    except Exception as e:
        send(f"خطا: {e}")
        time.sleep(10)
