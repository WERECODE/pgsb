import tkinter as tk
import tkinter.messagebox as messagebox
import asyncio
import discord, threading
from discord.ext import commands
import customtkinter

bot = commands.Bot(command_prefix='.', self_bot=True)
bot_is_running = False  # Flag to keep track if the bot is running

# GUI setup
root = customtkinter.CTk()
root.geometry("900x500")
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# Dark mode theme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


def start_purge():
    global bot_is_running
    if not bot_is_running:
        messagebox.showinfo("Bot Not Running", "The bot is not running. Please start the bot first.")
        return

    channel_id = int(channel_entry.get())

    async def purge_messages():
        try:
            await bot.wait_until_ready()  # Wait for the bot to be ready
            user_id = bot.user.id  # Access the bot.user.id after the bot is ready
            channel = bot.get_channel(channel_id)
            if not channel:
                log_listbox.insert(tk.END, "Invalid channel ID.")
                return

            def is_target_user(message):
                return message.author.id == user_id

            deleted = await channel.purge(limit=None, check=is_target_user)

            if deleted:
                messagebox.showinfo("Finished", "Purge Complete!")
                log_listbox.insert(tk.END, "Messages deleted:")
                for message in deleted:
                    log_listbox.insert(tk.END, f"{message.content} - {message.created_at}")

        except ValueError:
            log_listbox.insert(tk.END, "Invalid channel ID. Please enter a valid integer.")
        except discord.Forbidden:
            log_listbox.insert(tk.END, "I don't have the necessary permissions to delete messages.")
        except discord.HTTPException as e:
            log_listbox.insert(tk.END, f"An error occurred: {e}")

    bot.loop.create_task(purge_messages())

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

@bot.event
async def on_ready():
    global bot_is_running
    bot_is_running = True
    print("Bot is ready.")

def bbc():
    threading.Thread(target=runbot).start()

@bot.event
async def on_message(message):
    await bot.process_commands(message)


# Set grid row and column weights to center everything
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

listbox_bg_color = "#2E3440"  # Replace this color code with the desired dark mode background
log_listbox = tk.Listbox(master=frame, bg=listbox_bg_color, fg="white", width=80, height=20)
log_listbox.grid(row=1, column=0, columnspan=2, pady=10)

# Place the channel ID label and entry on top
channel_label = customtkinter.CTkLabel(master=frame, text="Channel ID:")
channel_label.grid(row=0, column=0, pady=5)

channel_entry = customtkinter.CTkEntry(master=frame, placeholder_text="id")
channel_entry.grid(row=0, column=1, pady=5)

# Place the button container at the bottom
button_container = tk.Frame(frame, bg="#2E3440")  # Set the background color for the button container
button_container.grid(row=2, column=0, columnspan=2)

purge_button = customtkinter.CTkButton(master=button_container, text="Purge", command=start_purge)
purge_button.pack(side=tk.LEFT, padx=5)

btn = customtkinter.CTkButton(master=button_container, text="Start", command=bbc)
btn.pack(side=tk.LEFT, padx=5)


root.protocol("WM_DELETE_WINDOW", on_closing)

def runbot():
    try:
        with open("token.txt", "r") as token_file:
            token = token_file.read().strip()
        bot.run(token)
    except FileNotFoundError:
        messagebox.showerror("Error", "token.txt not found.") 
root.mainloop()