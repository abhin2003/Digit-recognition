# 🖊️ Handwritten Digit Recognition Project

## 📌 Project Overview
This project implements a complete **handwritten digit recognition system** using deep learning.  
It consists of two main components:

1. **CNN Model Training** – Training a Convolutional Neural Network on the MNIST dataset.  
2. **Real-time Digit Recognition App** – A Pygame-based application for drawing and recognizing digits in real time.  

---

## 📊 Dataset: MNIST
**MNIST (Modified National Institute of Standards and Technology database)** is the standard benchmark for handwritten digit classification.  

- **Classes:** 10 digits (0–9)  
- **Training Images:** 60,000  
- **Test Images:** 10,000  
- **Image Size:** 28×28 pixels  
- **Color:** Grayscale (0–255 pixel values)  

**Characteristics:**
- Centered, normalized digits  
- White digits on black background  
- Pre-split into training and testing sets  

---

## 🧠 Model Architecture: CNN
**Input Shape:** (28, 28, 1)  


- **Total Layers:** 7  
- **Trainable Parameters:** ~1.2M  
- **Activation Functions:** ReLU (hidden), Softmax (output)  
- **Regularization:** Dropout (0.25)  

---

## ⚙️ Training Configuration
**Preprocessing:**
- Normalize pixel values → `[0, 255]` → `[0, 1]`  
- Reshape: `(28, 28)` → `(28, 28, 1)`  
- One-Hot Encode labels (e.g., `5 → [0,0,0,0,0,1,0,0,0,0]`)  

**Training Setup:**
- Optimizer: **Adam**  
- Loss: **Categorical Cross-Entropy**  
- Metric: **Accuracy**  
- Epochs: **50** (with early stopping)  
- Validation Split: **30%**  
- Batch Size: **32**  

**Features:**
- Early Stopping (patience = 4)  
- Model Checkpoint (saves best model as `bestmodel.h5`)  

---

## 🖥️ Applications

### Pygame Desktop App
The **Digit Recognizer App** allows users to draw digits and get instant recognition.  

**Features:**
- **Canvas Size:** 640×480 pixels  
- **Drawing Color:** White on black background  
- **Brush:** Circle with 4-pixel radius  
- **Clear Canvas:** Press **`n`**  
- **Model:** Pre-trained CNN (`bestmodel.h5`)

### 🌐 Web Application
A modern browser-based interface for digit recognition.

**Features:**
- **Browser-based canvas** - Draw digits directly in your web browser
- **Real-time predictions** - Get instant digit recognition results
- **Confidence scores** - See prediction confidence and all digit probabilities
- **Mobile-friendly** - Works on touch devices
- **Modern UI** - Beautiful, responsive design

**Running the Web App:**
```bash
# Install web dependencies
pip install -r requirements-web.txt

# Start the Flask server
python web_app.py

# Open http://localhost:5000 in your browser
```  



---

## 🔄 Project Workflow
**Phase 1: Model Development**  
- Load MNIST → Explore data → Preprocess  
- Build CNN → Train → Evaluate  
- Save model as `bestmodel.h5`  

**Phase 2: Application Development**  
- Build Pygame UI  
- Load trained model  
- Preprocess user-drawn digits  
- Predict & display results  

---

## 🛠️ Technologies Used
**Machine Learning:**  
- TensorFlow / Keras  
- NumPy  
- Matplotlib  

**Desktop Application:**  
- Pygame (GUI)  
- OpenCV (image preprocessing)  
- NumPy

**Web Application:**  
- Flask (backend)  
- HTML5 Canvas (frontend)  
- JavaScript  
- OpenCV (image preprocessing)  
- Pillow (image processing)  

---

## 📈 Model Performance
- **Expected Accuracy:** 95–99% on MNIST test set  
- **Real-time Inference:** Near-instantaneous prediction  
- **Model Size:** ~4.8 MB (`.h5`)  

---

## 🚀 Usage Instructions

### 🔹 Pygame Desktop App
1. Install Python 3.11+
2. Run the installer and check "Add python.exe to PATH."
3. Open the project folder in a terminal
4. Install dependencies:
   ```bash
   python -m pip install -r requirements-flex.txt
   ```
5. Run the app:
   ```bash
   python app.py
   ```

### 🌐 Web Application (Local)
1. Install dependencies:
   ```bash
   pip install -r requirements-web.txt
   ```
2. Start the server:
   ```bash
   python web_app.py
   ```
3. Open your browser: `http://localhost:5000`

### 🚀 Deployment
For deploying to production (Render, Railway, Heroku, Docker, etc.), see **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed instructions.