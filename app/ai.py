import streamlit as st

# Lib availability flags
try:
    import torch  # noqa: F401
    torch_available = True
except Exception:
    torch_available = False

try:
    from transformers import BlipProcessor, BlipForConditionalGeneration  # noqa: F401
    transformers_available = True
except Exception:
    transformers_available = False

@st.cache_resource
def load_blip_model():
    if not torch_available or not transformers_available:
        return None, None
    try:
        from transformers import BlipProcessor, BlipForConditionalGeneration
        import torch
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        model = model.to('cpu')
        model.eval()
        return processor, model
    except Exception as e:
        st.error(f"Error loading BLIP model: {str(e)}")
        st.error("This might be due to insufficient memory or missing dependencies.")
        return None, None

def generate_image_caption(image):
    if not torch_available or not transformers_available:
        return "AI model unavailable: PyTorch or Transformers not installed"
    if st.session_state.blip_processor is None or st.session_state.blip_model is None:
        processor, model = load_blip_model()
        if processor is None or model is None:
            return "Error: Could not load BLIP model. Possibly memory constrained."
        st.session_state.blip_processor = processor
        st.session_state.blip_model = model
    try:
        import torch
        if image.mode != 'RGB':
            image = image.convert('RGB')
        inputs = st.session_state.blip_processor(image, return_tensors="pt")
        inputs = {k: v.to('cpu') for k, v in inputs.items() if hasattr(v, 'to')}
        with torch.no_grad():
            output = st.session_state.blip_model.generate(
                **inputs, max_length=50, num_beams=5, do_sample=False, early_stopping=True
            )
        caption = st.session_state.blip_processor.decode(output[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        st.warning("AI model encountered an issue. Possibly memory constrained.")
        return f"Error generating caption: {str(e)}"

def load_ai_models() -> bool:
    if not torch_available or not transformers_available:
        st.error("❌ AI libraries not available" if st.session_state.language == 'english' else "❌ AI లైబ్రరీలు అందుబాటులో లేవు")
        st.error("Please ensure PyTorch and Transformers are installed.")
        return False
    if not st.session_state.ai_model_loaded:
        loading_msg = "🤖 మా AI మోడల్‌ను లోడ్ చేస్తున్నాము..." if st.session_state.language == 'telugu' else "🤖 Loading our magical AI brain..."
        success_msg = "✅ AI మోడల్ విజయవంతంగా లోడ్ అయ్యింది!" if st.session_state.language == 'telugu' else "✅ Model loaded successfully!"
        info_msg = "💡 తదుపరిసారి మరింత వేగంగా లోడ్ అవుతుంది!" if st.session_state.language == 'telugu' else "💡 Will load faster next time!"
        error_msg = "❌ AI మోడల్ లోడ్ కాలేదు." if st.session_state.language == 'telugu' else "❌ Failed to load AI model."
        with st.spinner(loading_msg):
            processor, model = load_blip_model()
            if processor is not None and model is not None:
                st.session_state.blip_processor = processor
                st.session_state.blip_model = model
                st.session_state.ai_model_loaded = True
                st.success(success_msg)
                st.info(info_msg)
                return True
            st.error(error_msg)
            st.error("This might be due to insufficient memory. The app will continue without AI features.")
            return False
    return True