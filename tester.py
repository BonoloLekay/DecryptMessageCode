import requests
from bs4 import BeautifulSoup
import tkinter as tk

def fetch_unicode_grid(doc_url):
    response = requests.get(doc_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    table_rows = soup.find_all('tr')

    points = []
    max_x = 0
    max_y = 0

    for row in table_rows:
        columns = row.find_all('td')
        if len(columns) != 3:
            continue
        try:
            x = int(columns[0].text.strip())
            char = columns[1].text.strip()
            y = int(columns[2].text.strip())
        except ValueError:
            continue
        points.append((char, x, y))
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for char, x, y in points:
        grid[y][x] = char

    return "\n".join("".join(row) for row in grid)

def display_gui(message):
    root = tk.Tk()
    root.title("Unicode Grid Viewer")

    text_widget = tk.Text(root, wrap="none", font=("Courier", 10))
    text_widget.insert(tk.END, message)
    text_widget.config(state=tk.DISABLED)
    text_widget.pack(expand=True, fill="both")

    root.mainloop()

url = 'https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub'
message = fetch_unicode_grid(url)
display_gui(message)
