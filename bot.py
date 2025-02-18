import os
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

async def chat_with_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка AI: {str(e)}"

async def start(update: Update, context):
    await update.message.reply_text(
        "Привет, искатель мудрости! \n\n"
        "🔮 Спроси меня о магии, напиши /quest для задания или /recipe для волшебного рецепта!"
    )

async def quest(update: Update, context):
    quest_prompt = "Придумай фэнтезийный квест с магией, приключениями и загадками."
    quest_text = await chat_with_ai(quest_prompt)
    await update.message.reply_text(quest_text)

async def recipe(update: Update, context):
    recipe_prompt = "Придумай волшебный рецепт с магическими ингредиентами и эффектами."
    recipe_text = await chat_with_ai(recipe_prompt)
    await update.message.reply_text(recipe_text)

async def handle_message(update: Update, context):
    user_message = update.message.text
    ai_response = await chat_with_ai(user_message)
    await update.message.reply_text(ai_response)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quest", quest))
    app.add_handler(CommandHandler("recipe", recipe))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Магический бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
