import random

from util.util_human_web_browsing.theme_interest import calculate_interest_in_theme
from util.util_human_web_browsing.content_smilarity import calculate_content_similarity
from util.util_human_web_browsing.theme_similarity import calculate_theme_similarity
from util.util_human_web_browsing.page_interest import calculate_page_interest
from util.util_human_web_browsing.page_staying_time import calculate_page_staying_time

from util.util_human_web_browsing.next_page import get_all_clickable_links
from util.util_human_web_browsing.next_page import calculate_link_possibility
from util.util_human_web_browsing.next_page import normalize_link_possibility
from util.util_human_web_browsing.next_page import find_link_in_distribution


class UtilWrapper:
    DEFAULT_NEW_THEME_INTEREST = 0.5
    DEFAULT_INTEREST_PEAK_TIME = 600
    DEFAULT_THEME_CLOSENESS_THRESHOLD = 0.6
    DEFAULT_PHI_VISUAL_EFFECT = 0.2

    def __init__(self, total_staying_time,
                 new_theme_interest=DEFAULT_NEW_THEME_INTEREST,
                 interest_peak_time=DEFAULT_INTEREST_PEAK_TIME,
                 theme_closeness_threshold=DEFAULT_THEME_CLOSENESS_THRESHOLD,
                 phi_visual_effect=DEFAULT_PHI_VISUAL_EFFECT):

        self.remaining_staying_time = int(total_staying_time)

        self.new_theme_interest = float(new_theme_interest)
        self.interest_peak_time = int(interest_peak_time)
        self.theme_closeness_threshold = float(theme_closeness_threshold)
        self.phi_visual_effect = float(phi_visual_effect)
        self.phi_theme_effect = 1 - phi_visual_effect

        self.cumulative_theme_stay_time = 0
        self.prev_page = None

    def before_proceed_to_next_page(self, time_stayed):
        self.cumulative_theme_stay_time += time_stayed
        self.remaining_staying_time -= time_stayed
        self.remaining_staying_time = max(0, self.remaining_staying_time)

    def proceed_to_next_page(self, theme_closeness, prev_page):
        if theme_closeness < self.theme_closeness_threshold:
            self.cumulative_theme_stay_time = 0

        self.prev_page = prev_page

    def get_theme_interest_level(self):
        return calculate_interest_in_theme(self.cumulative_theme_stay_time,
                                           new_theme_interest=self.new_theme_interest,
                                           interest_peak_time=self.interest_peak_time)

    def calculate_content_similarity(self, cont):
        if self.prev_page is not None:
            return calculate_content_similarity(cont, self.prev_page.content)
        else:
            return 0

    def calculate_interest_in_page(self, page):
        return calculate_page_interest(page, self.cumulative_theme_stay_time)

    def calculate_staying_time(self, page_interest, max_content_length):
        return calculate_page_staying_time(page_interest, self.get_theme_interest_level(), max_content_length)

    @staticmethod
    def calculate_theme_closeness(page_title, link_title):
        result = calculate_theme_similarity(page_title, link_title)
        return result

    @staticmethod
    def get_all_clickable_links_from_driver(driver):
        return get_all_clickable_links(driver)

    def calculate_and_normalize_possibility_for_all_link(self, page, all_links):
        all_links, total_score = calculate_link_possibility(page, self.get_theme_interest_level(),
                                                            all_links, self.phi_visual_effect)
        all_links = normalize_link_possibility(all_links, total_score)
        return all_links

    @staticmethod
    def get_a_random_link(all_links):
        num = random.random()
        link_to_be_clicked = find_link_in_distribution(num, all_links)
        return link_to_be_clicked
