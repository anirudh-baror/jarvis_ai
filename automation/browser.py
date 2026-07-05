import webbrowser
import urllib.parse

def open_youtube():
    """Opens the YouTube homepage."""
    webbrowser.open("https://www.youtube.com")

def play_on_youtube(song_name):
    """Searches and directly plays a specific query/song on YouTube."""
    encoded_query = urllib.parse.quote_plus(song_name)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"
    webbrowser.open(url)

def search_google(query):
    """Executes a Google search for the specified query string."""
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    webbrowser.open(url)