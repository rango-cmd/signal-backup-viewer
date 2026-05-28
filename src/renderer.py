import os
import zipfile

def generate_html_output(recipients, chat_to_recipient, chats, chat_meta, self_real_name, disk_cache, tz_suffix):
    html_start = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Telegram Data Export</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ background: #fdfdfd; color: #000000; font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-size: 14px; margin: 0; padding: 0; }}
        .page_wrap {{ display: flex; width: 100vw; height: 100vh; overflow: hidden; }}
        .sidebar {{ width: 360px; background: #ffffff; border-right: 1px solid #e6e6e6; display: flex; flex-direction: column; flex-shrink: 0; }}
        .sidebar-nav {{ display: flex; background: #f8fafc; border-bottom: 1px solid #e6e6e6; }}
        .nav-tab {{ flex: 1; text-align: center; padding: 14px 0; cursor: pointer; font-weight: bold; color: #707579; border-bottom: 2px solid transparent; }}
        .nav-tab.active {{ color: #3a6d99; border-bottom: 2px solid #3a6d99; }}
        .list-container {{ overflow-y: auto; flex: 1; display: none; }}
        .list-container.active {{ display: block; }}
        .chat-item {{ display: flex; align-items: center; padding: 11px 18px; cursor: pointer; border-bottom: 1px solid #f9f9f9; text-decoration: none; }}
        .chat-item:hover {{ background: #f4f4f5; }}
        .chat-item.active {{ background: #419fd9; }}
        .chat-item.active .name, .chat-item.active .preview, .chat-item.active .meta-badge {{ color: #ffffff !important; }}
        .chat-item.active .tag-pinned {{ background: rgba(255,255,255,0.2); color: #fff; }}
        .userpic {{ width: 44px; height: 44px; border-radius: 50%; color: #ffffff; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 14px; flex-shrink: 0; font-size: 16px; }}
        .chat-info {{ overflow: hidden; flex: 1; }}
        .name-row {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 2px; }}
        .name {{ font-weight: bold; font-size: 14.5px; color: #000000; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .preview {{ font-size: 13px; color: #707579; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .meta-badge {{ font-size: 11px; color: #a3a3a3; }}
        .tag-pinned {{ background: #e4eaf0; color: #55677d; padding: 1px 5px; border-radius: 4px; font-size: 10px; font-weight: bold; margin-left: 5px; }}
        .tag-timer {{ background: rgba(231, 111, 81, 0.15); color: #e76f51; padding: 2px 6px; border-radius: 4px; font-size: 11px; margin-left: 8px; font-weight: normal; }}
        .main {{ flex: 1; display: flex; flex-direction: column; background: #f4f4f5; overflow: hidden; }}
        .chat-window {{ display: none; flex-direction: column; height: 100%; overflow: hidden; }}
        .chat-window.active {{ display: flex; }}
        .page_header {{ padding: 14px 24px; background: #ffffff; border-bottom: 1px solid #e6e6e6; display: flex; align-items: center; z-index: 10; }}
        .page_header .name {{ font-size: 15px; font-weight: bold; display: flex; align-items: center; }}
        .messages-area {{ flex: 1; overflow-y: auto; padding: 20px 0; background: #dbecea; }} 
        .history {{ max-width: 720px; width: 100%; margin: 0 auto; padding: 0 20px; display: flex; flex-direction: column; }}
        .message_row {{ display: flex; width: 100%; margin-bottom: 8px; align-items: flex-start; }}
        .message_row.received {{ justify-content: flex-start; }}
        .message_row.sent {{ justify-content: flex-end; }}
        .message_box {{ max-width: 68%; background: #ffffff; padding: 8px 12px; border-radius: 12px; position: relative; box-shadow: 0 1px 1px rgba(0,0,0,0.1); }}
        .received .message_box {{ border-bottom-left-radius: 4px; background: #ffffff; color: #000000; margin-left: 10px; }}
        .sent .message_box {{ border-bottom-right-radius: 4px; background: #effdde; color: #000000; margin-right: 10px; }}
        .from_name {{ font-weight: bold; font-size: 13.5px; margin-bottom: 4px; }}
        .received .from_name {{ text-align: left; }}
        .sent .from_name {{ text-align: right; color: #43a047; }}
        .text {{ font-size: 14px; line-height: 1.5; word-wrap: break-word; white-space: pre-wrap; }}
        .date_stamp {{ float: right; font-size: 11px; color: #a3a3a3; margin-top: 5px; margin-left: 12px; }}
        .clear {{ clear: both; }}
        .img-container {{ margin: 5px 0; border-radius: 6px; overflow: hidden; display: block; }}
        .img-attach {{ max-width: 100%; max-height: 340px; border-radius: 6px; display: block; }}
        .service {{ text-align: center; margin: 12px 0; width: 100%; }}
        .service_message {{ background: rgba(214, 227, 235, 0.8); color: #4a5768; padding: 4px 14px; border-radius: 12px; font-size: 12px; display: inline-block; }}
    </style>
</head>
<body>
    <div class="page_wrap">
        <div class="sidebar">
            <div class="sidebar-nav">
                <div class="nav-tab active" onclick="switchTab('chat-list-pane', this)">Chats</div>
                <div class="nav-tab" onclick="switchTab('contact-list-pane', this)">Contacts</div>
            </div>
            <div id="chat-list-pane" class="list-container active">
"""

    contact_pane_html = '</div><div id="contact-list-pane" class="list-container">'
    content_area = '</div></div><div class="main">'
    
    sorted_chats = sorted(chats.items(), key=lambda x: (chat_meta.get(x[0], {'pinnedOrder': float('inf')})['pinnedOrder'], -len(x[1])))
    ext_map = {'image/jpeg': '.jpeg', 'image/jpg': '.jpg', 'image/png': '.png', 'video/mp4': '.mp4', 'text/plain': '.txt'}

    # 取得原始壓縮檔路徑來執行隨選解壓
    zip_path = args_file_placeholder = list(disk_cache.values())[0]['zip_internal_path'] if disk_cache else ""
    
    for chat_id, messages in sorted_chats:
        if not messages: continue
        
        last_item = messages[-1]
        last_msg_text = "Photo"
        if 'standardMessage' in last_item:
            last_msg_text = last_item['standardMessage'].get('text', {}).get('body', 'Photo')
        elif 'updateMessage' in last_item:
            last_msg_text = "Service message"
        last_msg_text = last_msg_text.replace("￼", "Photo")

        target_recipient_id = chat_to_recipient.get(chat_id)
        room = recipients.get(target_recipient_id, {'name': f'Chat #{chat_id}', 'is_group': False, 'color': '#5288c1', 'initial': 'C'})
        
        meta = chat_meta.get(chat_id, {'pinnedOrder': float('inf'), 'expirationTimerMs': None})
        expiration_tag = f'<span class="tag-timer">{meta["expirationTimerMs"]}</span>' if meta['expirationTimerMs'] else ''
        pinned_badge = '<span class="tag-pinned">pinned</span>' if meta['pinnedOrder'] != float('inf') else ''

        html_start += f"""
        <div class="chat-item" id="menu-{chat_id}" onclick="showChat('{chat_id}')">
            <div class="userpic" style="background: {room['color']}">{room['initial']}</div>
            <div class="chat-info">
                <div class="name-row">
                    <div class="name">{room['name']} {pinned_badge}</div>
                    <span class="meta-badge">{len(messages)} msgs</span>
                </div>
                <div class="preview">{last_msg_text[:20]}</div>
            </div>
        </div>
        """
        
        if not room.get('is_group'):
            contact_pane_html += f"""
            <div class="chat-item" id="contact-menu-{chat_id}" onclick="switchTab('chat-list-pane', document.querySelector('.nav-tab')); showChat('{chat_id}')">
                <div class="userpic" style="background: {room['color']}">{room['initial']}</div>
                <div class="chat-info"><div class="name-row"><div class="name">{room['name']}</div></div><div class="preview">Open chat history</div></div>
            </div>
            """

        content_area += f"""
        <div class="chat-window" id="chat-{chat_id}">
            <div class="page_header">
                <div class="userpic" style="width:34px; height:34px; font-size:13px; background: {room['color']}; margin-right: 12px;">{room['initial']}</div>
                <div class="name"><strong>{room['name']}</strong> {expiration_tag}</div>
            </div>
            <div class="messages-area"><div class="history">
        """
        
        for item in messages:
            ts = int(item['dateSent']) / 1000
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts)) + tz_suffix
            
            if 'standardMessage' in item:
                msg = item['standardMessage']
                body = msg.get('text', {}).get('body', '').replace("￼", "")
                is_inc = 'incoming' in item
                
                author = recipients.get(item.get('authorId'), {'name': f'User {item.get("authorId")}', 'color': '#3a6d99', 'initial': 'U'})
                display_name = author['name'] if is_inc else self_real_name
                display_color = author['color'] if is_inc else "#43a047"
                
                content_area += f'<div class="message_row {"received" if is_inc else "sent"}">'
                if is_inc:
                    content_area += f'<div class="userpic" style="width:34px; height:34px; font-size:12px; background: {author["color"]}">{author["initial"]}</div>'
                
                content_area += f"""<div class="message_box">
                        <div class="from_name" style="color: {display_color}">{display_name}</div>
                        <div class="text">"""
                
                if 'attachments' in msg:
                    for att in msg['attachments']:
                        info = att.get('pointer', {})
                        j_size = info.get('locatorInfo', {}).get('size') if info.get('locatorInfo') else None
                        j_ext = ext_map.get(info.get('contentType', '')) or os.path.splitext(info.get('fileName', ''))[1].lower()
                        
                        composite_key = (j_size, j_ext)
                        if j_size and j_ext and composite_key in disk_cache:
                            meta_info = disk_cache[composite_key]
                            internal_src = meta_info['zip_internal_path']
                            out_dir = meta_info['target_dir']
                            
                            # 隨選即時解壓：僅將正確配對到的檔案寫入輸出資料夾中
                            full_out_path = os.path.join(out_dir, internal_src)
                            if not os.path.exists(full_out_path):
                                os.makedirs(os.path.dirname(full_out_path), exist_ok=True)
                                # 追溯最外層的真正 ZIP 檔案位置解壓
                                import sys
                                main_zip_file = sys.argv[sys.argv.index('-f') + 1]
                                with zipfile.ZipFile(main_zip_file, 'r') as rn_z:
                                    with rn_z.open(internal_src) as source_bytes, open(full_out_path, 'wb') as target_bytes:
                                        target_bytes.write(source_bytes.read())
                            
                            content_area += f'<div class="img-container"><a href="{internal_src}" target="_blank"><img class="img-attach" src="{internal_src}"></a></div>'
                        else:
                            content_area += f'<div style="color:#707579; font-size:12px; font-style:italic;">[Media: {info.get("fileName", "Photo")}]</div>'
                
                if body: content_area += f'<div>{body}</div>'
                content_area += f'<span class="date_stamp">{time_str}</span></div><div class="clear"></div></div></div>'
            
            elif 'updateMessage' in item:
                content_area += f'<div class="service"><div class="service_message">System Notification Update | {time_str}</div></div>'
        content_area += '</div></div></div>'

    js_script = """
    <script>
        function switchTab(paneId, tabEl) {
            document.querySelectorAll('.list-container, .nav-tab').forEach(el => el.classList.remove('active'));
            document.getElementById(paneId).classList.add('active');
            tabEl.classList.add('active');
        }
        function showChat(id) {
            document.querySelectorAll('.chat-window, .chat-item').forEach(el => el.classList.remove('active'));
            const tc = document.getElementById('chat-' + id), tm = document.getElementById('menu-' + id), tcm = document.getElementById('contact-menu-' + id);
            if(tc) tc.classList.add('active'); if(tm) tm.classList.add('active'); if(tcm) tcm.classList.add('active');
            if(tc) { const ma = tc.querySelector('.messages-area'); if(ma) ma.scrollTop = ma.scrollHeight; }
        }
        window.onload = function() { const first = document.querySelector('#chat-list-pane .chat-item'); if(first) first.click(); }
    </script>
    """
    return html_start + contact_pane_html + content_area + js_script + "</div></body></html>"