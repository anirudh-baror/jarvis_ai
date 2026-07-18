import webbrowser
import urllib.parse

def open_youtube():
    """Opens the YouTube homepage."""
    webbrowser.open("https://www.youtube.com")

def play_on_youtube(song_name: str):
    """Searches for and plays a specific song or video on YouTube.

    Args:
        song_name: The name of the song or video to search and play.
    """
    encoded_query = urllib.parse.quote_plus(song_name)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"
    webbrowser.open(url)

def search_google(query: str):
    """Performs a Google search for the given query.

    Args:
        query: The text to search for on Google.
    """
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    webbrowser.open(url)