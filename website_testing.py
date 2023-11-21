from googlesearch import search
import webbrowser


def open_website_from_search(query):
    try:
        search_results = list(search(query, num_results=1))
        # print(search_results)
        if search_results:
            website_url = search_results[0]
            # print(website_url)
            # Extract the site name from the URL
            site_name = website_url.split('www.')[-1].split('.com')[0]
            # print(site_name)
            # say(f"Opening {site_name} ...")
            webbrowser.open(website_url)
        else:
            print('sorry, no results found')
    except Exception as e:
        print(f"An error occurred: {str(e)}")


open_website_from_search("swiggy")

import webbrowser

urls = ['https://youtube.com/', 'https://google.com/']

for url in urls:
    webbrowser.open(url)


for i in range(3, 5):
    print(f'hello person {i}')
