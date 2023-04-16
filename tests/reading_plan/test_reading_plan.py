import pytest
from tech_news.analyzer.reading_plan import (
    ReadingPlanService,
)  # noqa: F401, E261, E501

find_news_return = []


def test_reading_plan_group_news(mocker):
    mocker.patch("tech_news.database.find_news", return_value=find_news_return)

    with pytest.raises(ValueError):
        ReadingPlanService.group_news_for_available_time(-1)

    assert (
        ReadingPlanService.group_news_for_available_time(15)["readable"][0][
            "unfilled_time"
        ]
        == 1
    )

    assert ReadingPlanService.group_news_for_available_time(15)["readable"][0][
        "chosen_news"
    ] == [
        (find_news_return[0]["title"], find_news_return[0]["reading_time"]),
        (find_news_return[1]["title"], find_news_return[1]["reading_time"]),
    ]

    assert (
        len(ReadingPlanService.group_news_for_available_time(15)["unreadable"])
        == 0
    )
