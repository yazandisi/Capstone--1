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



