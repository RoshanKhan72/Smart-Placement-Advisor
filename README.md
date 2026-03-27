# 🎯 AI-Based Smart Placement Advisor

A comprehensive Streamlit application that helps students analyze their placement prospects and get personalized improvement suggestions.

## 🚀 Features

### Core Functionality
- **Placement Prediction**: Calculate placement probability using rule-based scoring system
- **Skill Gap Analysis**: Identify missing key skills for better placement chances
- **Improvement Suggestions**: Get personalized recommendations to boost placement prospects
- **Company-wise Predictions**: See chances for different types of companies (TCS/Infosys, Product Companies, Startups)
- **Resume Scoring**: Analyze resume text and get a score out of 100

### User Interface
- Clean, modern design with gradient headers
- Interactive charts and visualizations
- Progress bars and metric cards
- Responsive layout with sidebar inputs
- Color-coded probability categories

## 📋 How to Run

### 🚀 Quick Start (Auto-opens Browser)

**Option 1: Double-click the batch file**
```
run.bat
```

**Option 2: Run the Python starter**
```bash
python start.py
```

**Option 3: Manual Streamlit**
```bash
streamlit run app.py
```

### Prerequisites
- Python 3.7+
- pip package manager

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd "Placement Advisor"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   - Use `run.bat` for automatic browser opening
   - Or use `python start.py` for enhanced startup
   - Or manual: `streamlit run app.py`

## 🎮 How to Use

1. **Fill Your Information** (Sidebar)
   - Adjust CGPA slider (0-10)
   - Enter number of skills and projects
   - Select your technical skills from the list
   - Paste your resume text for analysis

2. **Analyze Your Profile**
   - Click the "Analyze My Profile" button
   - View comprehensive results in the main dashboard

3. **Review Results**
   - Overall placement probability with category (High/Medium/Low)
   - Score breakdown pie chart
   - Company-wise prediction bar chart
   - Skill gap analysis
   - Resume score
   - Personalized improvement suggestions

## 📊 Scoring Algorithm

### Placement Probability Calculation
- **CGPA**: 40% weight
- **Skills**: 30% weight  
- **Projects**: 20% weight
- **Key Skills Bonus**: 10% weight

### Company-wise Predictions
- **TCS/Infosys**: High weight on CGPA (60%)
- **Product Companies**: High weight on skills + projects (70%)
- **Startups**: Balanced approach (35% each)

### Resume Scoring
- Keyword matching (Python, Java, SQL, ML, etc.)
- Length-based bonus
- Maximum score: 100 points

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn (optional)
- **Visualization**: Plotly
- **Styling**: Custom CSS

## 📁 Project Structure

```
Placement Advisor/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## 🎯 Key Features Explained

### 1. Placement Prediction
Uses a sophisticated rule-based algorithm considering:
- Academic performance (CGPA)
- Technical skills count
- Project experience
- Key industry skills

### 2. Skill Gap Analyzer
Compares user skills with industry requirements:
- Required: DSA, DBMS, OS, OOP
- Identifies missing skills
- Provides targeted suggestions

### 3. Improvement Suggestions
Generates personalized recommendations:
- CGPA improvement targets
- Skill acquisition suggestions
- Project recommendations
- Specific skill focus areas

### 4. Company-wise Predictions
Tailored predictions for different company types:
- Service companies (TCS, Infosys)
- Product-based companies
- Startups and emerging companies

### 5. Resume Analysis
Intelligent resume scoring based on:
- Industry keyword presence
- Technical skills mentioned
- Project experience
- Overall content quality

## 🎨 UI Features

- **Gradient headers** for modern look
- **Progress bars** for visual probability display
- **Interactive charts** (pie and bar charts)
- **Color-coded categories** (Green/Yellow/Red)
- **Responsive design** for all screen sizes
- **Metric cards** for key statistics
- **Suggestion boxes** with clear recommendations

## 🚀 Demo Ready

This application is perfect for:
- Hackathon demonstrations
- Student career counseling
- Placement cell activities
- Career development workshops

## 📈 Future Enhancements

- Integration with real placement data
- Machine learning model training
- Company-specific requirements
- Interview preparation module
- Mock interview features

## 🤝 Contributing

Feel free to enhance the application with:
- New features
- UI improvements
- Algorithm optimizations
- Additional company types

## 📞 Support

For any issues or suggestions, please reach out through the project repository.

---

**🚀 AI Smart Placement Advisor - Your Gateway to Better Career Opportunities!**
