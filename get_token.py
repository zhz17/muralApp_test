import requests

# --- 1. 填入你的配置信息 ---
CLIENT_ID = "你的_CLIENT_ID"          # 替换它
CLIENT_SECRET = "你的_CLIENT_SECRET"  # 替换它
REDIRECT_URI = "http://localhost:8000/callback" # 必须和后台设置完全一致

def get_access_token():
    # --- 2. 这里的 Code 需要你手动运行脚本时输入 ---
    code = input("请粘贴你在浏览器地址栏里复制的 Code: ").strip()

    print("\n正在向 Mural 申请 Token...")

    url = "https://app.mural.co/api/public/v1/auth/token"
    
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status() # 检查是否有错
        
        data = response.json()
        token = data.get("access_token")
        
        print("\n" + "="*40)
        print("🎉 成功拿到 Token！")
        print("="*40)
        print(token)
        print("="*40)
        print("\n请复制上面的 Token 字符串，保存备用。")
        
    except requests.exceptions.HTTPError as err:
        print(f"\n❌ 出错了: {err}")
        print(f"详细信息: {response.text}")

if __name__ == "__main__":
    get_access_token()