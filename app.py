from flask import Flask, render_template, session, redirect, url_for, request, flash, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def display_timezone_info():
    url = 'https://api-american-football.p.rapidapi.com/timezone'
    headers = {
        'X-RapidAPI-Key': 'c3ebf7c1f3msh249690003386ae4p1cb0d9jsnb4664232a801',
        'X-RapidAPI-Host': 'api-american-football.p.rapidapi.com'
    }
    try:
        response = requests.get(url, headers=headers)
        timezone_data = response.json()
        # Pass the data to the template for rendering
    except requests.exceptions.RequestException as e:
        return f'Error: {e}'

    url = 'https://api-american-football.p.rapidapi.com/seasons'

    try:
        response = requests.get(url, headers=headers)
        season_data = response.json()
        # Pass the data to the template for rendering
        return render_template('index.html', timezone_data = timezone_data, season_data=season_data)
    except requests.exceptions.RequestException as e:
        return f'Error: {e}'

@app.route('/team', methods = ['POST'])
def get_team():
    # get team name from the dropdown menu
    team_name = request.form.get('team_name')
    if not team_name:
        return "No team name provided"
    # team names
    url_team = "https://api-american-football.p.rapidapi.com/teams"
    
    # team id's
    url_id = "https://api-american-football.p.rapidapi.com/players"
    # header
    headers = {
        "X-RapidAPI-Key": "c3ebf7c1f3msh249690003386ae4p1cb0d9jsnb4664232a801",
        "X-RapidAPI-Host": "api-american-football.p.rapidapi.com"
    }
    # get the logo using the team data
    querystring_team = {"name": team_name}
    print ('querystring_team', querystring_team)
    
    
    try:
        response_team = requests.get(url_team, headers=headers, params=querystring_team)
        print ('response_team', response_team)
        data = response_team.json()
        team_logo = data['response'][0]['logo']
        #return render_template('team.html',team_logo = team_logo) # Return the team data as JSON response
    except requests.exceptions.RequestException as e:
         return f'Error: {e}'
    #-----------------------------------------------------------------------------------------

    # get the team_id using the team data
    team_id = data['response'][0]['id']
    querystring_id = {"team": team_id, "season": "2022"}
    print ('team id', team_id)
    print ('querystring_id', querystring_id)

    try:
        response_id = requests.get(url_id, headers=headers, params=querystring_id)
        print ('response_id', response_id)
        data_id = response_id.json()
        #print ('data id', data_id)
        player_names = [player['name'] for player in data_id['response']]
        player_id = [player['id'] for player in data_id['response']]
        global player_id_name
        player_id_name = []
        for i in range(len(player_id)):
            player = {'id': player_id[i], 'name': player_names[i]}
            player_id_name.append(player)
        # print (player_id_name)
    except requests.exceptions.RequestException as e:
         return f'Error: {e}'

    #-----------------------------------------------------------------------------------------
    
    
    
    return render_template('team.html',team_logo = team_logo, player_names = player_names, player_id_name = player_id_name) # Return the team data as JSON response

# get the player stats for a user to view

@app.route('/player_stats.html/<int:player_id>', methods = ['GET'])
def player_stats(player_id):
    # get stats from API using the player_id
    url_player = "https://api-american-football.p.rapidapi.com/players"
    url_stats = "https://api-american-football.p.rapidapi.com/players/statistics"
    headers = {
        "X-RapidAPI-Key": "c3ebf7c1f3msh249690003386ae4p1cb0d9jsnb4664232a801",
        "X-RapidAPI-Host": "api-american-football.p.rapidapi.com"
    }
    
    querystring_stats = {"season":"2022","id":player_id}
    try:
        response_stats = requests.get(url_stats, headers=headers, params=querystring_stats)
        player_stats = response_stats.json()
        player_stats = player_stats['response'][0]['teams'][0]['groups']
        stat_category = []
        for name  in player_stats:
            stat_category.append(name['name'])
        
        
    except requests.exceptions.RequestException as e:
         return f'Error: {e}'
    print (player_stats)

    querystring_player = {"id": player_id}
    try:
        response_image = requests.get(url_player, headers=headers, params=querystring_player)
        player_img = response_image.json()
        player_img = player_img['response'][0]['image']
    except requests.exceptions.RequestException as e:
         return f'Error: {e}'
    return render_template ('player_stats.html', player_stats = player_stats, stat_category = stat_category, player_img = player_img)


if __name__ == '__main__':
    app.run(debug=True)

