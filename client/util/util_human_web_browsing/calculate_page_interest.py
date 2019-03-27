# initial value of interest (0, 1)
initial_interest = 0.5

# time point when interest reaches the max
# when time = 600 seconds, interest will reach 0 at around 1449 s (23.23 min)
highest_interest_time = 600
highest_interest_time_square = highest_interest_time ** 2


def calculate_interest_in_theme(cumulative_staying_time):
    temp_time = cumulative_staying_time - highest_interest_time
    temp_time = temp_time ** 2 * 1.0

    temp_interest = initial_interest - 1.0

    current_interest = temp_interest / highest_interest_time_square * temp_time + 1
    current_interest = max(0, current_interest)

    print(current_interest)
    return current_interest
