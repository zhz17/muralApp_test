html_dashboard = """
<!DOCTYPE html>
<html>
<head>
    <title>Mural Batch Creator</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { border: 1px solid #ccc; padding: 20px; border-radius: 8px; }
        input, textarea, button { width: 100%; margin-bottom: 10px; padding: 10px; box-sizing: border-box; }
        textarea { height: 200px; font-family: monospace; }
        .status { padding: 10px; margin-top: 10px; border-radius: 4px; display: none; }
        .success { background-color: #d4edda; color: #155724; }
        .error { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h1>Mural 批量绘图工具</h1>
    
    <div class="container">
        <!-- 模块 1: 验证 Mural ID -->
        <h3>1. 验证 Mural ID</h3>
        <input type="text" id="muralId" placeholder="输入 Mural ID (例如: workspace.123456)">
        <button onclick="verifyMural()" style="background-color: #007bff; color: white;">Verify Mural ID</button>
        <div id="verifyStatus" class="status"></div>

        <hr>

        <!-- 模块 2: 批量提交 Shape -->
        <h3>2. 提交 JSON 绘图</h3>
        <textarea id="jsonInput" placeholder='[{"x": 100, "y": 100, "width": 100, "height": 100, "color": "#FF0000"}]'></textarea>
        <button onclick="submitShapes()" style="background-color: #28a745; color: white;">Submit Shapes</button>
        <div id="submitStatus" class="status"></div>
    </div>

    <script>
        async function verifyMural() {
            const muralId = document.getElementById('muralId').value;
            const statusDiv = document.getElementById('verifyStatus');
            
            try {
                // 调用后端接口，浏览器会自动带上 Cookie 中的 Token
                const response = await fetch(`/murals/${muralId}/verify`);
                const data = await response.json();
                
                statusDiv.style.display = 'block';
                if (response.ok) {
                    statusDiv.className = 'status success';
                    statusDiv.innerText = `验证成功! Mural 名称: ${data.title}`;
                } else {
                    throw new Error(data.detail || '验证失败');
                }
            } catch (e) {
                statusDiv.className = 'status error';
                statusDiv.innerText = `错误: ${e.message}`;
            }
        }

        async function submitShapes() {
            const muralId = document.getElementById('muralId').value;
            const jsonText = document.getElementById('jsonInput').value;
            const statusDiv = document.getElementById('submitStatus');
            
            if (!muralId) { alert("请先填写 Mural ID"); return; }
            
            try {
                // 解析文本为 JSON 对象
                let shapes;
                try {
                    shapes = JSON.parse(jsonText);
                } catch (e) {
                    throw new Error("JSON 格式错误，请检查输入");
                }

                const response = await fetch(`/murals/${muralId}/batch-shapes`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(shapes)
                });
                
                const result = await response.json();
                statusDiv.style.display = 'block';
                
                if (response.ok) {
                    statusDiv.className = 'status success';
                    statusDiv.innerText = `完成! 成功绘制: ${result.success_count}, 失败: ${result.fail_count}`;
                } else {
                    throw new Error(result.detail || '提交失败');
                }
            } catch (e) {
                statusDiv.className = 'status error';
                statusDiv.innerText = `处理失败: ${e.message}`;
            }
        }
    </script>
</body>
</html>
"""