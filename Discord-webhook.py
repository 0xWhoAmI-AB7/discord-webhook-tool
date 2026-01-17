import customtkinter as ctk
import requests
import json
import threading
from tkinter import messagebox

# ---------------- SETTINGS ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ---------------- SEND FUNCTION ----------------
def send_message():
    webhook = webhook_entry.get().strip()
    username = botname_entry.get().strip()
    message = message_text.get("1.0", "end").strip()

    if not webhook or not message:
        messagebox.showerror("Error", "Webhook URL and message are required!")
        return

    send_button.configure(state="disabled", text="Sending... ⏳")

    def task():
        try:
            data = {
                "content": message,
                "username": username if username else "Webhook Bot"
            }

            response = requests.post(
                webhook,
                data=json.dumps(data),
                headers={"Content-Type": "application/json"}
            )

            if response.status_code in (200, 204):
                messagebox.showinfo("Success", "Message sent successfully!")
                message_text.delete("1.0", "end")
            else:
                messagebox.showerror("Failed", f"Error {response.status_code}\n{response.text}")

        except Exception as e:
            messagebox.showerror("Exception", str(e))

        send_button.configure(state="normal", text="Send Message 🚀")

    threading.Thread(target=task, daemon=True).start()

# ---------------- UI ----------------
app = ctk.CTk()
app.title("Discord Webhook Tool by WHO AM I")
app.geometry("520x500")
app.resizable(False, False)

# Title
title = ctk.CTkLabel(
    app,
    text="Discord Webhook Sender by WHO AM I",
    font=ctk.CTkFont(size=22, weight="bold")
)
title.pack(pady=15)

# Frame
frame = ctk.CTkFrame(app, corner_radius=15)
frame.pack(padx=20, pady=10, fill="both", expand=True)

# Webhook
ctk.CTkLabel(frame, text="Webhook URL").pack(anchor="w", padx=20, pady=(15, 0))
webhook_entry = ctk.CTkEntry(frame, placeholder_text="https://discord.com/api/webhooks/...")
webhook_entry.pack(padx=20, fill="x")

# Bot name
ctk.CTkLabel(frame, text="Bot Name").pack(anchor="w", padx=20, pady=(15, 0))
botname_entry = ctk.CTkEntry(frame, placeholder_text="WHO AM I")
botname_entry.pack(padx=20, fill="x")
botname_entry.insert(0, "WHO AM I")

# Message
ctk.CTkLabel(frame, text="Message").pack(anchor="w", padx=20, pady=(15, 0))
message_text = ctk.CTkTextbox(frame, height=120)
message_text.pack(padx=20, fill="x")

# Send button
send_button = ctk.CTkButton(
    frame,
    text="Send Message 🚀",
    corner_radius=12,
    height=45,
    command=send_message
)
send_button.pack(pady=25)

# Footer
footer = ctk.CTkLabel(
    app,
    text="Free • Open-Source",
    text_color="white"
)
footer.pack(pady=5)


app.mainloop()
