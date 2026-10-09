# First Aid App

A simple first aid guide built with Streamlit. Each emergency has its own card with a clear, step-by-step protocol, so you can find what to do quickly, even under stress.

**Live app:** https://firstaidkit.streamlit.app 

> ⚠️ **In an emergency, call 112 first.**
> This app is a guide, not a replacement for professional medical help or first aid training.

---

## Features

- **Start here**: a triage button that helps you choose the right card when you're unsure what's happening
- **Situation cards**: the most frequent emergencies, each with numbered steps to follow
- **Infant and child cards**: CPR and choking protocols adapted for babies and children
- **Simple illustrations**: hand positions, recovery position and other key moments
- **Two languages**: Bulgarian and English (BG / EN switch)

## How to use

1. Open the app.
2. Choose your language (BG / EN).
3. If you know what happened, open the matching card. If not, press **Start here**.
4. Follow the steps in order.

## Run it locally

You need Python 3.9 or newer.

```bash
git clone https://github.com/Schaubia/FirstAid.git
cd FirstAid
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app opens in your browser at `http://localhost:8501`.

## Project structure

```
streamlit_app.py    # main app file (keep this name — the deployment uses it)
requirements.txt    # Python packages the app needs
README.md           # this file
```

## Updating the app

The online app is deployed on Streamlit Community Cloud from this repository.
Any change committed to the main branch is redeployed automatically within about a minute.

## Roadmap

- Downloadable / installable phone version
- More emergency cards

## Disclaimer

The content follows commonly accepted first aid guidelines and is being medically reviewed before the installable version is released. Protocols can change over time. When in doubt, follow the instructions of the emergency operator (112).
