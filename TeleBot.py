from utils import *
from Reddit import *
import telegram.ext
MangaList = []
DailyManga = []
LastCommand = "None"
chatID = ""
greetings = "Welcome to the manga bot! \n Type /help to get the list of possible commands. \n " \
            "Type /create_list to make your first list. "


def start(update, context):
    update.send_message(chat_id=context.message.chat_id, text=greetings)
    global chatID
    chatID = context.message.chat_id

def manga(update, context):
    if(LastCommand == "new_chapter"):
        message = (get_message(context.message.text))
        if(message != ""):
            update.send_message(chat_id=context.message.chat_id, text=message)
        else:
            update.send_message(chat_id=context.message.chat_id, text="Sorry no manga with this name found")
            
    elif(LastCommand == "create_list" or LastCommand == "add_to_list"):
        size = len(MangaList)
        title = context.message.text
        MangaList.append(title)
        if(title != ""):
            update.send_message(chat_id=context.message.chat_id, text=title + " was successfullly added")

        else:
            update.send_message(chat_id=context.message.chat_id, text="Could not add entry")

    elif (LastCommand == "remove_from_list"):
        size = len(MangaList)
        for entry in MangaList:
            if context.message.text in entry:
                MangaList.remove(entry)
                update.send_message(chat_id=context.message.chat_id, text="Entry: " + entry + " was removed")
        if size == len(MangaList):
            update.send_message(chat_id=context.message.chat_id, text="This entry is not found in your manga list")

    else:
        update.send_message(chat_id=context.message.chat_id, text="Sorry I did not understand that command.")

def new_chapter(update, context, args):
    global LastCommand
    LastCommand = "new_chapter"
    if(len(args) == 0):
        update.send_message(chat_id=context.message.chat_id, text="Please send me the manga name")
    else:
       context.message.text = args[0]
       manga(update, context)


def create_list(update, context, args):
    global LastCommand
    LastCommand = "create_list"
    if(len(args) == 0):
        if (MangaList == []):
            update.send_message(chat_id=context.message.chat_id, text="Please send me the manga name to add to list")
        else:
            update.send_message(chat_id=context.message.chat_id, text="List already exists")
    else:
        context.message.text = args[0]
        manga(update, context)

def add_to_list(update, context, args):
    global LastCommand
    LastCommand = "add_to_list"
    if (len(args) == 0):
        update.send_message(chat_id=context.message.chat_id, text="Please send me the manga name to add to list")
    else:
        context.message.text = args[0]
        manga(update, context)

def print_list(update, context):
    global LastCommand
    LastCommand = "print_list"
    update.send_message(chat_id=context.message.chat_id, text="Here is the list of manga that I currently keep track of:")
    for entry in MangaList:
        update.send_message(chat_id=context.message.chat_id, text=entry)

def remove_from_list(update, context, args):
    global LastCommand
    LastCommand = "remove_from_list"
    if (len(args) == 0):
        update.send_message(chat_id=context.message.chat_id, text="Please send me the name of the manga to remove")
    else:
        context.message.text = args[0]
        manga(update, context)

def clean_list(update, context):
    global LastCommand,MangaList
    MangaList = []
    LastCommand = "clean_list"
    update.send_message(chat_id=context.message.chat_id, text="List was successfully cleaned")

def get_updates(update, context):
    global LastCommand
    LastCommand = "get_updates"
    update.send_message(chat_id=context.message.chat_id, text="These are the new chapters of your list:")
    for entry in MangaList:
        text = get_message(entry)
        update.send_message(chat_id=context.message.chat_id, text=text)

def clear_chapters(bot, job):
    global DailyManga
    DailyManga = []

def send_chapters(bot, job):
    global DailyManga
    for entry in MangaList:
        text = check_fresh(entry)
        if(text != "" and text not in DailyManga):
            bot.send_message(chat_id=chatID, text="New Chapter! \n" + text)
            DailyManga.append(text)

def help(update, context):
    global LastCommand
    LastCommand = "help"
    update.send_message(chat_id=context.message.chat_id, text="Here is the current list of commands: \n"
                                                              "/new_chapter sends you the last chapter of the manga that you"
                                                              " search \n"
                                                              "/create_list creates list of manga and notifies you whenever new"
                                                              " chapter will be posted on r/manga \n"
                                                              "/add_to_list adds new manga to your list \n"
                                                              "/remove_from_list removes selected manga from list \n"
                                                              "/clean_list removes all entries from the list \n"
                                                              "/get_updates sends you latest chapters of manga in your list")

