# 🖼️ Visual Question Answering System (VQA)

An **Explainable AI-based Visual Question Answering System** that enables users to upload an image and ask questions about it. The system analyzes images using deep learning and provides intelligent answers with support for voice interaction, multilingual translation, Grad-CAM visualization, and PDF report generation.

---

## 🎥 Demo Video

[![Watch Demo]("C:\Users\jjerl\Videos\Screen Recordings\Screen Recording 2026-04-22 205033.mp4")

▶️ Click the image above to watch the full demo

---

## 🚀 Features

* 🧠 **Dual Model Support**

  * Offline Trained Model (ViLT)
  * Gemini Vision API (Online)

* 🖼️ **Image Input**

  * Upload image
  * Image via URL

* ❓ **Question Answering**

  * Manual question input
  * Predefined questions

* 🌍 **Multilingual Support**

  * English, Hindi, Tamil, Malayalam, Telugu

* 🎙️ **Voice Interaction**

  * Speech-to-text (input)
  * Text-to-speech (output)

* 🔥 **Explainable AI**

  * Grad-CAM heatmap visualization

* 📄 **PDF Report**

  * Download Q&A history with image

* 📚 **Session History**

  * Stores previous questions and answers

---

## 🏗️ Project Structure

```bash
visual_question_answering/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env
│
├── model/
│   ├── trained_vqa/        # (Download separately)
│   ├── gemini_api.py
│   ├── gradcam.py
│
├── utils/
│   ├── translator.py
│   ├── voice_utils.py
│   ├── pdf_generator.py
│   ├── image_utils.py
│
├── data/
│   └── my_vqa.json
│
├── assets/
├── reports/
├── train/
├── testing/
```

---

## ⚠️ Important Note (Model Download)

Due to GitHub file size limitations, the trained model is not included in this repository.

👉 Download the model from:
**<img width="263" height="311" alt="image" src="https://github.com/user-attachments/assets/3c5a0354-0cec-4e52-b058-dc04e5e8a1c3" />
**

After downloading, place it in:

```bash
model/trained_vqa/
```

---

## 🛠️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/Visual-Question-Answering-System.git
cd Visual-Question-Answering-System
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv vqa_env
```

Activate:

**Windows**

```bash
vqa_env\Scripts\activate
```

**Mac/Linux**

```bash
source vqa_env/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup Environment Variables

Create `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

## 🧠 How It Works

1. Upload image or provide URL
2. Ask a question
3. System processes:

   * Checks dataset for matching answer
   * Uses ViLT model if needed
   * Or Gemini Vision API
4. Generates answer
5. Optional:

   * Translate answer
   * Voice output
   * Grad-CAM visualization
   * Generate PDF report

---

## 🔬 Technologies Used

* Python
* Streamlit
* PyTorch
* Hugging Face Transformers (ViLT)
* Grad-CAM (Explainable AI)
* Google Gemini API
* SpeechRecognition & gTTS
* ReportLab

---

## 📊 Dataset

Custom dataset (`my_vqa.json`) includes:

* Images
* Questions
* Answers
* Keyword matching

---

## 💡 Key Highlights

* Combines **Computer Vision + NLP**
* Supports **Explainable AI (XAI)**
* Multi-modal system (Image + Text + Voice)
* Interactive UI with Streamlit

---

## 🎯 Future Enhancements

* Cloud deployment (Streamlit Cloud / AWS)
* Improve model accuracy
* Real-time camera input
* Mobile application

---

## 👩‍💻 Author

**Jerlin Ishabel**
MSc Data Science

---


