from tech_news.database import search_news
from datetime import datetime


def datetime_valid(dt_str):
    try:
        datetime.fromisoformat(dt_str)
    except Exception:
        raise ValueError("Data inválida")
    return True


# Requisito 7
def search_by_title(title):
    news = search_news({"title": {"$regex": f"{title}", "$options": "i"}})
    if news:
        return [(elm["title"], elm["url"]) for elm in news]
    return []


# Requisito 8
def search_by_date(date: str):
    if datetime_valid(date):
        formatedDate = f"{date[-2:]}/{date[5:7]}/{date[0:4]}"
        news = search_news({"timestamp": formatedDate})
    if news:
        return [(elm["title"], elm["url"]) for elm in news]
    return []


# Requisito 9
def search_by_category(category: str):
    news = search_news({"category": category.lower().capitalize()})
    if news:
        return [(elm["title"], elm["url"]) for elm in news]
    return []
