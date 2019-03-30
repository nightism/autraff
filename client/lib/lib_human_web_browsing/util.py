from util.util_human_web_browsing.theme_interest import calculate_interest_in_theme


DEFAULT_NEW_THEME_INTEREST = 0.5
DEFAULT_INTEREST_PEAK_TIME = 600
DEFAULT_THEME_CLOSENESS_THRESHOLD = 0.6
DEFAULT_PHI_VISUAL_EFFECT = 0.2


class UtilWrapper:

    def __init__(self, total_staying_time, new_theme_interest=DEFAULT_NEW_THEME_INTEREST,
                 interest_peak_time=DEFAULT_INTEREST_PEAK_TIME,
                 theme_closeness_threshold=DEFAULT_THEME_CLOSENESS_THRESHOLD,
                 phi_visual_effect=DEFAULT_PHI_VISUAL_EFFECT):

        self.remaining_staying_time = int(total_staying_time)

        self.new_theme_interest = float(new_theme_interest)
        self.interest_peak_time = int(interest_peak_time)
        self.theme_closeness_threshold = float(theme_closeness_threshold)
        self.phi_visual_effect = float(phi_visual_effect)
        self.phi_page_interest_effect = 1 - phi_visual_effect

        self.cumulative_theme_stay_time = 0

    def proceed_to_next_page(self, theme_closeness, time_stayed):
        if theme_closeness < self.theme_closeness_threshold:
            self.cumulative_theme_stay_time = 0
        else:
            self.cumulative_theme_stay_time += time_stayed

        self.remaining_staying_time -= time_stayed
        self.remaining_staying_time = max(0, self.remaining_staying_time)

    def get_theme_interest_level(self):
        return calculate_interest_in_theme(self.cumulative_theme_stay_time,
                                           new_theme_interest=self.new_theme_interest,
                                           interest_peak_time=self.interest_peak_time)



