# tts.py

import threading
import queue
import subprocess

tts_queue = queue.Queue()

# Customize these:
VOICE = "Samantha"   # or Alex, Daniel, Victoria, etc.
RATE = "170"         # try 150–250 for slower/faster speech

def tts_worker():
    while True:
        text = tts_queue.get()
        if text is None:
            break
        try:
            subprocess.run(["say", "-v", VOICE, "-r", RATE, text])
        except Exception as e:
            print("TTS Error:", e)
        finally:
            tts_queue.task_done()

tts_thread = threading.Thread(target=tts_worker, daemon=True)
tts_thread.start()

def tts_question(text):
    tts_queue.put(text)
