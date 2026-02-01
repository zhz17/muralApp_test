html_dashboard = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mural Operations Console</title>
    <!-- Fonts: Inter + JetBrains Mono -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0f172a;
            --panel-bg: #1e293b;
            --primary: #3b82f6;
            --primary-hover: #2563eb;
            --success: #10b981;
            --danger: #ef4444;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --border: #334155;
            --input-bg: #020617;
            --glow: 0 0 20px rgba(59, 130, 246, 0.15);
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(99, 102, 241, 0.08) 0%, transparent 40%);
        }

        .dashboard {
            width: 100%;
            max-width: 800px;
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(8px);
        }

        header {
            margin-bottom: 40px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        h1 {
            font-size: 20px;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin: 0;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .status-badge {
            font-size: 12px;
            color: var(--text-muted);
            font-family: 'JetBrains Mono', monospace;
            padding: 4px 8px;
            border: 1px solid var(--border);
            border-radius: 4px;
        }

        .section-title {
            font-size: 14px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }

        .section-title::before {
            content: '';
            display: inline-block;
            width: 6px;
            height: 6px;
            background: var(--primary);
            margin-right: 10px;
            border-radius: 50%;
            box-shadow: 0 0 8px var(--primary);
        }

        .input-group {
            display: flex;
            gap: 12px;
            margin-bottom: 30px;
        }

        .input-wrapper {
            flex: 1;
            position: relative;
        }

        input, textarea {
            width: 100%;
            background: var(--input-bg);
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 14px 16px;
            border-radius: 6px;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            transition: all 0.2s ease;
            box-sizing: border-box;
        }

        textarea {
            font-family: 'JetBrains Mono', monospace;
            min-height: 200px;
            resize: vertical;
            line-height: 1.6;
            font-size: 13px;
        }

        input:focus, textarea:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }

        button {
            background: var(--primary);
            color: white;
            border: none;
            padding: 0 24px;
            font-weight: 500;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 14px;
            min-width: 120px;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 46px; /* Match input height roughly */
        }

        button:hover {
            background: var(--primary-hover);
            box-shadow: var(--glow);
        }

        button:disabled {
            opacity: 0.7;
            cursor: not-allowed;
        }

        .btn-submit {
            width: 100%;
            margin-top: 20px;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        }
        
        .btn-submit:hover {
             box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
        }

        .message-box {
            margin-top: 12px;
            padding: 12px;
            border-radius: 6px;
            font-size: 13px;
            display: none;
            animation: fadeIn 0.3s ease;
        }

        .success {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: #34d399;
        }

        .error {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: #fca5a5;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-5px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Loading Spinner */
        .spinner {
            width: 18px;
            height: 18px;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 0.8s linear infinite;
            display: none;
            margin-right: 8px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .loading .spinner { display: block; }
        
        hr.divider {
            border: 0;
            height: 1px;
            background: var(--border);
            margin: 40px 0;
            opacity: 0.5;
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <header>
            <h1>Mural Command Center</h1>
            <div class="status-badge">SYSTEM READY</div>
        </header>

        <!-- Module 1: Verification -->
        <div class="section">
            <div class="section-title">Target Verification</div>
            <div class="input-group">
                <div class="input-wrapper">
                    <input type="text" id="muralId" placeholder="Enter Mural ID (e.g. mural-uuid-123)">
                </div>
                <button id="btnVerify" onclick="verifyMural()">
                    <div class="spinner"></div>
                    <span>VERIFY TARGET</span>
                </button>
            </div>
            <div id="verifyStatus" class="message-box"></div>
        </div>

        <hr class="divider">

        <!-- Module 2: Payload Execution -->
        <div class="section">
            <div class="section-title">Shape Payload Configuration</div>
            <textarea id="jsonInput" placeholder='[\n  {\n    "x": 100,\n    "y": 100,\n    "width": 200,\n    "height": 150,\n    "style": { "backgroundColor": "#FF0099" }\n  }\n]'></textarea>
            
            <button id="btnSubmit" class="btn-submit" onclick="submitShapes()">
                <div class="spinner"></div>
                <span>EXECUTE DRAWING SEQUENCE</span>
            </button>
            <div id="submitStatus" class="message-box"></div>
        </div>
    </div>

    <script>
        async function verifyMural() {
            const muralId = document.getElementById('muralId').value.trim();
            const statusDiv = document.getElementById('verifyStatus');
            const btn = document.getElementById('btnVerify');
            
            if (!muralId) {
                showStatus(statusDiv, 'Please enter a Mural ID', 'error');
                return;
            }

            setLoading(btn, true);
            statusDiv.style.display = 'none';

            try {
                const response = await fetch(`/murals/${muralId}/verify`);
                const data = await response.json();
                
                if (response.ok) {
                    showStatus(statusDiv, `VERIFIED: ${data.title} [ID: ${data.id}]`, 'success');
                } else {
                    throw new Error(data.detail || 'Verification failed');
                }
            } catch (e) {
                showStatus(statusDiv, `ERROR: ${e.message}`, 'error');
            } finally {
                setLoading(btn, false);
            }
        }

        async function submitShapes() {
            const muralId = document.getElementById('muralId').value.trim();
            const jsonText = document.getElementById('jsonInput').value;
            const statusDiv = document.getElementById('submitStatus');
            const btn = document.getElementById('btnSubmit');
            
            if (!muralId) {
                alert("Target Mural ID required. Please verify first.");
                document.getElementById('muralId').focus();
                return;
            }
            
            try {
                // Pre-validate JSON
                const shapes = JSON.parse(jsonText);
                
                setLoading(btn, true);
                statusDiv.style.display = 'none';

                const response = await fetch(`/murals/${muralId}/batch-shapes`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(shapes)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    const failMsg = result.fail_count > 0 ? ` (${result.fail_count} failed)` : '';
                    showStatus(statusDiv, `SEQUENCE COMPLETE: ${result.success_count} shapes drawn${failMsg}`, result.fail_count > 0 ? 'error' : 'success');
                } else {
                    throw new Error(result.detail || 'Submission failed');
                }
            } catch (e) {
                if (e instanceof SyntaxError) {
                    showStatus(statusDiv, 'INVALID JSON PAYLOAD: Check syntax', 'error');
                } else {
                    showStatus(statusDiv, `EXECUTION ERROR: ${e.message}`, 'error');
                }
            } finally {
                setLoading(btn, false);
            }
        }

        function showStatus(element, message, type) {
            element.innerText = message;
            element.className = `message-box ${type}`;
            element.style.display = 'block';
        }

        function setLoading(btn, isLoading) {
            if (isLoading) {
                btn.classList.add('loading');
                btn.disabled = true;
            } else {
                btn.classList.remove('loading');
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
"""