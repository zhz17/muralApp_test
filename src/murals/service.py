import requests
import time

class MuralService:
    def create_square(self, mural_id: str, shape_data: dict, access_token: str):
        url = f"https://app.mural.co/api/public/v1/murals/{mural_id}/widgets"
        
        # 关键点：将 Token 放入 Authorization Header
        headers = {
            "Authorization": f"Bearer {access_token}",  # Mural 要求 Bearer 格式 [2]
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # 组装正方形的 payload (参考你之前的定义)
        payload = {
            "type": "shape",
            "x": shape_data.x,
            "y": shape_data.y,
            "style": {"shape": "rectangle"} 
            # ... 其他参数
        }

        # 发送请求
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_mural_details(self, mural_id: str, access_token: str) -> dict:
        """验证 Mural 是否存在并获取信息"""
        url = f"https://app.mural.co/api/public/v1/murals/{mural_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            raise ValueError("Mural ID 不存在")
        response.raise_for_status()
        
        return response.json()

    def create_shapes_batch(self, mural_id: str, shapes: list, access_token: str) -> dict:
        """循环解析并绘制"""
        results = {"success_count": 0, "fail_count": 0, "errors": []}
        
        for index, shape in enumerate(shapes):
            try:
                # 复用已有的 create_square 方法
                # 注意：这里我们直接透传 Pydantic 对象
                self.create_square(mural_id, shape, access_token)
                results["success_count"] += 1
                
                # 稍微暂停一下防止触发 Mural 的 Rate Limit (API 速率限制)
                time.sleep(0.1) 
                
            except Exception as e:
                results["fail_count"] += 1
                results["errors"].append(f"Shape #{index+1} failed: {str(e)}")
        
        return results
mural_service = MuralService()