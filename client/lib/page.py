from util.util_human_web_browsing.content_smilarity import calculate_content_similarity
from util.util_human_web_browsing.theme_similarity import calculate_theme_similarity
from util.util_human_web_browsing.theme_interest import calculate_interest_in_theme
from util.util_human_web_browsing.page_interest import calculate_page_interest
from util.util_human_web_browsing.page_staying_time import calculate_page_staying_time


class Page:
    max_content_length = 0

    def __init__(self, title, content, theme_staying_time, prev_page, height):
        self.title = title
        self.content = content
        self.height = height

        # the time spent on current theme
        self.theme_staying_time = theme_staying_time

        # calculate the interest in current theme
        self.interest_in_theme = calculate_interest_in_theme(self.theme_staying_time)

        # calculate the content closeness with previous page
        if prev_page is None:
            # at the beginning of browsing
            self.content_closeness = 0
        else:
            self.content_closeness = calculate_content_similarity(self.content, prev_page.content)

        # record the max length of web page
        if Page.max_content_length < len(self.content):
            Page.max_content_length = len(self.content)

        # calculate the page interest
        self.interest_in_page = calculate_page_interest(self)

        # calculate staying time for current page
        # among all content in a page, around 10% of them will be really useful information
        self.staying_time = int(calculate_page_staying_time(self.interest_in_page,
                                                            self.interest_in_theme,
                                                            self.max_content_length))

    def calculate_theme_closeness(self, link_title):
        result = calculate_theme_similarity(self.title, link_title)
        return result

    # TODO def calculate_staying_time(self, ):
