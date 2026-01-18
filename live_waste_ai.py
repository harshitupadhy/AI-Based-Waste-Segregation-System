import streamlit as st
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import ollama
from gtts import gTTS
import base64

# --- CONFIG ---
st.set_page_config(page_title="Smart Bin AI (CLIP)", page_icon="♻️")
st.title("♻️ Smart Bin AI (Genius Mode)")

# Loading Message Outside Function
status = st.empty()
status.warning("🧠 Loading CLIP Brain... (Pehli baar thoda time lagega)")

# --- LOAD CLIP MODEL ---
# Fix: Is function ke andar koi st.write/st.toast nahi hona chahiye
@st.cache_resource
def load_clip_model():
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return model, processor

try:
    model, processor = load_clip_model()
    status.success("✅ AI Ready! Camera use karein.")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# --- CUSTOM LABELS (Aap jo chaho wo list bana lo) ---
# AI inme se hi choose karega -> Projector galti se nahi bolega
POSSIBLE_ITEMS = [
    "Smartphone",
    "Headphones or Earphones",
    "Plastic Water Bottle",
    "Banana Peel",
    "Lays Chips Packet",
    "Paper Waste",
    "Laptop",
    "Glass Bottle",
    "Metal Can",
    "Pen or Pencil"
]

def identify_with_clip(image):
    # 1. Process
    inputs = processor(
        text=POSSIBLE_ITEMS, 
        images=image, 
        return_tensors="pt", 
        padding=True
    )
    
    # 2. Prediction
    outputs = model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1) 
    
    # 3. Best Match
    best_match_idx = probs.argmax()
    best_label = POSSIBLE_ITEMS[best_match_idx]
    confidence = probs[0][best_match_idx].item() * 100
    
    return best_label, confidence

def ask_llama(item_name):
    prompt = (
        f"Identify waste: '{item_name}'. "
        "Strictly classify into one bin:\n"
        "1. Green Bin (Organic)\n"
        "2. Blue Bin (Recyclable - Plastic/Metal/Glass)\n"
        "3. Red Bin (E-Waste - Phone/Earphones/Wires)\n"
        "Reply in Hinglish. Keep it extremely short."
    )
    try:
        res = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
        return res['message']['content']
    except:
        return "Thinking..."

def speak(text):
    try:
        tts = gTTS(text=text, lang='en', tld='co.in')
        tts.save("temp.mp3")
        with open("temp.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""<audio controls autoplay><source src="data:audio/mp3;base64,{b64}"></audio>"""
            st.markdown(md, unsafe_allow_html=True)
    except: pass

# --- UI ---
st.info("📷 Photo lijiye (Mobile, Bottle, Food, etc.)")
camera_img = st.camera_input("Scan Waste")

if camera_img:
    img = Image.open(camera_img)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(img, caption="Captured", width=200)
    
    with col2:
        with st.spinner("CLIP Brain soch raha hai..."):
            # Vision (CLIP)
            item, conf = identify_with_clip(img)
            
            st.subheader(f"🔍 Found: {item}")
            st.caption(f"Confidence: {conf:.1f}%")
            
            # Logic (Llama)
            advice = ask_llama(item)
            
            if "Green" in advice: st.success(f"✅ {advice}")
            elif "Red" in advice or "E-Waste" in advice: st.error(f"🔴 {advice}")
            else: st.info(f"♻️ {advice}")
            
            speak(advice)