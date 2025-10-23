#測試用程式，唔需要理佢
from app.utils import add_increment_to_rates, should_highlight_cell, format_rate_for_display,is_even_number
if __name__ == "__main__":
    print(is_even_number(1e-10,13))
    print(is_even_number(3.4e-10,11))