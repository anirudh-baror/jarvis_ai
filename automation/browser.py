import webbrowser

def open_youtube():
    """Opens YouTube."""
    webbrowser.open("https://www.youtube.com")

def play_on_youtube(song_name):
    """Searches and plays a video on YouTube."""
    url = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}"
    webbrowser.open(url)

def search_google(query):
    """Searches Google for the given query."""
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)