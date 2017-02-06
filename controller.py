from scraper import *
import json

teams = {'1': 'Arsenal',
         '2': 'Hull City',
         '3': 'Watford',
         '4': 'Manchester United',
         '5': 'Everton',
         '6': 'Middlesbrough'}


class Controller:

    def __init__(self):
        self.supported_tournaments = ['Premier League', 'FA Cup']
        self.bbc_results = BbcScraper(self.supported_tournaments)

    def parse(self, query):
        spl = query.split('/')
        match_status = spl[2].split('=')[1]
        if spl[1].isdigit():
            return self.get_matches_by_team_id(spl[1], match_status)
        else:
            return self.get_matches_by_tournament_name(spl[1], match_status)

    def get_matches_by_tournament_name(self, t_name, match_status=None):
        res = []
        res.extend(self.bbc_results.get_matches_by_tournament_name(t_name, match_status))

        return json.dumps(res)

    def get_matches_by_team_id(self, t_id, match_status=None):
        res = []
        if t_id in teams.keys():
            res.extend(self.bbc_results.get_matches_by_team_name(teams[t_id], match_status))

        return json.dumps(res)

