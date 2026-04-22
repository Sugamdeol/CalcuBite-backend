# 🥗 CalcuBite

An AI-powered food analysis tool that identifies food from images and provides detailed nutritional information using Pollinations AI.

![CalcuBite](https://img.shields.io/badge/CalcuBite-AI%20Food%20Analysis-green)
![Flask](https://img.shields.io/badge/Flask-3.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- 📸 **Image Upload**: Drag & drop or click to upload food photos
- 🤖 **AI Analysis**: Uses Pollinations AI for food recognition
- 📊 **Nutrition Facts**: Calories, protein, carbs, fat, fiber, sugar, sodium
- 🏷️ **Dietary Tags**: Identifies vegan, keto, high-protein, etc.
- 💡 **Health Insights**: AI-generated health information
- 📱 **Responsive Design**: Works on desktop and mobile

## Tech Stack

- **Backend**: Flask 3.0
- **Frontend**: Vanilla JavaScript + CSS3
- **AI API**: Pollinations AI (Free tier)
- **Deployment**: Render (Free tier)

## Quick Start

### Local Development

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd calcubite
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run the app:**
```bash
python app.py
```

The app will be available at `http://localhost:5000`

### Deploy to Render (Free Tier)

#### Option 1: Using render.yaml (Recommended)

1. **Push code to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

2. **Create Render account:**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

3. **New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml`

4. **Deploy:**
   - Click "Create Web Service"
   - Wait for build & deploy (2-3 minutes)

#### Option 2: Manual Configuration

1. **Create new Web Service on Render**
2. **Configure:**
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Plan**: Free

3. **Add Environment Variables:**
   - `SECRET_KEY`: (generate a random string)
   - `FLASK_ENV`: production

## API Endpoints

### POST /analyze
Analyze a food image and return nutritional information.

**Request:**
```http
POST /analyze
Content-Type: multipart/form-data

image: <image_file>
```

**Response:**
```json
{
  "success": true,
  "food_name": "Grilled Chicken Salad",
  "confidence": "High",
  "nutrition": {
    "calories": 350,
    "protein": 35,
    "carbs": 12,
    "fat": 18,
    "fiber": 4,
    "sugar": 3,
    "sodium": 420
  },
  "health_insights": "A healthy, protein-rich meal...",
  "dietary_category": "High-protein, Low-carb, Gluten-free",
  "portion_estimate": "~300g serving",
  "raw_analysis": "..."
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "CalcuBite API",
  "version": "1.0.0"
}
```

## Project Structure

```
calcubite/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment config
├── .env.example        # Environment variables template
├── README.md           # This file
├── uploads/            # Temporary upload storage
├── static/
│   ├── css/
│   │   └── style.css   # App styles
│   └── js/
│       └── app.js      # Frontend logic
└── templates/
    └── index.html      # Main UI
```

## How It Works

1. **Image Upload**: User uploads a food photo via drag-drop or file picker
2. **Base64 Encoding**: Image is converted to base64 for API transmission
3. **AI Analysis**: Pollinations AI analyzes the image and generates:
   - Food identification
   - Nutritional estimates
   - Health insights
   - Dietary classifications
4. **Result Display**: Formatted results shown with visual nutrition cards

## Limitations

- Nutritional values are **estimates** based on AI analysis
- Portion sizes are approximations
- Accuracy depends on image quality and clarity
- Not a substitute for professional dietary advice

## Customization

### Styling
Edit `static/css/style.css` to customize:
- Colors (CSS variables at top of file)
- Layout and spacing
- Animations

### Analysis Prompt
Edit the `analyze_food_with_pollinations()` function in `app.py` to customize:
- Analysis depth
- Output format
- Additional nutritional fields

## Troubleshooting

### Common Issues

**Upload fails:**
- Check file size (max 16MB)
- Verify file type (JPG, PNG, GIF, WebP)

**Analysis timeout:**
- Pollinations AI may be slow during peak times
- Timeout is set to 60 seconds

**Deployment fails on Render:**
- Check Python version in render.yaml
- Verify all dependencies in requirements.txt

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use for personal or commercial projects.

## Credits

- Built with [Flask](https://flask.palletsprojects.com/)
- AI powered by [Pollinations](https://pollinations.ai)
- Icons and emojis from open source projects

---

**Disclaimer**: CalcuBite provides estimated nutritional information for educational purposes only. Always consult a healthcare professional or registered dietitian for personalized dietary advice.
