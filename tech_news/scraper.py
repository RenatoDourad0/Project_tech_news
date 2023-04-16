from time import sleep
from parsel import Selector
from requests import get
from tech_news.database import create_news


#  Requisito 1
def fetch(url):
    try:
        sleep(1)
        response = get(
            url,
            timeout=3,
            headers={
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
            },
        )
        response.raise_for_status()
        return response.text
    except Exception:
        return None


# Requisito 2
def scrape_updates(html_content):
    list = []
    selector = Selector(text=html_content)
    post_links = selector.css("h2[class=entry-title] a::attr(href)").getall()
    list.extend(post_links)
    return list


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    next_page_link = selector.css(
        "div[class=nav-links] a:last-of-type::attr(href)"
    ).get()
    if not next_page_link:
        return None
    return next_page_link


# Requisito 4
def scrape_news(html_content):
    selector = Selector(text=html_content)
    post = {}
    post["url"] = selector.css("head link[rel=canonical]::attr(href)").get()
    title = selector.css(".entry-title::text").get()
    if title is None:
        title = selector.css(".Hero_hero__title__dCXAM-title::text").get()
    post["title"] = title.strip()
    post["timestamp"] = selector.css(".meta-date::text").get()
    post["writer"] = selector.css(".author > a::text").get()
    post["reading_time"] = int(
        selector.css(".meta-reading-time::text").get().split(" ")[0]
    )
    post["summary"] = (
        selector.css("div[class=entry-content] > p:first-of-type")
        .xpath("string()")
        .get()
        .strip()
    )
    post["category"] = selector.css(".category-style .label::text").get()
    return post


# Requisito 5
def get_tech_news(amount):
    full_links = []
    url = "https://blog.betrybe.com"
    while len(full_links) < amount:
        html = fetch(url)
        url = scrape_next_page_link(html)
        links = scrape_updates(html)
        full_links.extend(links)

    posts = []
    for link in full_links:
        if len(posts) < amount:
            post_html = fetch(link)
            post_data = scrape_news(post_html)
            posts.append(post_data)

    create_news(posts)
    return posts
