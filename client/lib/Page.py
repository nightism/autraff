from util.util_human_web_browsing.content_smilarity import calculate_content_similarity
from util.util_human_web_browsing.theme_similarity import calculate_theme_similarity
from util.util_human_web_browsing.calculate_page_interest import calculate_interest_in_theme


class Page:
    def __init__(self, title, content, theme_staying_time):
        self.title = title
        self.content = content
        self.theme_staying_time = theme_staying_time  # the time spent on current theme
        self.intertest_in_theme = calculate_interest_in_theme(theme_staying_time)

    def calculate_theme_closeness(self, another_title):
        result = calculate_theme_similarity(self.title, another_title)
        return result

    def calculate_content_closeness(self, another_content):
        # TODO
        result = calculate_content_similarity(self.content, another_content)
        return result

    # TODO def calculate_staying_time(self, ):
