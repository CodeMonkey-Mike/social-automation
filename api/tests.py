import json
from datetime import datetime
from poll import pick_poll_less_than_7_days, get_poll_data


polls = get_poll_data()
dict = json.load(polls)
print('dict:', dict)
picked = pick_poll_less_than_7_days(dict)

print('picked:', picked)
