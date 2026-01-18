# ♻️ SmartBin AI: Intelligent Waste Segregation System

**SmartBin AI** is a real-time, AI-powered application designed to automate waste segregation at the source. It uses advanced Computer Vision and Large Language Models (LLMs) to identify waste items via a webcam and guides the user on which bin to use (Green, Blue, or Red).

> **Tech Stack:** Python | Streamlit | CLIP (Vision) | Llama 3.2 (Logic) | Ollama

---

## 🚀 Key Features

- **👀 Advanced Vision:** Uses OpenAI's **CLIP Model** (via Hugging Face) for highly accurate object detection (distinguishes between similar items like phones and plastic bottles).
- **🧠 Intelligent Decision Making:** Uses **Llama 3.2 (via Ollama)** to logically classify items into Organic, Recyclable, or E-Waste categories.
- **🗣️ Voice Assistance:** Provides audio guidance in **Hinglish** (Hindi + English) using Google TTS, making it accessible to a wider audience.
- **📹 Real-Time Scanning:** Direct webcam integration for instant waste identification.
- **🔒 Privacy First:** The core AI logic runs locally on the device using Ollama.

---

## 🛠️ Tech Stack & Libraries

| Component | Technology Used | Description |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Web-based User Interface for camera & interaction. |
| **Vision Model** | CLIP (OpenAI) | Matches images with text labels (Zero-shot classification). |
| **AI Brain** | Llama 3.2 (Ollama) | Reasons the bin category based on the identified object. |
| **Audio** | gTTS | Converts text instructions to speech. |
| **Backend** | Python | Core logic and integration. |

---

## ⚙️ How It Works

1.  **Capture:** The user shows a waste item to the camera.
2.  **Identify:** The **CLIP Model** analyzes the image and identifies the object (e.g., "Smartphone", "Banana Peel").
3.  **Classify:** **Llama 3.2** receives the object name and decides the correct bin (Green, Blue, or Red) based on waste management rules.
4.  **Guide:** The system displays the result on screen and **speaks** the instruction (e.g., *"Ye E-Waste hai, ise Red Bin mein dalein"*).

---

## 💻 Installation & Setup

### Prerequisites
1.  **Python 3.8+** installed.
2.  **Ollama** installed and running (`ollama serve`).
3.  **Llama 3.2 Model** pulled (`ollama run llama3.2`).

### Steps

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/SmartBin-AI.git](https://github.com/your-username/SmartBin-AI.git)
    cd SmartBin-AI
    ```

2.  **Install Dependencies**
    ```bash
    pip install streamlit ollama torch transformers pillow gTTS
    ```

3.  **Run the Application**
    Make sure Ollama is running in the background, then execute:
    ```bash
    streamlit run live_waste_ai.py
    ```

---

## 📸 Screenshots

*(Add a screenshot of your project here - showing the interface detecting an item)*

---

## 🔮 Future Improvements
- [ ] Add support for custom object training using YOLO.
- [ ] Gamification system (Points for correct disposal).
- [ ] IoT integration to automatically open smart bin lids.

---

## 🤝 Contribution
Contributions are welcome! Feel free to open an issue or submit a pull request.

---

**Developed by [Your Name]**
