import urllib.request
from bs4 import BeautifulSoup


class Retriever:
    def get_page(self, path):
        req = urllib.request.Request(path)
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
        return the_page


class Scraper:
    """base class for scrapers. defines common methods and members"""

    def __init__(self, supported_tournaments):
        self.supported_tournaments = supported_tournaments
        self.data_retriever = Retriever()
        self.urls = []

    def get_matches_by_tournament_name(self, t_name):
        pass

    def get_matches_by_team_id(self, t_id):
        pass

    def change_retriever(self, new_retriever):
        self.data_retriever = new_retriever


class BbcScraper(Scraper):
    def __init__(self, supported_tournaments):
        super().__init__(supported_tournaments)
        self.urls.append('http://www.bbc.com/sport/football/results')
        self.urls.append('http://www.bbc.com/sport/football/fixtures')
        self.parser = BbcFormatParser(supported_tournaments)

    def get_matches_by_tournament_name(self, t_name, match_status):
        results = []
        if t_name not in self.supported_tournaments:
            return results

        for url in self.urls:
            html = self.data_retriever.get_page(url)
            results.extend(self.parser.parse_html(html))

        return_lst = []
        for match in results:
            if match['tournament'] != t_name:
                continue

            if match_status is not None:
                if match['status'] != match_status:
                    continue

            return_lst.append(match)
        return return_lst

    def get_matches_by_team_id(self, team_name, match_status):
        results = []
        for url in self.urls:
            html = self.data_retriever.get_page(url)
            results.extend(self.parser.parse_html(html))

        return_lst = []
        for match in results:
            if match['home_team'] == team_name or match['away_team'] == team_name:
                return_lst.append(match)

        return return_lst

    def change_parser(self, new_parser):
        self.parser = new_parser


class FormatParser:
    def __init__(self, supported_tournaments):
        self.supported_tournaments = supported_tournaments

    def update_supported_tournaments(self, new_supported_tournaments):
        self.supported_tournaments = new_supported_tournaments

    def parse_html(self, html):
        pass


class BbcFormatParser(FormatParser):
    def __init__(self, supported_tournaments):
        super().__init__(supported_tournaments)

    def parse_html(self, html):
        """parse the html data by the bbc page format,
        return a result structure"""

        parsed_html = BeautifulSoup(html, "html.parser")
        results_data = parsed_html.find('div', class_="fixtures-table full-table-medium")

        results = []
        start_time = ''
        for tag in results_data.children:
            if tag.name == 'h2':
                start_time = tag.contents[0].strip()
            elif tag.name == 'table':

                # extract league name and check if its in the list
                tournament = tag.find('thead').find_all('th')[1].contents[0].strip()
                if tournament not in self.supported_tournaments:
                    continue

                matches = tag.find('tbody').find_all('tr')
                for match in matches:
                    match_details = match.find('td', class_='match-details')
                    home_team = match_details.find('span', class_='team-home teams').find('a').contents[0].strip()
                    away_team = match_details.find('span', class_='team-away teams').find('a').contents[0].strip()
                    score = match_details.find('span', class_='score')
                    if score is not None:
                        score = score.find('abbr').contents[0].strip()

                    try:
                        home_score = int(score.split('-')[0])
                        away_score = int(score.split('-')[1])
                        status = "played"
                        results.append(
                            {"home_team": home_team, "away_team": away_team, "status": status, "home_score": home_score,
                             "away_score": away_score, "tournament": tournament, "start_time": start_time})
                    except (ValueError, AttributeError):
                        status = "upcoming"
                        results.append({"home_team": home_team, "away_team": away_team, "status": status, "tournament": tournament, "start_time":start_time })

        '''
        # get all dates headers
        all_dates = results_data.find_all('h2')
        all_dates = [x.contents[0].strip() for x in all_dates]

        '''
        return results

