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

# --- LOAD CLIP MODEL ---
@st.cache_resource
def load_clip_model():
    st.toast("🧠 Loading CLIP Model... (thoda heavy hai)")
    # Ye model text aur image dono samajhta hai
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return model, processor

try:
    model, processor = load_clip_model()
    st.success("✅ AI Ready!")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# --- CUSTOM LABELS (Aap jo chaho wo list bana lo) ---
# CLIP sirf inme se choose karega, isliye 'Projector' galti se nahi bolega
POSSIBLE_ITEMS = [
    "Smartphone or Mobile Phone",
    "Plastic Water Bottle",
    "Banana Peel or Fruit",
    "Chips Packet or Plastic Wrapper",
    "Paper Ball or Newspaper",
    "Laptop or Computer",
    "Earphones or Headphones",
    "Glass Bottle",
    "Metal Can"
]

def identify_with_clip(image):
    # 1. Image aur Text dono ko process karo
    inputs = processor(
        text=POSSIBLE_ITEMS, 
        images=image, 
        return_tensors="pt", 
        padding=True
    )
    
    # 2. Prediction
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image # Image-text similarity score
    probs = logits_per_image.softmax(dim=1) # Probability me convert karo
    
    # 3. Best Match dhundo
    best_match_idx = probs.argmax()
    best_label = POSSIBLE_ITEMS[best_match_idx]
    confidence = probs[0][best_match_idx].item() * 100
    
    return best_label, confidence

def ask_llama(item_name):
    prompt = (
        f"Identify waste: '{item_name}'. "
        "Strictly classify into: "
        "1. Green Bin (Organic), "
        "2. Blue Bin (Recyclable), "
        "3. Red Bin (E-Waste). "
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
    st.image(img, caption="Captured", width=200)
    
    with st.spinner("CLIP Brain soch raha hai..."):
        # Vision (CLIP)
        item, conf = identify_with_clip(img)
        
        st.subheader(f"🔍 Found: {item}")
        st.caption(f"Confidence: {conf:.1f}%")
        
        # Logic (Llama)
        advice = ask_llama(item)
        
        if "Green" in advice: st.success(advice)
        elif "Red" in advice: st.error(advice)
        else: st.info(advice)
        
        speak(advice)