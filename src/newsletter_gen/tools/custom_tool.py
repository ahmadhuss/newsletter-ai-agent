import os
from datetime import datetime, timedelta

from crewai_tools import BaseTool
from exa_py import Exa


class SearchAndContents(BaseTool):
    name: str = "Search and Contents Tool"
    # agent will read the tool description
    description: str = (
        "Searches the web based on a search query for the latest results. Results are only from the last week. Uses the Exa API. This also returns the contents of the search results."
    )

    def _run(self, search_query: str) -> str:
        exa = Exa(api_key=os.getenv('EXA_API_KEY'))

        # 1 Week ago date 7 days
        one_week_ago = datetime.now() - timedelta(days=7)
        date_cutoff = one_week_ago.strftime('%Y-%m-%d')

        # Return Search and their content, search_query our agent will formulate
        # Exa works on transformers if agent didn't formulate the query, then use_autoprompt
        # helps Exa to reformulate the query
        search_results = exa.search_and_contents(query=search_query,
                                                 use_autoprompt=True,
                                                 start_published_date=date_cutoff,
                                                 text={
                                                     'include_html_tags': False,
                                                     'max_characters': 8000
                                                 }
                                                 )
        return search_results


class FindSimilar(BaseTool):
    name: str = "Find Similar Tool"
    # agent will read the tool description
    description: str = (
        "Searches for similar articles to a given article using the Exa API. Takes in a URL of the article"
    )

    def _run(self, article_url: str) -> str:
        exa = Exa(api_key=os.getenv('EXA_API_KEY'))

        # 1 Week ago date 7 days
        one_week_ago = datetime.now() - timedelta(days=7)
        date_cutoff = one_week_ago.strftime('%Y-%m-%d')

        search_results = exa.find_similar(url=article_url, start_published_date=date_cutoff)
        return search_results


class GetContents(BaseTool):
    name: str = "Get Contents Tool"
    # agent will read the tool description Exa API to get article detail we have to pass ID in list
    # in Exa case the ID will be article URL
    description: str = (
        "Gets the contents of a specific article using the Exa API. Takes in the ID of the article in a list, like this: ['https://www.cnbc.com/2024/04/18/my-news-story']."
    )

    def _run(self, article_ids: list[str]) -> str:
        exa = Exa(api_key=os.getenv('EXA_API_KEY'))
        contents = exa.get_contents(ids=article_ids)
        return contents

# Actually Test the tool I will execute directly from here.
# if __name__ == '__main__':
# search_and_contents = SearchAndContents()
# search_results = search_and_contents.run(search_query="latest news on the Singapore Stock market")
# print(search_results)

# Find Similar
# ID: https://www.rediff.com/business/report/sensex-nifty-settle-marginally-lower-in-volatile-trade/20240812.htm
# find_similar = FindSimilar()
# similar_results = find_similar.run(article_url='https://www.rediff.com/business/report/sensex-nifty-settle-marginally-lower-in-volatile-trade/20240812.htm')
# print(similar_results)

# Get Contents Based on ID
# So Exa has already scraped the data for us and indexed it.
# get_contents = GetContents()
# contents = get_contents.run(
#     article_ids=["https://www.rediff.com/business/report/sensex-nifty-settle-marginally-lower-in-volatile-trade/20240812.htm"])
# print(contents)
