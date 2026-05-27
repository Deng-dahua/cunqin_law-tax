"""百度URL推送 — 每日限额10条（无ICP备案），自动追踪进度"""
import requests, re, os, json

API = "http://data.zz.baidu.com/urls?site=https://cunqin.tax&token=SWGy4vjzNfOGuuLt"
SITEMAP = r"C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\source\sitemap.xml"
STATE_FILE = r"C:\Users\26726\WorkBuddy\2026-05-20-21-20-24\tools\.baidu_push_state.json"
DAILY_LIMIT = 10

def get_urls():
    with open(SITEMAP, 'r', encoding='utf-8') as f:
        content = f.read()
    return re.findall(r'<loc>(https://cunqin\.tax/[^<]+)</loc>', content)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"pushed": [], "last_push": None}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def push(urls):
    payload = "\n".join(urls)
    headers = {"Content-Type": "text/plain"}
    try:
        resp = requests.post(API, data=payload.encode('utf-8'), headers=headers, timeout=30)
        return resp.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    import datetime
    state = load_state()
    all_urls = get_urls()
    
    # Find unpushed URLs
    pending = [u for u in all_urls if u not in state["pushed"]]
    
    print(f"全站 URL: {len(all_urls)} | 已推送: {len(state['pushed'])} | 待推送: {len(pending)}")
    
    if not pending:
        print("全部 URL 已推送完毕！")
        return
    
    batch = pending[:DAILY_LIMIT]
    print(f"\n本次推送: {len(batch)} 条")
    for u in batch:
        print(f"  {u}")
    
    result = push(batch)
    if result:
        success = result.get('success', 0)
        remain = result.get('remain', '?')
        print(f"\n成功: {success}, 今日剩余: {remain}")
        
        if success > 0:
            state["pushed"].extend(batch)
            state["last_push"] = datetime.date.today().isoformat()
            save_state(state)
            print(f"状态已保存。累计推送: {len(state['pushed'])}/{len(all_urls)}")
    else:
        print("\n推送失败")

if __name__ == '__main__':
    main()
