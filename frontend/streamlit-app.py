# ./frontend/streamlit-app.py

import os
import sys

import streamlit as st

import asyncio
import nest_asyncio

from pathlib import Path

# Add the repo root to python pathes for imports
root_dir_path = Path().absolute()
sys.path.append(str(root_dir_path))

#from tg_bot.aiogram_bot import run_bot
from tg_bot.py_tg_bot import run_bot

# Allow nested loops (e.g. in jupyter, streamlit, databricks)
nest_asyncio.apply()


RUNTIME_FOUND = None
ATTACHED_TO_MAIN_LOOP = None

async def main():

    st.sidebar.write("Welcome!")

    st.title("Streamlit Telegram App")

    st.subheader("Debug messages")
    st.write(f"Runtime found: {RUNTIME_FOUND}")
    st.write(f"Attached to main loop: {ATTACHED_TO_MAIN_LOOP}")
    st.write(f"Root dir path set to {root_dir_path}")
    st.write(f"**Root dir content**")
    st.write('\\\n'.join(os.listdir(root_dir_path)))
    st.write(f"**Environment variables**")
    secret_env_vars = ['TELEGRAM_BOT_API_TOKEN']
    excluded_env_vars = []
    st.write('\\\n'.join((f"{k}: {v}" if k not in secret_env_vars else f"{k}: *****") 
                         for k, v in os.environ.items() if k not in excluded_env_vars))

async def run_all():
    tasks = [
        asyncio.create_task(main()),
        asyncio.create_task(run_bot())
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    from streamlit import runtime

    # Run in Snowflake
    # in Databricks, we are already inside async context (thus can't use asyncio.run) (this was before nested patching)
    if runtime.exists():
        RUNTIME_FOUND = True
        print(f"DEBUG: running from streamlit runtime")

        loop = asyncio.get_event_loop()

        if loop.is_running():
            ATTACHED_TO_MAIN_LOOP = True
            print(f"DEBUG: attached to main loop")
            #loop.create_task(run_all())
            loop.run_until_complete(run_all())

        else:
            ATTACHED_TO_MAIN_LOOP = False
            print(f"DEBUG: new main loop started")
            asyncio.run(run_all())  # or run main if not async but streamlit

    # Local run (interactive debug available)
    else:
        RUNTIME_FOUND = False
        print(f"DEBUG: redirect to streamlit cli call")

        import sys
        from streamlit.web import cli as stcli

        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())

