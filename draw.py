import requests
import json

# ================= 配置区域 =================
MURAL_ID = "您的_MURAL_ID_填在这里"  # 例如 "123456.7890" 或纯数字字符串
ACCESS_TOKEN = "您的_ACCESS_TOKEN_填在这里"
# ===========================================

def create_sticky_note(mural_id, token, text="Hello from API!"):
    """
    在指定 Mural 上创建一个便利贴
    """
    url = f"https://app.mural.co/api/public/v1/murals/{mural_id}/widgets/sticky-note"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        # 加上 User-Agent 防止被防火墙拦截 (解决 WinError 10054)
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 定义便利贴的属性
    payload = {
        "text": text,
        "x": 100,        # 画板上的 X 坐标
        "y": 100,        # 画板上的 Y 坐标
        "width": 150,    # 宽度
        "height": 150,   # 高度
        "color": "#FFEFD5", # 颜色 (黄色)
        "shape": "square"   # 形状
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() # 如果状态码不是 200/201，抛出异常
        
        print("✅ 成功创建便利贴！")
        print("组件 ID:", response.json().get('id'))
        
    except requests.exceptions.HTTPError as err:
        print(f"❌ 请求被拒绝: {err}")
        print("详细信息:", response.text)
    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    create_sticky_note(MURAL_ID, ACCESS_TOKEN, "这是通过 Python 自动创建的！")