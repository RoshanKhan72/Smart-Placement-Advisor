from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Smart Placement Advisor - Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #667eea; text-align: center; }
            .form-group { margin: 20px 0; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            button { background: #667eea; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            button:hover { background: #5a6fd8; }
            .result { margin: 20px 0; padding: 20px; background: #f0f9ff; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 AI Smart Placement Advisor</h1>
            <p>Test version - Flask Backend</p>
            
            <div class="form-group">
                <label>CGPA:</label>
                <input type="range" id="cgpa" min="0" max="10" step="0.1" value="7.5" oninput="document.getElementById('cgpaValue').textContent = this.value">
                <span id="cgpaValue">7.5</span>
            </div>
            
            <div class="form-group">
                <label>Skills:</label>
                <select multiple size="5">
                    <option>DSA</option>
                    <option>DBMS</option>
                    <option>OS</option>
                    <option>Python</option>
                    <option>Java</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Number of Projects:</label>
                <input type="number" min="0" max="20" value="2">
            </div>
            
            <button onclick="analyze()">🔍 Analyze My Profile</button>
            
            <div id="result" class="result" style="display: none;">
                <h3>🎯 Placement Probability: 75%</h3>
                <p>Category: <strong style="color: green;">High</strong></p>
                <p>Missing Skills: <span style="color: red;">OS, OOP</span></p>
                <p>💡 Suggestions: Improve OS skills, Add more projects</p>
            </div>
        </div>
        
        <script>
            function analyze() {
                document.getElementById('result').style.display = 'block';
                window.scrollTo(0, document.getElementById('result').offsetTop);
            }
        </script>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    print("📱 Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
