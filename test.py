from get_data import get_data
from Queries import ALL_STATION

g = get_data("http://localhost:3030/bicycle",ALL_STATION)

print(g)