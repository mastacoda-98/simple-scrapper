import requests, json, csv
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
response = requests.get(url, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")

with open("books.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Price", "Rating"])

    for a in soup.find_all("article"):
        if "product_pod" not in a.get("class", []):
            continue

        rating_text = a.find("p", class_="star-rating")["class"][1]

        ratings = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }

        rating = ratings.get(rating_text, 0)
        name = a.h3.a["title"]
        price = a.find("p", class_="price_color").text

        writer.writerow([name, price, rating])

print("Saved to books.csv")