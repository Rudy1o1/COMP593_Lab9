import requests


def get_pokemon_info(pokemon_name):


    """
    Gets All information about a specified Pokemon
    :param name: Pokemon name
    :returns: Dictionary of Pokemon Info, if succesful. None, if not.      
    """

    print("Getting Pokemon information...", end=" ")
    
    URL = 'https://pokeapi.co/api/v2/pokemon/'
    response = requests.get(URL + str(pokemon_name))

    if response.status_code == 200:
        print('success')
        return response.json() # Convert response body to a dictionary

    else:
        print('failed. Response code:', response.status_code)
        return

def get_pokemon_image_url(name):

    pokemon_dict= get_pokemon_info(name)

    if pokemon_dict:
        return pokemon_dict['sprites']['other']['official-artwork']['front_default']

def get_pokemon_list(limit=100, offeset=0):

    url = 'https://pokeapi.co/api/v2/pokemon'

    params = {
        'limit': limit,
        'offeset':offeset
    }

    resp_msg = requests.get(url, params=params)

    if resp_msg.status_code == 200:
        
        resp_dict = resp_msg.json()
        return [p['name'] for p in resp_dict['results']]
    
    else:
        print('Failed to get Pokemon list.')
        print('Response code:', resp_msg.status_code)
        print(resp_msg.text)