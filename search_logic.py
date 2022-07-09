import requests
def search_logic(form,data,c_id,a_id ):
    data.clear()
    title = form.title.data
    url = "https://api.igdb.com/v4/games"
   
    payload = f"fields id,name, summary, url, screenshots.url; search \"{title}\";\n\n\n where screenshots > 0; where videos > 0;"
    headers = {
    'Client-ID': c_id,
    'Authorization': a_id,
    'Content-Type': 'text/plain'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    info = response.json()
    
    return info

def search_by_id_logic(id,data,c_id,a_id ):
    data.clear()
    id = id
    url = "https://api.igdb.com/v4/games"
   
    payload = f"fields id,name, summary, url, screenshots.url,videos; where id = {id};\n\n\n"
    headers = {
    'Client-ID': c_id,
    'Authorization': a_id,
    'Content-Type': 'text/plain'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    info = response.json()
    
    return info

def search_for_vid(id,data,c_id,a_id):
    data.clear()
    url = "https://api.igdb.com/v4/game_videos"

    payload = f"fields video_id; where id = {id};"
    headers = {
    'Client-ID': c_id,
    'Authorization': a_id,
    'Content-Type': 'text/plain'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    info = response.json()
    
    return info

def get_live_video(game_name):
    url = f"https://api.twitch.tv/helix/search/channels?query={game_name}&live_only=true"
    payload = ""
    headers = {
        'Client-ID': 'o5ny07nd7uy2wol6w70f8bo17qhv1a',
        'Authorization': 'Bearer nwylltbgpyzj0hb8xohtrl6y5x7he1'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    info = response.json()
    check_live = [g['is_live'] for g in info['data']]
    
    print([g['is_live'] for g in info['data']])
    print('***************asdadasdasdafsfsef')
 
    # ['is_live']
    try:
        dis_name = info['data'][0]['display_name']
    except:
        dis_name = "yazandisi"
    
    return dis_name

