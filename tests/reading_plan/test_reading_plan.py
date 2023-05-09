import pytest
from tech_news.analyzer.reading_plan import (
    ReadingPlanService,
)  # noqa: F401, E261, E501

find_news_return = [
    {
        "title": "Cabos de rede: o que são, quais os tipos e como crimpar?",
        "reading_time": 9,
    },
    {
        "title": "Estruturas de repetição: quais as 4 principais e quando usá-las?",
        "reading_time": 5,
    },
    {
        "title": "Website development: o que é, o que faz e salário! O guia inicial!",
        "reading_time": 13,
    },
]


def test_reading_plan_group_news(mocker):
    with pytest.raises(ValueError):
        with mocker.patch(
            "tech_news.database.find_news", return_value=find_news_return
        ):
            ReadingPlanService.group_news_for_available_time(-1)

    with mocker.patch(
        "tech_news.database.find_news", return_value=find_news_return
    ):
        assert (
            ReadingPlanService.group_news_for_available_time(15)["readable"][
                0
            ]["unfilled_time"]
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
