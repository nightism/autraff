

def calculate_interest_in_theme(cumulative_staying_time, new_theme_interest=0.5,
                                interest_peak_time=600  # when time = 600 seconds,
                                # interest will reach 0 at around 1449 s (23.23 min)
                                ):

    highest_interest_time_square = interest_peak_time ** 2
    temp_time = cumulative_staying_time - interest_peak_time
    temp_time = temp_time ** 2 * 1.0

    temp_interest = new_theme_interest - 1.0

    current_interest = temp_interest / highest_interest_time_square * temp_time + 1
    current_interest = max(0, current_interest)

    # print(current_interest)
    return current_interest
