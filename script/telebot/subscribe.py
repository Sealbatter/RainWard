from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

def get_coordinates(location):
    

def subscribe(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    location = ' '.join(context.args)  # Get location from command arguments
    # Convert location to lat, lon (implement this function)
    lat, lon = get_coordinates(location)
    subscriptions[user_id] = {'location': (lat, lon), 'subscribed': True}
    update.message.reply_text(f"Subscribed to rain alerts for {location}.")


