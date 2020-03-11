import re
from recipe_scrapers import scrape_me
# Gordon Ramsay's shit
# scrape = scrape_me('https://www.bbc.co.uk/food/recipes/chickenpaprikawithle_80341')

# instructions = scrape.instructions()
# y = scrape.yields()
# print(y)
# print(instructions)

# scrape = scrape_me('https://www.gordonramsay.com/gr/recipes/roast-beef-with-caramelised-onion-gravy/')
# scrape = scrape_me('https://www.gordonramsay.com/gr/recipes/roast-turkey-with-lemon-parsley-and-garlic/')
# scrape = scrape_me('https://www.gordonramsay.com/gr/recipes/pork-stuffed-with-manchego-and-membrillo/')
# y = scrape.yields()
# print(y)

# Delish shit
# scrape = scrape_me('https://www.delish.com/cooking/recipe-ideas/a27572327/chicken-cordon-bleu-recipe/')
# scrape = scrape_me('https://www.delish.com/cooking/recipe-ideas/a30209024/earl-grey-creme-brulee-recipe/')
scrape = scrape_me('https://www.delish.com/cooking/recipe-ideas/recipes/a56732/pumpkin-cheesecake-roll-recipe/')
# scrape = scrape_me('https://www.delish.com/cooking/recipe-ideas/a24276998/buche-de-noel-yule-log-cake-recipe/')
# scrape = scrape_me('https://www.delish.com/cooking/recipe-ideas/a30781614/banh-mi-recipe/')
# scrape = scrape_me('https://www.delish.com/cooking/recipe-ideas/a30142671/easy-cheese-straws-recipe/')

print(scrape.total_time())

# TIME_REGEX = re.compile(
#     r'(\D*(?P<hours>\d+)\s*(hours|hrs|hr|h|Hours|H))?(\D*(?P<minutes>\d+)\s*(minutes|mins|min|m|Minutes|M))?'

# match = TIME_REGEX.search('1 hours 10 minutes'
