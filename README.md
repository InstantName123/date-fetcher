# Data fetcher (proxies supported)
It supports **proxy rotation**, **Discord webhook alerts**, and a **safety mode** that ensures no requests are made without proxies. This makes it especially useful for environments where data fetching must be controlled, monitored, and/or logged in real-time.  

----------------

## 🚀 Features:
- **Safety mode** → prevents running without proxies.
- **Proxy support** → works with HTTP & HTTPS proxies.
- **Automatic saving** → each response is saved as a file.
- **Discord webhook notifications** → real-time alerts for:
  - Success (file saved)
  - Request errors
  - Timeouts
  - Proxy issues
- **Easily configurable waiting interval** → default is every 3 hours.
- **Continuous loop** → even on errors/fails it keeps running until stopped manually.
- **safety mode** → Ensures no unproxied requests are sent when **safety mode** is enabled.

----------------

## ⚙️ Installation steps:

1. Clone this repository:
   ```git clone https://github.com/yourusername/data-fetcher.git```
   ```cd data-fetcher```

2. Activate python enviremont:
   ```python -m venv venv```
   For Linux/MacOS: ```source venv/bin/activate```
   For Windows: ```venv\Scripts\activate```

3. Install pip "Requests" package
   ```pip install requests```

4. Open auto-fetcher.py in a text editor
   Change all configurations for your project (Don't forget to adjust the waiting time and the webhook)

5. Run the file in a screen (for linux) for windows you can just run the script and minimize the window
   ```screen python3 auto-fetcher.py```

## ⚠️ Disclaimer:
## This project is for educational and monitoring purposes only.
## Do not use it to send automated requests to third-party services without permission.

