from tech_news.database import find_news


def value_getter(item):
    return item[1]


# Requisito 10
def top_5_categories():
    news = find_news()
    category_list = [post["category"] for post in news]

    category_dict = {}
    for category in category_list:
        if category in category_dict:
            category_dict[f"{category}"] += 1
        else:
            category_dict[f"{category}"] = 0
    # return category_dict.items()
    sorted_by_value = sorted(
        category_dict.items(), key=value_getter, reverse=True
    )[:5]
    return sorted(sorted_by_value)
