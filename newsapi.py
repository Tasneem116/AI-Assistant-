from config import gnews_apikey
import json

def get_news():
    import urllib.request
    category = ''
    categories = ['general', 'world', 'nation', 'business', 'technology', 'entertainment', 'sports', 'science', 'health']
    user = 'i want to hear regarding technology'
    for i in user.split():
        if i in categories:
            category+=i

    url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=in&max=10&apikey={gnews_apikey}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]
        for i in range(3):
            # articles[i].title
            print(f"Title: {articles[i]['title']}")
            # articles[i].description
            print(f"Description: {articles[i]['description']}")


get_news()
