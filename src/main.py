from ntscraper import Nitter
import time

from spinner import spinner


def scrape_twitter_accounts(usernames: list[str], tag: str) -> int:
    """Scrape twitter account Tweets and filter it by Tag and return the number of Tweets

    Args:
        usernames (list[str]): accounts username list
        stock_symbol (str): Search Tag

    Returns:
        int: number of Tweets with Tag
    """
    # handle :Fetching error: Instance has been rate limited.Use another instance or try again later.
    try:
        # create new Nitter object
        scraper = Nitter(log_level=1)

        # all users tweets
        users_tweets_list = scraper.get_tweets(usernames, mode="user")
        
    except Exception as e:
        if "Instance has been rate limited" in str(e):
            print("Error: Instance has been rate limited. Waiting for 60 seconds and trying again.")
            time.sleep(60)
            scrape_twitter_accounts(usernames, tag)
        else:
            raise e

    # users_tweets_list = [
    # {
    # 'threads': [],
    #  'tweets': [{'text': 'test text',...}]
    # },
    # {
    # 'threads': [],
    #  'tweets': [{'text': 'test text',...}]
    # }
    # ,... ]

    # filtered_tweets = []   # TEST
    filtered_tweets_count = 0
    for user_tweets in users_tweets_list:
        for tweet in user_tweets["tweets"]:
            if tag in tweet["text"]:
                # filtered_tweets.append(tweet)  # TEST
                filtered_tweets_count += 1

    # scraper.session_reset()   # TEST
    # print(f"filterd tweets: {filtered_tweets}")  # TEST
    # print(f"\nNumber of tweets taged by {tag}: {filtered_tweets_count}")
    return filtered_tweets_count

def get_time_interval(minute: str) -> int:
    """handel time interval as a integer"""
    try:
        interval = int(minute)
        return interval
    except ValueError:
        print("Time interval must be an integer\n")
        minute_ = input("\nEnter the time interval by minutes: " )
        get_time_interval(minute_)

def main():
    users_links = [
        "https://twitter.com/Mr_Derivatives",
        "https://twitter.com/warrior_0719",
        "https://twitter.com/ChartingProdigy",
        "https://twitter.com/allstarcharts",
        "https://twitter.com/yuriymatso",
        "https://twitter.com/TriggerTrades",
        "https://twitter.com/AdamMancini4",
        "https://twitter.com/CordovaTrades",
        "https://twitter.com/Barchart",
        "https://twitter.com/RoyLMattox",
    ]

    # users_links = [ "Mr_Derivatives", ....]
    users_list = [user.split("/")[-1].strip() for user in users_links]

    # TEST:
    # mentions_count = scrape_twitter_account(users_list, "#TSLA")
    # total_mentions += mentions_count

    total_mentions = 0
    while True:
        # Tag input
        tag = input("\nEnter Search Tag (Tag length must be greater than or equal 3): $")
        if len(tag.strip()) < 3:
            print("Tag length must be greater than or equal 3\n")
            continue
        else:
            tag = f"${tag.strip().upper()}"

        delta_time = None
        start_time = time.time()
        
        # slice --> 4 users for maximum
        # loop through a subset of Twitter accounts (4 users at a time)
        for slice in range(4, len(users_list) + 3, 4):
            scraping_users_list = users_list[slice - 4 : slice]
            
            print(f"Start Scraping ({', '.join(scraping_users_list)}) users...\n")

            mentions_count = scrape_twitter_accounts(scraping_users_list, tag)
            total_mentions += mentions_count

            print(
                f"Success Scraping ({', '.join(scraping_users_list)}) users with '{tag}' Tag\n"
            )
            print("--------------------------------------------------------")

            if len(users_list) + 3 - 1 != slice:
                print("Rest...\n")
                # time.sleep(1 * 60)
                spinner(1 * 60)

        end_time = time.time()
        delta_time = end_time - start_time

        print(
            f'\n"{tag}" was mentioned "{total_mentions}" times in the last "{round(delta_time / 60, 1)}" minutes.\n'
        )

        # new session
        q = input(
            f"Enter 'q' to quit or any key to start new session: "
        )
        if q == "q":
            print("Bye! :)")
            break
        
        # time interval 
        time_input = input("\nEnter 'q' to quit or enter the time interval by minutes: " )
        if time_input == "q":
            print("Bye! :)")
            break
        time_interval = get_time_interval(time_input)
        
        print("\nWaiting...\n")
        # reset counter
        total_mentions = 0
        
        # time.sleep(time_interval * 60)
        spinner(time_interval * 60)


if __name__ == "__main__":
    main()
