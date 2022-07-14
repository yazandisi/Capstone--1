import requests
import datetime
def search_logic(form,data,c_id,a_id ):
    """Uses IGDB API to get JSON with game details using string"""
    data.clear()
    print(datetime.datetime.now().timestamp())
    title = form.title.data
    url = "https://api.igdb.com/v4/games"
   
    payload = f"fields id,name, summary, url, screenshots.url; search \"{title}\";\n\n\n where screenshots > 0; where videos > 0;"
    headers = {
    'Client-ID': c_id,
    'Authorization': a_id,
    'Content-Type': 'text/plain'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    
    
    print('**********PRINT TIME****************')
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    info = response.json()
    return info

def search_by_id_logic(id,data,c_id,a_id ):
    """Uses IGDB API to return JSON using ID"""
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
    """Uses IDGB API to get gameplay/trailer video"""
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

def get_live_video(game_name,c_id,a_id):
    """Uses twitch API to get streamer indo"""
    url = f"https://api.twitch.tv/helix/search/channels?query={game_name}&live_only=true"
    payload = ""
    headers = {
        'Client-ID': c_id,
        'Authorization': a_id,
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    info = response.json()

    try:
        check_live = [g['is_live'] for g in info['data']].index(True)
        dis_name = info['data'][check_live]['display_name']
    except:
        dis_name = "yazandisi"
    
    return dis_name

