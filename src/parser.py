import json
import time
import collections

def get_tz_str():
    offset = -time.timezone if time.daylight == 0 else -time.altzone
    hours = offset // 3600
    minutes = (abs(offset) % 3600) // 60
    return f" (UTC{hours:+03d}{minutes:02d})"

def format_expiration_time(ms):
    if not ms: return None
    seconds = int(ms) // 1000
    if seconds < 60: return f"{seconds}s"
    minutes = seconds // 60
    if minutes < 60: return f"{minutes}m"
    hours = minutes // 60
    if hours < 24: return f"{hours}h"
    return f"{hours // 24}d"

def parse_signal_backup(file_path):
    recipients = {}       
    chat_to_recipient = {} 
    chats = collections.defaultdict(list)
    chat_meta = {} 
    self_real_name = "User" 
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            try: data = json.loads(line)
            except: continue
            
            if 'account' in data:
                acc = data['account']
                if acc.get('givenName'):
                    self_real_name = acc.get('givenName')
                continue

            if 'recipient' in data:
                r = data['recipient']
                rid = r.get('id')
                
                color_map = {
                    "A100": "#4f9cd4", "A110": "#52b69a", "A120": "#76c893",
                    "A130": "#e76f51", "A140": "#f4a261", "A150": "#e9c46a",
                    "A160": "#457b9d", "A170": "#a2d2ff", "A180": "#bde0fe",
                    "A190": "#ffafcc", "A200": "#ffc8dd", "A210": "#cdb4db"
                }
                raw_color = r.get('avatarColor', 'A100')
                color = color_map.get(raw_color, "#95a5a6")

                if 'group' in r:
                    group_info = r['group']
                    snapshot = group_info.get('snapshot', {})
                    title_obj = snapshot.get('title', {})
                    group_title = title_obj.get('title') or "Unknown Group"
                    recipients[rid] = {'name': group_title, 'is_group': True, 'color': color, 'initial': group_title[:1].upper()}
                elif 'contact' in r:
                    contact = r['contact']
                    name = contact.get('profileGivenName') or contact.get('systemGivenName') or f"User {rid}"
                    recipients[rid] = {'name': name, 'is_group': False, 'color': color, 'initial': name[:1].upper()}
                elif 'self' in r:
                    name = r['self'].get('profileGivenName') or r['self'].get('systemGivenName') or self_real_name
                    recipients[rid] = {'name': name, 'is_group': False, 'color': "#5288c1", 'initial': name[:1].upper()}
            
            elif 'chat' in data:
                c = data['chat']
                cid = c.get('id')
                chat_to_recipient[cid] = c.get('recipientId')
                chat_meta[cid] = {
                    'pinnedOrder': c.get('pinnedOrder') if c.get('pinnedOrder') is not None else float('inf'),
                    'expirationTimerMs': format_expiration_time(c.get('expirationTimerMs'))
                }
            
            elif 'chatItem' in data:
                item = data['chatItem']
                chats[item.get('chatId', 'unknown_chat')].append(item)
                
    return recipients, chat_to_recipient, chats, chat_meta, self_real_name