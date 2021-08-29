import os
import tweepy
import datetime
import time
import sys
import matplotlib.pyplot as plt

dati = datetime
ti = time

consumer_key = "***"
consumer_secret = "***"
access_key = "***"
access_secret = "***"


def fnum(num):
    if 0 < num < 10:
        result = "000" + str(num)
    elif 10 <= num < 100:
        result = "00" + str(num)
    elif 100 <= num < 1000:
        result = "0" + str(num)
    else:
        result = str(num)
    return result


def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    all_tweets = []
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    all_tweets.extend(new_tweets)
    oldest = all_tweets[-1].id - 1
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1
        # print(f"Number of tweets streamed from @{screen_name}: {len(all_tweets)}")
        print("*", end='')
    print("")
    return all_tweets


def convert_to_timestamp(username, tweets, timespan):
    file = f"data/{username}.txt"
    if os.path.exists(file):
        os.remove(file)
    f = open(file, "a")

    if timespan == "1":
        month = int(ti.time()) - 2678400
    else:
        month = 0

    counter = 1
    for tweet in tweets:
        dt = str(tweet.created_at).split(' ')
        date = dt[0].split('-')
        time = dt[1].split(':')
        datetime = dati.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))
        timestamp = str((ti.mktime(datetime.timetuple()))).replace(".0", "")
        if int(timestamp) < month:
            break
        f.write(f"{fnum(counter)}:{timestamp}\n")
        counter += 1
    f.close()


def draw_scatter_graph(username, color):
    data = {}

    x1 = []
    y1 = []

    f = open(f"data/{username}.txt", "r")
    for line in f:
        timestamp = int(line.split(':')[1]) + 16200
        dh = (ti.strftime("%d %H:%M", ti.localtime(timestamp))).split(' ')
        d = int(dh[0])
        hm = dh[1].split(":")
        h = int(hm[0])
        m = int((int(hm[1]) * 100) / 60)
        item = f'{d}-{h}.{m}'
        if item in data:
            data[item] += 1
        else:
            data.update({item: 1})

    for k in data.keys():
        dh = k.split("-")
        d = float(dh[0])
        h = float(dh[1])
        mx = float(d + (h / 24))
        my = h

        x1.append(mx)
        y1.append(my)

    plt.scatter(x1, y1, color=f'#{color}', s=3, marker="*")

    space = '               '
    plt.title(f'\n@{username}\'s Tweets Scatter Graph\n', fontname="Times New Roman", size=18)
    plt.xlabel("Days of the month \n \nDeveloped by @ZarchiMohammad")
    plt.ylabel("Hours of the day (GMT +04:30 Iran)")
    plt.grid(color='gray', linestyle='--', linewidth=0.3)
    plt.xlim([0, 32])
    plt.ylim([0, 25])
    x = [' ', ' ', ' ', ' ', ' ', '5', ' ', ' ', ' ', ' ', '10', ' ', ' ', ' ', ' ', '15', ' ', ' ', ' ', ' ', '20',
         ' ',
         ' ', ' ', ' ', '25', ' ', ' ', ' ', ' ', '30', ' ']

    y = ['0', ' ', ' ', ' ', ' ', ' ', '6', ' ', ' ', ' ', ' ', ' ', '12', ' ', ' ', ' ', ' ', ' ', '18', ' ', ' ',
         ' ', ' ', ' ', '24']
    plt.xticks(range(len(x)), x)
    plt.yticks(range(len(y)), y)
    plt.tick_params(axis='y', which='both', labelleft=True, labelright=True)
    plt.savefig(f'image/SG/{username}.png', bbox_inches='tight')
    sys.stdout.flush()


if __name__ == '__main__':
    username = input("Insert Twitter @username: ")
    timespan = input("Timespan 1.Month 2.All : ")
    print("Please wait ", end='')
    tweets = get_all_tweets(username)
    convert_to_timestamp(username, tweets, timespan)
    i = int(input("Insert your color code: "))
    colors = {1: "CC5200", 2: "CC7B00", 3: "CCA400", 4: "CBCC00",
              5: "86B800", 6: "00A405", 7: "007AA4", 8: "0043A4",
              9: "1C00A4", 10: "6E00A4", 11: "AE0065", 12: "CD0000"}
    draw_scatter_graph(username, colors[i])
