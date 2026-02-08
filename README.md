# Discord-Bot-Control-Panel-Dashboard-Application-Window
Hi! welcome to DBCP/D (Discord bot control panel / dashboard) application window download!
Tired of opening Visual Studios Code (or any other programming software you use) and relaunch your bot.py or main.py every single time? well you dont need to anymore with an application window that acts like a control panel for your bot!

# The panel currently includes:
- Latency status (ms)
- shutdown bot button
- bot startup button
- open console button (WARNING: MAY NOT SAVE THE CURRENT LINES WHEN YOU CLOSE CONSOLE AND THEN REOPEN!)

# Instructions
1 - Move the downloaded file into your bot folder project or to download fast, run in your powershell on vs code or any programming software: git clone https://github.com/WinterToasterteam/Discord-Bot-Control-Panel-Dashboard-Application-Window
(FOR THE 2nd OPTION ON DOWNLOADING IN POWERSHELL: MAKE SURE TO HAVE git DOWNLOADED OR IT MIGHT NOT BE RECOGNIZED! AFTER DOWNLOADING git PUT IT IN SYSTEM PATH!)

2 - download venv and have Python 3.8 or higher:

`python -m venv venv` (create an virtual environment to prevent globals to be interfered with its dependencies)

3 - create additional changes to window.py as putting your own .png, .wav sounds and extras!

# Installing latency correctly
1 - for the latency system, in your bot project, create: latency.json

2 - after creating latency.json, go to your bot.py or main.py, then make this above your @bot.event:

```python
@tasks.loop(seconds=1)
async def latency_task():
    bot_dir = os.path.dirname(os.path.abspath(__file__))
    latency_path = os.path.join(bot_dir, "latency.json")

    try:
        latency_ms = round(bot.latency * 1000)
        with open(latency_path, "w") as f:
            json.dump({"latency": latency_ms}, f)
    except Exception as e:
        print("Latency write error:", e)
```
# after creating latency_task, put this under @bot.event below the on_ready event:
```python
if not latency_task.is_running():
    latency_task.start()
```
congrats! you also installed the latency system! if you have any issues, please reach out to my discord: toasterteam
little notes on the script:
- while the bot is online and you reopen the dashboard (or whatever you like to call it), it will show as "OFFLINE", i will later fix that soon.
- 
**WARNING**: this panel assumes local access, do not expose it to the internet.
