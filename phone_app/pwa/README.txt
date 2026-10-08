FIRST AID / ПЪРВА ПОМОЩ - phone app (works offline)

WHAT IS IN THIS FOLDER
  index.html            the whole app (all cards, drawings, both languages)
  manifest.webmanifest  name and icon for the phone's home screen
  sw.js                 keeps the app on the phone so it works without internet
  icons/                app icons

PUT IT ONLINE (free, GitHub Pages)
  1. On github.com: New repository, e.g. "first-aid", set to Public.
  2. "Add file" > "Upload files". Upload EVERYTHING inside this folder
     (index.html must be at the top level, not inside another folder). Commit.
  3. Settings > Pages > Source: "Deploy from a branch", Branch: main, folder: / (root) > Save.
  4. After about a minute the app is at:  https://YOUR-USERNAME.github.io/first-aid/

INSTALL ON A PHONE (open the link once with internet)
  Android (Chrome):  menu (three dots) > "Install app" or "Add to Home screen".
  iPhone (Safari):   Share button > "Add to Home Screen".  (Must be Safari.)
  After that it opens from the home screen, also with no signal.

UPDATE THE CONTENT
  1. Edit cards.py / cards_bg.py / illustrations.py as before.
  2. Run:  python build_pwa.py      (in the folder with cards.py; needs Pillow: pip install pillow)
  3. Upload the new files from the pwa folder to the same repository, replacing the old ones.
  Phones get the update the next time the app is opened with internet
  (sometimes it needs to be closed and opened once more).
