import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from groq import AsyncGroq

TOKEN = os.environ["TOKEN"]
GROQ_KEY = os.environ["GROQ_KEY"]

client = AsyncGroq(api_key=GROQ_KEY)

async def javob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    savol = update.message.text

    try:
        natija = await client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "Foydalanuvchi savoliga o'zbek tilida, sodda va qisqa javob ber."
                },
                {"role": "user", "content": savol},
            ],
        )
        matn = natija.choices[0].message.content
    except Exception as e:
        matn = "Xatolik: " + str(e)

    await update.message.reply_text(matn)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, javob))
app.run_polling()
