# ./frontend/streamlit-app.py

import streamlit as st

def main():

    st.sidebar.write("Welcome!")

    st.title("Streamlit Telegram App")


if __name__ == '__main__':
    from streamlit import runtime

    # Run in Snowflake
    if runtime.exists():
        main()
    # Local run (interactive debug available)
    else:
        import sys
        from streamlit.web import cli as stcli

        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
