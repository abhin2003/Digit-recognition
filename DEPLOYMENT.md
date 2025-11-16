# 🚀 Deployment Guide

This guide covers multiple deployment options for the Digit Recognition Web App.

## 📋 Prerequisites

- Python 3.11+
- `bestmodel.h5` file in the project root
- All dependencies from `requirements-web.txt`

---

## 🌐 Deployment Options

### 1. **Render.com** (Recommended - Free Tier Available)

**Steps:**

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a new Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Or use the Render CLI

3. **Configure the service:**
   - **Name:** `digit-recognition` (or your choice)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements-web.txt`
   - **Start Command:** `python web_app_production.py`
   - **Plan:** Free (or paid for better performance)

4. **Set Environment Variables:**
   - `PORT`: `5000` (auto-set by Render)
   - `FLASK_ENV`: `production`
   - `MODEL_PATH`: `bestmodel.h5`

5. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy

**Or use Render.yaml:**
- Push `render.yaml` to your repo
- Render will auto-detect and use it

**Note:** Free tier spins down after 15 minutes of inactivity. First request may take ~30 seconds.

---

### 2. **Railway.app** (Easy & Fast)

**Steps:**

1. **Install Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login:**
   ```bash
   railway login
   ```

3. **Initialize project:**
   ```bash
   railway init
   ```

4. **Deploy:**
   ```bash
   railway up
   ```

5. **Set environment variables** (if needed):
   ```bash
   railway variables set FLASK_ENV=production
   ```

**Or via Railway Dashboard:**
- Go to [railway.app](https://railway.app)
- Click "New Project" → "Deploy from GitHub repo"
- Select your repository
- Railway auto-detects Python and deploys

---

### 3. **Heroku** (Classic Platform)

**Steps:**

1. **Install Heroku CLI:**
   - Download from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create app:**
   ```bash
   heroku create your-app-name
   ```

4. **Set buildpacks:**
   ```bash
   heroku buildpacks:set heroku/python
   ```

5. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

6. **Open app:**
   ```bash
   heroku open
   ```

**Note:** Heroku free tier is no longer available. Paid plans start at $5/month.

---

### 4. **Docker Deployment** (Any Platform)

**Build and run locally:**

```bash
# Build the image
docker build -t digit-recognition .

# Run the container
docker run -p 5000:5000 digit-recognition
```

**Deploy to Docker Hub:**

```bash
# Tag the image
docker tag digit-recognition yourusername/digit-recognition

# Push to Docker Hub
docker push yourusername/digit-recognition
```

**Deploy to platforms that support Docker:**
- **Fly.io:** `flyctl launch`
- **DigitalOcean App Platform:** Connect Docker Hub
- **AWS ECS/Fargate:** Use Docker image
- **Google Cloud Run:** `gcloud run deploy`

---

### 5. **VPS Deployment** (DigitalOcean, AWS EC2, etc.)

**Steps:**

1. **SSH into your server:**
   ```bash
   ssh user@your-server-ip
   ```

2. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   ```

3. **Clone your repository:**
   ```bash
   git clone your-repo-url
   cd digit-recognition
   ```

4. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements-web.txt
   ```

5. **Run with Gunicorn (production WSGI server):**
   ```bash
   pip3 install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 web_app_production:app
   ```

6. **Set up Nginx reverse proxy** (optional but recommended):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

7. **Use systemd for auto-start:**
   Create `/etc/systemd/system/digit-recognition.service`:
   ```ini
   [Unit]
   Description=Digit Recognition Web App
   After=network.target

   [Service]
   User=your-user
   WorkingDirectory=/path/to/digit-recognition
   ExecStart=/usr/bin/gunicorn -w 4 -b 0.0.0.0:5000 web_app_production:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Then:
   ```bash
   sudo systemctl enable digit-recognition
   sudo systemctl start digit-recognition
   ```

---

### 6. **Google Cloud Run** (Serverless)

**Steps:**

1. **Install Google Cloud SDK:**
   ```bash
   # Follow: https://cloud.google.com/sdk/docs/install
   ```

2. **Build and push container:**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/digit-recognition
   ```

3. **Deploy:**
   ```bash
   gcloud run deploy digit-recognition \
     --image gcr.io/YOUR_PROJECT_ID/digit-recognition \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

---

### 7. **AWS Elastic Beanstalk**

**Steps:**

1. **Install EB CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Initialize:**
   ```bash
   eb init -p python-3.11 digit-recognition
   ```

3. **Create environment:**
   ```bash
   eb create digit-recognition-env
   ```

4. **Deploy:**
   ```bash
   eb deploy
   ```

---

## 🔧 Production Considerations

### Using Gunicorn (Recommended for Production)

Replace Flask's development server with Gunicorn:

1. **Add to requirements-web.txt:**
   ```
   gunicorn==21.2.0
   ```

2. **Update Procfile:**
   ```
   web: gunicorn -w 4 -b 0.0.0.0:$PORT web_app_production:app
   ```

3. **Or run directly:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 web_app_production:app
   ```

### Environment Variables

Set these in your deployment platform:

- `PORT`: Server port (usually auto-set by platform)
- `FLASK_ENV`: `production` (disables debug mode)
- `MODEL_PATH`: Path to model file (default: `bestmodel.h5`)

### File Size Limits

- Ensure `bestmodel.h5` is included in deployment
- Some platforms have file size limits (check your platform's docs)
- Model is ~4.8 MB, should be fine on most platforms

---

## 📝 Quick Deploy Commands

### Render.com
```bash
# Using Render CLI
render deploy
```

### Railway
```bash
railway up
```

### Heroku
```bash
git push heroku main
```

### Docker
```bash
docker build -t digit-recognition . && docker run -p 5000:5000 digit-recognition
```

---

## ✅ Post-Deployment Checklist

- [ ] App is accessible via URL
- [ ] Health endpoint works: `https://your-app.com/health`
- [ ] Can draw and get predictions
- [ ] Model loads correctly (check logs)
- [ ] HTTPS enabled (if using custom domain)
- [ ] Error handling works
- [ ] Performance is acceptable

---

## 🐛 Troubleshooting

**Issue: Model not found**
- Ensure `bestmodel.h5` is in the project root
- Check `MODEL_PATH` environment variable

**Issue: Port binding error**
- Use `PORT` environment variable
- Check platform's port requirements

**Issue: Memory errors**
- TensorFlow can be memory-intensive
- Consider using a platform with more RAM
- Or optimize model loading

**Issue: Slow predictions**
- First prediction may be slow (model loading)
- Consider model warmup on startup
- Use GPU if available

---

## 📚 Additional Resources

- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)
- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Docker Documentation](https://docs.docker.com)

---

## 💡 Recommended Platforms

**For beginners:** Render.com or Railway.app (easiest setup)  
**For production:** AWS, Google Cloud, or VPS with Gunicorn  
**For serverless:** Google Cloud Run or AWS Lambda (with modifications)  
**For containers:** Docker on any platform

