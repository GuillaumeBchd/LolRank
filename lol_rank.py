import requests
import argparse
import enum

class Regions(enum.Enum):
    BR1 = "br1"
    EUN1 = "eun1"
    EUW1 = "euw1"
    JP1 = "jp1"
    KR = "kr"
    LA1 = "la1"
    LA2 = "la2"
    NA1 = "na1"
    OC1 = "oc1"
    RU = "ru"
    TR1 = "tr1"

    @classmethod
    def to_list(cls):
        return [r.value for r in Regions]

    @classmethod
    def to_string(cls):
        return ', '.join([r.value for r in Regions])


if __name__ == "__main__":

    # Initialize parser
    parser = argparse.ArgumentParser(description="A little program to automatically get the user lol rank in solo 5v5", prog="lol_rank")

    parser.add_argument("username", type=str, help="the league username.")
    parser.add_argument("token", type=str, help="the league api token.")
    parser.add_argument("-r", "--region", type=str, help="the region of the user. values are {}. default euw1".format(Regions.to_string()))

    # Parse arguments
    args = parser.parse_args()

    username = args.username
    token = args.token
    region = "euw1"
    if args.region is not None:
        if args.region not in Regions.to_list():
            parser.error("Wrong region, please choose one from this list : {}".format(Regions.to_string()))
        region = args.region


    # Header with given token
    header = {"X-Riot-Token" : token}

    # Get summoner_id
    url = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(region, username)
    r = requests.get(url, headers=header)
    if r.status_code == 200:
        summoner_id = r.json()["id"]
    elif r.status_code == 403:
        print("Your api token is invalid")
        exit(1)
    elif r.status_code == 404:
        print("Error, the user does not exist")
        exit(1)
    else:
        print("Something went wrong.")
        exit(1)

    # Get rank
    url = "https://{}.api.riotgames.com/lol/league/v4/entries/by-summoner/{}".format(region, summoner_id)
    r = requests.get(url, headers=header)
    for league in r.json():
        if league["queueType"] == "RANKED_SOLO_5x5":
            print("{} {} {}".format(league["tier"], league["rank"], league["leaguePoints"]))
            break
    