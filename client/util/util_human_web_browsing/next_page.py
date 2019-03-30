import math
from util.util_human_web_browsing.theme_similarity import calculate_theme_similarity


def get_all_clickable_links(driver):
    if driver is None:
        return []

    all_links = driver.find_elements_by_xpath('.//a')

    def validate_link(link):
        try:
            return link.text is not None and link.text != ""
        except:
            return False

    all_links = list(filter(lambda link: validate_link(link), all_links))

    return all_links


def calculate_link_theme_closeness_in_a_page(page_title, link):
    score = calculate_theme_similarity(page_title, link.text)

    return score


def calculate_link_visibility_closeness_in_a_page(page_height, link):
    # page_width = page.width

    location = link.location
    # x = location['x']
    y = location['y']

    # How far is the x deviated from the middle
    # x_closeness = 1.0 - 0.2 * abs(x - (page_width / 2.0)) / (page_width / 2.0)
    # How far is the y deviated from the top
    # the larger y_closeness, the farther the link

    y_closeness = y / page_height

    actual_closeness = 0.5 - 0.5 * math.sin(math.pi * (y_closeness - 0.5))

    return actual_closeness


def calculate_link_possibility(page, interest_in_theme, all_links, phi_visual_effect):
    all_link_possibility = []
    total_score = 0.0
    phi_theme_effect = 1 - phi_visual_effect

    for index, link in enumerate(all_links):
        try:
            visual_effect = phi_visual_effect * calculate_link_visibility_closeness_in_a_page(page.height, link)
            theme_closeness = calculate_link_theme_closeness_in_a_page(page.title, link)
            theme_interest = interest_in_theme
            theme_effect = phi_theme_effect \
                           * (2 * theme_closeness * theme_interest / (theme_closeness ** 2 + theme_interest ** 2))

            effect = (theme_effect + visual_effect)

            if effect > 0.0001:
                all_link_possibility.append({
                    'link': link,
                    'possibility': effect,
                    'theme_closeness': theme_closeness,
                })
                total_score += effect
        except:
            continue

    # print(len(all_link_possibility))

    return all_link_possibility, total_score


def normalize_link_possibility(all_links, total_score):
    total_score = total_score

    def normalize(link):
        link['possibility'] = link['possibility'] / total_score

        return link

    all_links = list(map(normalize, all_links))

    return all_links


def find_link_in_distribution(num, all_links):
    cumulative_score = 0
    prev_link = None

    # TODO change linear search to binary search
    for link in all_links:
        if cumulative_score > num:
            return prev_link
        else:
            cumulative_score += link['possibility']
            prev_link = link
    return prev_link
