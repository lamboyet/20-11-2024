from telegram import Update, ChatMemberUpdated
from telegram.ext import Updater, CommandHandler, ContextTypes, Application, ChatMemberHandler, MessageHandler, filters

user_tasks={}

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user_id=update.effective_user.id
    await update.message.reply_text("Welcome to the To Do List Bot! Here's how to use me:\n"
                 "- /add <task> Adds a new task to the list.\n"
                 "- /delete <task_number> Deletes a task. \n"
                 "- /list Lists your tasks.\n"
                 "- /start Restarts the bot.\n"
                 "Enjoy.")
    if user_id not in user_tasks:
        user_tasks[user_id] = []

async def greet_on_chat_open(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        user_id = update.effective_user.id
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Welcome to the To Do List Bot! Here's how to use me:\n"
                 "- /add <task> Adds a new task to the list.\n"
                 "- /delete <task_number> Deletes a task. \n"
                 "- /list Lists your tasks.\n"
                 "- /start Restarts the bot.\n"
                 "Enjoy."
        )
        if user_id not in user_tasks:
            user_tasks[user_id] = []

# async def greet_private_chat(update:Update,context:ContextTypes.DEFAULT_TYPE):
#     chat_member: ChatMemberUpdated =update.chat_member
#     if chat_member.chat.type =="private" and chat_member.new_chat_member.status == "member":
#         user_id = update.effective_user.id
#         await context.bot.sendMessage(
#             chat_id=chat_member.chat.id,
#             text="Welcome to the To-Do List Bot! Use /add, /list and /delete to manage your tasks ",
#         )
#     if user_id not in user_tasks:
#         user_tasks[user_id] = []


async def add_task(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    task = ' '.join(context.args)
    if not task:
        await update.message.reply_text("Usage: /add <task>")
        return

    if user_id not in user_tasks:
        user_tasks[user_id] = []
    user_tasks[user_id].append(task)

    await update.message.reply_text(f"Task added: {task}")


async def list_tasks(update: Update, context:ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tasks = user_tasks.get(user_id,[])
    if not tasks:
        await update.message.reply_text("Your task list is empty")
    else:
        task_list = "\n".join(f"{i+1}.{tasks[i]}" for i, task in enumerate(tasks))
        await update.message.reply_text(f"Your tasks: \n{task_list}")


async def delete_task(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tasks = user_tasks.get(user_id,[])

    if not tasks:
        await update.message.reply_text("Your task list is empty")

    try:
        task_number = int(context.args[0]) -1
        if 0 <= task_number < len(tasks):
            removed_task = tasks.pop(task_number)
            await update.message.reply_text(f"Removed task:{removed_task}")
        else:
            await update.message.reply_text("Invalid task number!")
    except(IndexError, ValueError):
        await update.message.reply_text("Usage: /delete <task_number>")


def main():
    TOKEN = "7749901842:AAHYxAvu0uYvjzamOmUUcAXb5tYdQQVpcdk"
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start",start))
    #application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE,greet_on_chat_open))
    #application.add_handler(ChatMemberHandler(greet_private_chat, ChatMemberHandler.MY_CHAT_MEMBER))
    application.add_handler(CommandHandler("add", add_task))
    application.add_handler(CommandHandler("list", list_tasks))
    application.add_handler(CommandHandler("delete", delete_task))

    application.run_polling()


if __name__ == "__main__":
    main()