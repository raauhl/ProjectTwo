def calculate_cagr(initial_value, final_value, num_years):
    cagr = ((final_value / initial_value) ** (1 / num_years) - 1) * 100
    return cagr