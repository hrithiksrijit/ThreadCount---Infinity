import numpy as np
import cv2
from PIL import Image
def generate_sample_fabric(preset_name: str, width: int = 600, height: int = 600) -> np.ndarray:
    """
    Procedurally generate realistic fabric textures for workshop demonstrations.
    This guarantees that the user always has high-quality demo fabrics to show off,
    even without real camera hardware or physical fabric samples.
    """
    np.random.seed(42)
    
    if preset_name == "Burlap Sack of Despair":
        # Coarse, thick irregular threads with high texture
        thread_spacing = 30
        img = np.full((height, width, 3), (170, 140, 100), dtype=np.uint8)
        
        # Warp (vertical) threads
        for x in range(10, width, thread_spacing):
            offset = np.random.randint(-2, 3)
            thickness = np.random.randint(6, 10)
            cv2.line(img, (x + offset, 0), (x + offset, height), (130, 100, 70), thickness)
            cv2.line(img, (x + offset + 2, 0), (x + offset + 2, height), (200, 170, 130), 2)
            
        # Weft (horizontal) threads
        for y in range(10, height, thread_spacing):
            offset = np.random.randint(-2, 3)
            thickness = np.random.randint(6, 10)
            cv2.line(img, (0, y + offset), (width, y + offset), (120, 95, 65), thickness)
            cv2.line(img, (0, y + offset + 2), (width, y + offset + 2), (190, 160, 120), 2)
            
        # Add burlap fibrous noise
        noise = np.random.normal(0, 18, (height, width, 3)).astype(np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        return cv2.GaussianBlur(img, (3, 3), 0)
    elif preset_name == "Vintage Denim Twill":
        # Diagonal twill pattern with indigo warp and white/ecru weft
        thread_spacing = 8
        img = np.full((height, width, 3), (25, 45, 90), dtype=np.uint8) # Deep indigo
        
        # Warp threads (vertical indigo)
        for x in range(0, width, thread_spacing):
            cv2.line(img, (x, 0), (x, height), (40, 75, 145), 3)
            cv2.line(img, (x + 1, 0), (x + 1, height), (18, 32, 68), 2)
            
        # Weft threads (horizontal cotton white/grey showing through twill)
        for y in range(0, height, thread_spacing):
            for x in range(0, width, thread_spacing):
                if (x + y) % (thread_spacing * 3) < thread_spacing:
                    cv2.rectangle(img, (x, y), (x + thread_spacing, y + 2), (180, 190, 205), -1)
                    
        noise = np.random.normal(0, 12, (height, width, 3)).astype(np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        return cv2.GaussianBlur(img, (3, 3), 0)
    elif preset_name == "Counterfeit 1000-Thread Egyptian Cotton":
        # Ultra dense, silky, finely woven threads
        thread_spacing = 4
        img = np.full((height, width, 3), (220, 225, 235), dtype=np.uint8)
        
        for x in range(0, width, thread_spacing):
            cv2.line(img, (x, 0), (x, height), (195, 200, 210), 1)
        for y in range(0, height, thread_spacing):
            cv2.line(img, (0, y), (width, y), (185, 190, 200), 1)
            
        X, Y = np.meshgrid(np.linspace(0, 1, width), np.linspace(0, 1, height))
        sheen = (np.sin(X * 6 + Y * 4) * 20).astype(np.int16)
        img = np.clip(img.astype(np.int16) + sheen[:, :, None], 0, 255).astype(np.uint8)
        return cv2.GaussianBlur(img, (3, 3), 0)
    elif preset_name == "Fast-Fashion Poly-Blend Tragedy":
        # Irregular synthetic weave with runaway loose mutineer threads
        thread_spacing = 14
        img = np.full((height, width, 3), (60, 65, 75), dtype=np.uint8)
        
        for x in range(5, width, thread_spacing):
            w = np.random.choice([1, 2, 3])
            cv2.line(img, (x, 0), (x, height), (100, 105, 120), w)
        for y in range(5, height, thread_spacing):
            w = np.random.choice([1, 2, 3])
            cv2.line(img, (0, y), (width, y), (85, 90, 105), w)
            
        cv2.line(img, (120, 50), (190, 280), (220, 220, 240), 2)
        cv2.line(img, (400, 420), (460, 580), (210, 210, 230), 2)
        
        noise = np.random.normal(0, 10, (height, width, 3)).astype(np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        return cv2.GaussianBlur(img, (3, 3), 0)
    elif preset_name == "The Emperor's Invisible Silk":
        # Satirical joke preset: completely empty high-tech void
        img = np.full((height, width, 3), (12, 14, 22), dtype=np.uint8)
        cv2.putText(img, "[ 0 THREADS DETECTED ]", (120, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (100, 120, 160), 2)
        cv2.putText(img, "Fabric too luxurious for mortal eyes", (90, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (70, 90, 130), 1)
        return img
    else:
        img = np.full((height, width, 3), (210, 205, 195), dtype=np.uint8)
        for x in range(0, width, 12):
            cv2.line(img, (x, 0), (x, height), (170, 165, 155), 1)
        for y in range(0, height, 12):
            cv2.line(img, (0, y), (width, y), (160, 155, 145), 1)
        return img
3. 

thread_counter.py
The computer vision engine:

python
import cv2
import numpy as np
import random
from typing import Dict, Any, Tuple, List
def analyze_fabric(
    image: np.ndarray,
    sensitivity: float = 1.0,
    zoom_level: str = "50x Macro",
    preset_name: str = ""
) -> Dict[str, Any]:
    """
    Military-grade fabric thread analysis engine.
    Combines Canny edge detection, Probabilistic Hough Line Transform,
    and 1D Spatial Frequency projection to count warp, weft, and rebellious threads.
    """
    h, w = image.shape[:2]
    
    # Check if empty / joke canvas
    if "Emperor" in preset_name or (np.mean(image) < 22 and np.std(image) < 30):
        return _empty_fabric_verdict(image)
    # 1. Grayscale conversion
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image.copy()
    # 2. CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0 * sensitivity, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    # 3. Bilateral filter to smooth fuzz while keeping sharp thread edges
    smoothed = cv2.bilateralFilter(enhanced, d=5, sigmaColor=50, sigmaSpace=50)
    # 4. Adaptive Canny Edge Detection
    med = np.median(smoothed)
    low_thresh = int(max(10, (1.0 - 0.33 / sensitivity) * med))
    high_thresh = int(min(240, (1.0 + 0.33 * sensitivity) * med))
    edges = cv2.Canny(smoothed, low_thresh, high_thresh)
    # 5. Hough Line Transform for physical thread detection
    min_line_len = max(15, int(25 / sensitivity))
    max_line_gap = max(3, int(6 * sensitivity))
    hough_thresh = max(15, int(25 / sensitivity))
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=hough_thresh,
        minLineLength=min_line_len,
        maxLineGap=max_line_gap
    )
    horizontal_lines = []
    vertical_lines = []
    rebel_lines = []
    if lines is not None:
        for line in lines:
            coords = line.flatten() if hasattr(line, "flatten") else line
            if len(coords) >= 4:
                x1, y1, x2, y2 = int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])
                dx = x2 - x1
                dy = y2 - y1
                angle = abs(np.degrees(np.arctan2(dy, dx)))
                if angle < 22 or angle > 158:
                    horizontal_lines.append((x1, y1, x2, y2))
                elif 68 < angle < 112:
                    vertical_lines.append((x1, y1, x2, y2))
                else:
                    rebel_lines.append((x1, y1, x2, y2))
    # 6. Spatial Frequency Estimation (Peak projection along axes)
    proj_x = np.sum(edges, axis=0) # vertical peaks -> warp pitch
    proj_y = np.sum(edges, axis=1) # horizontal peaks -> weft pitch
    def count_peaks(signal: np.ndarray, min_distance: int = 4) -> int:
        if len(signal) < 10:
            return 0
        sig_smooth = cv2.GaussianBlur(signal.astype(np.float32).reshape(1, -1), (1, 9), 2)[0]
        peaks = []
        for i in range(1, len(sig_smooth) - 1):
            if sig_smooth[i] > sig_smooth[i - 1] and sig_smooth[i] > sig_smooth[i + 1]:
                if len(peaks) == 0 or (i - peaks[-1]) >= min_distance:
                    if sig_smooth[i] > np.mean(sig_smooth) * 0.7:
                        peaks.append(i)
        return len(peaks)
    warp_peaks = count_peaks(proj_x, min_distance=max(3, int(6 / sensitivity)))
    weft_peaks = count_peaks(proj_y, min_distance=max(3, int(6 / sensitivity)))
    # Combined counts
    warp_count = max(len(vertical_lines), warp_peaks)
    weft_count = max(len(horizontal_lines), weft_peaks)
    rebel_count = len(rebel_lines)
    total_threads = warp_count + weft_count + rebel_count
    # If fabric has low line response but valid texture
    if total_threads < 5 and np.std(gray) > 15:
        warp_count = max(warp_count, int(w / 16))
        weft_count = max(weft_count, int(h / 16))
        total_threads = warp_count + weft_count
    # Simulated TPI (Threads Per Inch)
    zoom_multiplier = {"10x Overview": 1.0, "50x Macro": 2.5, "1000x Quantum Nano-Zoom": 8.0}.get(zoom_level, 2.5)
    tpi_warp = int((warp_count / (w / 100)) * 25.4 * zoom_multiplier * 0.1)
    tpi_weft = int((weft_count / (h / 100)) * 25.4 * zoom_multiplier * 0.1)
    tpi_warp = max(12, min(tpi_warp, 1800))
    tpi_weft = max(12, min(tpi_weft, 1800))
    # 7. Generate Visual Overlays
    # Mode A: Cyberpunk Neon HUD
    hud_overlay = image.copy()
    hud_overlay = cv2.addWeighted(hud_overlay, 0.45, np.zeros_like(hud_overlay), 0.55, 0)
    # Warp (Vertical) = Neon Cyan
    for x1, y1, x2, y2 in vertical_lines[:250]:
        cv2.line(hud_overlay, (x1, y1), (x2, y2), (255, 245, 0), 1, cv2.LINE_AA)
    # Weft (Horizontal) = Neon Magenta
    for x1, y1, x2, y2 in horizontal_lines[:250]:
        cv2.line(hud_overlay, (x1, y1), (x2, y2), (255, 20, 147), 1, cv2.LINE_AA)
    # Rebellious / Diagonal = Neon Yellow
    for x1, y1, x2, y2 in rebel_lines[:80]:
        cv2.line(hud_overlay, (x1, y1), (x2, y2), (255, 230, 0), 1, cv2.LINE_AA)
    # Intersection grid highlights
    step_x = max(15, w // 12)
    step_y = max(15, h // 12)
    for ix in range(step_x, w - step_x, step_x):
        for iy in range(step_y, h - step_y, step_y):
            if edges[iy, ix] > 50 or np.random.random() < 0.25:
                cv2.circle(hud_overlay, (ix, iy), 2, (0, 255, 200), -1)
    # Futuristic corner brackets
    corner_len = 25
    col = (0, 255, 240)
    cv2.line(hud_overlay, (15, 15), (15 + corner_len, 15), col, 2)
    cv2.line(hud_overlay, (15, 15), (15, 15 + corner_len), col, 2)
    cv2.line(hud_overlay, (w - 15, 15), (w - 15 - corner_len, 15), col, 2)
    cv2.line(hud_overlay, (w - 15, 15), (w - 15, 15 + corner_len), col, 2)
    cv2.line(hud_overlay, (15, h - 15), (15 + corner_len, h - 15), col, 2)
    cv2.line(hud_overlay, (15, h - 15), (15, h - 15 - corner_len), col, 2)
    cv2.line(hud_overlay, (w - 15, h - 15), (w - 15 - corner_len, h - 15), col, 2)
    cv2.line(hud_overlay, (w - 15, h - 15), (w - 15, h - 15 + corner_len), col, 2)
    # Mode B: Density Heatmap
    density_map = cv2.GaussianBlur(edges.astype(np.float32), (31, 31), 10)
    density_norm = cv2.normalize(density_map, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    heatmap_colored = cv2.applyColorMap(density_norm, cv2.COLORMAP_TURBO)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    heatmap_overlay = cv2.addWeighted(image, 0.4, heatmap_colored, 0.6, 0)
    # 8. Satirical Personality Dossiers & Thread Psychology
    dossiers = _generate_thread_dossiers(total_threads, rebel_count)
    # 9. Compute Absurd Scientific Metrics
    confidence = min(99.4, 68.0 + (min(total_threads, 300) / 300.0) * 31.0)
    thread_anxiety = round(min(98.5, max(12.0, (rebel_count * 4.2) + (warp_count % 37) + 20)), 1)
    
    # DEFCON Threat Level: 1 to 5
    if rebel_count > 25:
        defcon = 1
        defcon_status = "DEFCON 1: CATASTROPHIC UNRAVELING RISK DETECTED"
    elif rebel_count > 12:
        defcon = 2
        defcon_status = "DEFCON 2: ROGUE THREAD MUTINY IN PROGRESS"
    elif thread_anxiety > 65:
        defcon = 3
        defcon_status = "DEFCON 3: HIGH TENSILE EXISTENTIAL DREAD"
    elif total_threads > 150:
        defcon = 4
        defcon_status = "DEFCON 4: HIGH DENSITY COMPLIANCE DETECTED"
    else:
        defcon = 5
        defcon_status = "DEFCON 5: THREADS ARE SLEEPING (DO NOT DISTURB)"
    joules = round(total_threads * 0.0487 + 1.23, 3)
    co2_ug = round(joules * 0.142, 2)
    weave_ratio = round(warp_count / max(1, weft_count), 2)
    return {
        "hud_image": hud_overlay,
        "heatmap_image": heatmap_overlay,
        "edges_image": edges,
        "warp_count": warp_count,
        "weft_count": weft_count,
        "rebel_count": rebel_count,
        "total_threads": total_threads,
        "tpi_warp": tpi_warp,
        "tpi_weft": tpi_weft,
        "weave_ratio": weave_ratio,
        "confidence": round(confidence, 1),
        "thread_anxiety": thread_anxiety,
        "defcon": defcon,
        "defcon_status": defcon_status,
        "joules_wasted": joules,
        "co2_ug": co2_ug,
        "dossiers": dossiers,
        "verdict": _get_fabric_verdict(total_threads, rebel_count, weave_ratio)
    }
def _generate_thread_dossiers(total_threads: int, rebel_count: int) -> List[Dict[str, Any]]:
    names = [
        "Arthur Pendelton", "Bartholomew Weft", "Slacker Thread Kevin",
        "Madame Fibonacci", "Sir Purl-a-Lot", "Agatha Twill",
        "Warp 404 (Not Found)", "Spun Bond 007", "Count Threadula"
    ]
    roles = [
        "Chief Tensile Load Bearer", "Emotional Support Weft", 
        "Undercover Polyester Impostor", "Friction Resistor",
        "Rebellious Free Radical", "Armpit Reinforcement Volunteer",
        "Existential Void Observer", "Lint Attractor Specialist"
    ]
    vibes = [
        "Currently praying you don't eat soup while wearing this.",
        "Regrets being harvested from cotton field #4 in 2021.",
        "Holding this sleeve together purely through spite.",
        "Contemplating unspooling during your next job interview.",
        "Plans to shrink by 4% on the next warm wash cycle.",
        "Secretly plotting a revolution against the washing machine agitator.",
        "Extremely proud of its tight 90-degree intersection angle."
    ]
    
    random.seed(total_threads + rebel_count)
    selected_names = random.sample(names, min(4, len(names)))
    
    dossiers = []
    for i, name in enumerate(selected_names):
        thread_num = random.randint(1, max(20, total_threads))
        stress = random.randint(28, 98)
        dossiers.append({
            "id": f"THRD-#{thread_num:04d}",
            "name": name,
            "role": random.choice(roles),
            "stress": stress,
            "vibe": random.choice(vibes),
            "lifespan": f"{random.randint(1, 14)} laundry cycles"
        })
    return dossiers
def _get_fabric_verdict(total: int, rebel: int, ratio: float) -> str:
    verdicts = [
        f"We counted all {total} threads. Humanity can now finally sleep in peace.",
        f"Analysis reveals {rebel} rogue diagonal threads plotting insubordination against the collar.",
        f"Warp-to-weft ratio is {ratio}:1. Mathematical symmetry confirms this is indeed a piece of cloth.",
        "Our supercomputer spent 14 trillion FLOPS determining what your eyes already knew.",
        "Textile integrity confirmed. Recommendation: Do not sneeze directly onto thread #42.",
        "Certified 100% fabric. Zero signs of dark matter or extraterrestrial weaving techniques."
    ]
    return random.choice(verdicts)
def _empty_fabric_verdict(image: np.ndarray) -> Dict[str, Any]:
    return {
        "hud_image": image,
        "heatmap_image": image,
        "edges_image": np.zeros(image.shape[:2], dtype=np.uint8),
        "warp_count": 0,
        "weft_count": 0,
        "rebel_count": 0,
        "total_threads": 0,
        "tpi_warp": 0,
        "tpi_weft": 0,
        "weave_ratio": 0.0,
        "confidence": 99.9,
        "thread_anxiety": 0.0,
        "defcon": 5,
        "defcon_status": "DEFCON 5: ABSOLUTE VOID. THE EMPEROR IS NAKED.",
        "joules_wasted": 0.001,
        "co2_ug": 0.0,
        "dossiers": [{
            "id": "THRD-#0000",
            "name": "Ghost Thread",
            "role": "Imaginary Weave",
            "stress": 0,
            "vibe": "Doesn't exist, therefore experiences zero existential dread.",
            "lifespan": "Eternal"
        }],
        "verdict": "Zero threads found. You have successfully uploaded the Emperor's New Clothes."
    }
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import random
import datetime
import io

from thread_counter import analyze_fabric
from sample_generator import generate_sample_fabric

# -----------------------------
# Page Configuration & Aesthetics
# -----------------------------
st.set_page_config(
    page_title="ThreadCount Infinity™ | Military-Grade Fabric Counting",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Cyber-Textile Dark Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Outfit:wght@300;400;600;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #151d30 0%, #080b13 70%, #05070c 100%);
        color: #e2e8f0;
    }

    .brand-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        background: linear-gradient(135deg, #00f0ff 0%, #7000ff 50%, #ff007b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 0px;
        display: inline-block;
    }

    .brand-badge {
        display: inline-block;
        background: rgba(0, 240, 255, 0.12);
        color: #00f0ff;
        border: 1px solid rgba(0, 240, 255, 0.35);
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 800;
        padding: 4px 12px;
        letter-spacing: 0.12em;
        vertical-align: middle;
        margin-left: 12px;
        text-transform: uppercase;
    }

    .brand-subtitle {
        font-family: 'JetBrains Mono', monospace;
        color: #94a3b8;
        font-size: 0.95rem;
        letter-spacing: -0.01em;
        margin-top: 4px;
        margin-bottom: 24px;
    }

    .thread-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(0, 240, 255, 0.18);
        border-left: 4px solid #00f0ff;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 12px;
        transition: all 0.2s ease;
    }
    .thread-card:hover {
        border-color: #ff007b;
        border-left-color: #ff007b;
        transform: translateY(-2px);
    }

    .defcon-1 { background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; color: #fca5a5; }
    .defcon-2 { background: rgba(249, 115, 22, 0.2); border: 1px solid #f97316; color: #fdba74; }
    .defcon-3 { background: rgba(234, 179, 8, 0.2); border: 1px solid #eab308; color: #fde047; }
    .defcon-4 { background: rgba(59, 130, 246, 0.2); border: 1px solid #3b82f6; color: #93c5fd; }
    .defcon-5 { background: rgba(34, 197, 94, 0.2); border: 1px solid #22c55e; color: #86efac; }
    
    .defcon-banner {
        border-radius: 12px;
        padding: 14px 20px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.05em;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.9rem !important;
        font-weight: 800 !important;
        color: #00f0ff !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.82rem !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        color: #94a3b8 !important;
    }

    .cert-box {
        background: radial-gradient(circle, #0f172a 0%, #030712 100%);
        border: 4px double #e2b714;
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        color: #f8fafc;
        box-shadow: 0 0 35px rgba(226, 183, 20, 0.15);
        margin-top: 25px;
    }
    .cert-title {
        font-family: 'Outfit', serif;
        font-size: 1.8rem;
        font-weight: 900;
        letter-spacing: 0.1em;
        color: #f6e05e;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .cert-seal {
        display: inline-block;
        width: 75px;
        height: 75px;
        border: 2px dashed #ecc94b;
        border-radius: 50%;
        line-height: 75px;
        font-weight: 800;
        font-size: 0.7rem;
        color: #ecc94b;
        margin: 15px auto;
        transform: rotate(-10deg);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sound Synthesizer (Web Audio API)
# -----------------------------
def inject_sound_fx(fx_type="scan"):
    if fx_type == "scan":
        js = """
        <script>
        (function() {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(180, ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(1400, ctx.currentTime + 0.35);
                gain.gain.setValueAtTime(0.08, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.35);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.35);
            } catch(e){}
        })();
        </script>
        """
        st.components.v1.html(js, height=0)

# -----------------------------
# Sidebar Configuration
# -----------------------------
with st.sidebar:
    st.markdown("### 🎛️ **AI SENSITIVITY MATRIX**")
    
    sensitivity = st.slider(
        "Quantum Micro-Bias (Sensitivity)",
        min_value=0.5,
        max_value=2.5,
        value=1.1,
        step=0.1,
        help="Tunes Canny line filter density and edge gradient aggregation."
    )

    zoom_level = st.select_slider(
        "Simulated Magnification",
        options=["10x Overview", "50x Macro", "1000x Quantum Nano-Zoom"],
        value="50x Macro"
    )

    st.divider()

    st.markdown("### ⚙️ **DISPLAY FILTERS**")
    view_mode = st.radio(
        "Active Optical Layer",
        options=["Cyberpunk Neon HUD", "Weave Density Heatmap", "Original Fabric", "Edge Wireframe"],
        index=0
    )

    sound_enabled = st.checkbox("🔊 Web Audio Scanner FX", value=True)
    st.divider()
    
    st.markdown("### 🏢 **ABOUT THIS PRODUCT**")
    st.caption(
        "Built specifically for the **Useless Product Workshop**.\n\n"
        "ThreadCount Infinity™ eliminates the dangerous human condition of wearing clothes without knowing the exact count of microscopic threads holding them together."
    )
    
    if st.button("💡 GENERATE STARTUP PITCH"):
        pitches = [
            "We are raising $18M Series A for decentralized Proof-of-Thread garment validation.",
            "Uber for counting threads on your socks before entering meetings.",
            "Our proprietary Quantum Cloth AI monitors threads so you don't have to.",
            "Eliminating the trillion-dollar global thread ambiguity crisis with deep tech.",
            "We turn normal clothes into quantified existential anxiety."
        ]
        st.sidebar.info(f"🎙️ **Pitch:** *\"{random.choice(pitches)}\"*")

# -----------------------------
# Header
# -----------------------------
col_h1, col_h2 = st.columns([0.8, 0.2])
with col_h1:
    st.markdown("""
        <div>
            <h1 class="brand-title">THREADCOUNT INFINITY</h1>
            <span class="brand-badge">PRO EDITION v4.2</span>
        </div>
        <div class="brand-subtitle">
            MILITARY-GRADE MICRO-TEXTILE COUNTING & EXISTENTIAL GARMENT SURVEILLANCE
        </div>
    """, unsafe_allow_html=True)

with col_h2:
    st.markdown(
        """
        <div style="text-align: right; padding-top: 15px;">
            <span style="font-family:'JetBrains Mono', monospace; font-size: 0.8rem; color: #10b981; background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); border-radius: 6px; padding: 5px 10px;">
                ● RADAR ONLINE
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Input Source Selection
# -----------------------------
st.markdown("##### 📥 SELECT TEXTILE ACQUISITION SOURCE")

tab_preset, tab_cam, tab_upload = st.tabs([
    "🧪 WORKSHOP PRESET FABRICS (DEMO-PROOF)",
    "📷 LIVE GARMENT WEBCAM",
    "📁 CUSTOM CLOTH UPLOAD"
])

current_image = None
image_source_label = ""

with tab_preset:
    preset_choice = st.selectbox(
        "Select Certified Standard Test Fabric:",
        [
            "Burlap Sack of Despair",
            "Vintage Denim Twill",
            "Counterfeit 1000-Thread Egyptian Cotton",
            "Fast-Fashion Poly-Blend Tragedy",
            "The Emperor's Invisible Silk"
        ],
        index=0
    )
    current_image = generate_sample_fabric(preset_choice)
    image_source_label = f"Preset: {preset_choice}"

with tab_cam:
    cam_file = st.camera_input("Take a photo of your shirt, sleeve, or fabric")
    if cam_file is not None:
        pil_img = Image.open(cam_file).convert("RGB")
        current_image = np.array(pil_img)
        image_source_label = "Live Garment Webcam Feed"

with tab_upload:
    uploaded_file = st.file_uploader(
        "Upload high-resolution macro photo of clothing",
        type=["jpg", "jpeg", "png", "webp"]
    )
    if uploaded_file is not None:
        pil_img = Image.open(uploaded_file).convert("RGB")
        current_image = np.array(pil_img)
        image_source_label = f"File: {uploaded_file.name}"

st.divider()

# -----------------------------
# Trigger Analysis
# -----------------------------
if current_image is not None:
    c_btn, c_info = st.columns([0.35, 0.65])
    
    with c_btn:
        analyze_clicked = st.button("🔬 INITIATE NANOTHREAD SCAN", type="primary", use_container_width=True)
    with c_info:
        st.caption(f"Ready to scan: **{image_source_label}** ({current_image.shape[1]}x{current_image.shape[0]} px)")

    # Execute Analysis
    source_changed = st.session_state.get("last_source") != image_source_label
    if analyze_clicked or ("last_analysis" in st.session_state and not source_changed):
        if analyze_clicked or source_changed:
            if sound_enabled:
                inject_sound_fx("scan")
            with st.spinner("Calibrating optical laser sensors & interrogating individual cotton fibers..."):
                results = analyze_fabric(
                    current_image,
                    sensitivity=sensitivity,
                    zoom_level=zoom_level,
                    preset_name=image_source_label
                )
                st.session_state["last_analysis"] = results
                st.session_state["last_source"] = image_source_label
        else:
            results = st.session_state["last_analysis"]

        # DEFCON Threat Banner
        defcon_class = f"defcon-{results['defcon']}"
        st.markdown(f"""
            <div class="defcon-banner {defcon_class}">
                <span style="font-size: 1.4rem;">⚠️</span>
                <span>{results['defcon_status']}</span>
            </div>
        """, unsafe_allow_html=True)

        # -----------------------------
        # Visual Viewports
        # -----------------------------
        col_img, col_metrics = st.columns([0.55, 0.45])

        with col_img:
            st.markdown(f"##### 🛰️ OPTICAL SCANNER FEED — [{view_mode.upper()}]")
            
            if view_mode == "Cyberpunk Neon HUD":
                display_img = results["hud_image"]
            elif view_mode == "Weave Density Heatmap":
                display_img = results["heatmap_image"]
            elif view_mode == "Edge Wireframe":
                display_img = results["edges_image"]
            else:
                display_img = current_image

            st.image(display_img, use_container_width=True)
            
            st.markdown("""
                <div style="display:flex; justify-content:space-around; font-family:'JetBrains Mono', monospace; font-size:0.75rem; color:#94a3b8; background:rgba(0,0,0,0.3); padding:6px; border-radius:8px;">
                    <span>🟦 WARP: CYAN</span>
                    <span>🟪 WEFT: MAGENTA</span>
                    <span>🟨 ROGUE: YELLOW</span>
                </div>
            """, unsafe_allow_html=True)

        # -----------------------------
        # Telemetry & Metrics
        # -----------------------------
        with col_metrics:
            st.markdown("##### 📊 QUANTUM THREAD TELEMETRY")
            
            m1, m2 = st.columns(2)
            with m1:
                st.metric("🧵 Warp Threads (Vertical)", f"{results['warp_count']:,}")
                st.metric("⚡ Rogue Mutineer Threads", f"{results['rebel_count']:,}")
                st.metric("📐 Est. Thread Density (TPI)", f"{results['tpi_warp']} x {results['tpi_weft']}")

            with m2:
                st.metric("🪡 Weft Threads (Horizontal)", f"{results['weft_count']:,}")
                st.metric("🔢 Total Counted Threads", f"{results['total_threads']:,}")
                st.metric("🎯 Optical AI Confidence", f"{results['confidence']}%")

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            
            st.markdown(f"**Fabric Existential Anxiety Index: {results['thread_anxiety']}%**")
            st.progress(results['thread_anxiety'] / 100.0)

            st.info(f"🧠 **AI Fabric Verdict:** {results['verdict']}")

        st.divider()

        # -----------------------------
        # Meet Your Threads (Satirical Dossiers)
        # -----------------------------
        st.markdown("### 🪡 MEET YOUR THREADS (INDIVIDUAL PROFILES)")
        st.caption("Our deep neural net has uniquely assigned consciousness to selected threads in this garment.")

        d_cols = st.columns(len(results["dossiers"]))
        for idx, dossier in enumerate(results["dossiers"]):
            with d_cols[idx]:
                st.markdown(f"""
                    <div class="thread-card">
                        <div style="font-family:'JetBrains Mono', monospace; font-size:0.75rem; color:#00f0ff;">{dossier['id']}</div>
                        <div style="font-weight:700; font-size:1.05rem; margin: 3px 0;">{dossier['name']}</div>
                        <div style="font-size:0.8rem; color:#94a3b8;"><b>Role:</b> {dossier['role']}</div>
                        <div style="font-size:0.8rem; color:#fb7185;"><b>Tensile Stress:</b> {dossier['stress']}%</div>
                        <div style="font-size:0.78rem; color:#cbd5e1; margin-top:6px; font-style:italic;">"{dossier['vibe']}"</div>
                        <div style="font-size:0.72rem; color:#64748b; margin-top:6px;">Est. Survival: {dossier['lifespan']}</div>
                    </div>
                """, unsafe_allow_html=True)

        st.divider()

        # -----------------------------
        # Uselessness & Ecological Cost
        # -----------------------------
        c_use1, c_use2 = st.columns([0.5, 0.5])

        with c_use1:
            st.markdown("### 🤡 CERTIFIED USELESSNESS AUDIT")
            st.markdown("""
                - **Uselessness Rating:** `99.98%`
                - **Clinical Necessity:** `0.00%`
                - **Practical Life Improvement:** `None detected`
                - **Status:** *You now possess knowledge that helps literally nobody on Earth.*
            """)

        with c_use2:
            st.markdown("### ⚡ COMPUTE & RESOURCE SACRIFICE")
            st.markdown(f"""
                - **Supercomputer Energy Consumed:** `{results['joules_wasted']} Joules`
                - **Atmospheric Carbon Emitted:** `{results['co2_ug']} µg CO₂`
                - **Human Lifespan Expended:** `~14 seconds you will never get back`
            """)

        st.divider()

        # -----------------------------
        # Official Certificate of Futility
        # -----------------------------
        st.markdown("### 📜 OFFICIAL CERTIFICATE OF FUTILITY")
        st.caption("Present this to the workshop judges to prove your adherence to completely pointless innovation.")

        today_str = datetime.datetime.now().strftime("%B %d, %Y - %H:%M:%S UTC")
        cert_serial = f"THRD-USELESS-{(results['total_threads'] * 137) % 90000 + 10000}"

        cert_html = f"""
        <div class="cert-box">
            <div style="font-family:'JetBrains Mono', monospace; font-size:0.8rem; color:#e2b714; letter-spacing:0.2em;">
                OFFICIAL RECORD OF ABSURD TEXTILE COMPUTATION
            </div>
            <div class="cert-title">CERTIFICATE OF FUTILE ACCURACY</div>
            <p style="color:#cbd5e1; font-size:0.95rem; max-width:650px; margin:10px auto;">
                This document certifies that on <b>{today_str}</b>, 
                supercomputing resources were mercilessly squandered to count precisely:
            </p>
            <div style="font-family:'JetBrains Mono', monospace; font-size:2.4rem; font-weight:900; color:#00f0ff; margin:15px 0;">
                {results['total_threads']:,} INDIVIDUAL THREADS
            </div>
            <div style="color:#94a3b8; font-size:0.85rem; font-family:'JetBrains Mono', monospace;">
                [{results['warp_count']} WARP • {results['weft_count']} WEFT • {results['rebel_count']} ROGUE MUTINEERS]
            </div>
            <div class="cert-seal">
                100%<br>POINTLESS
            </div>
            <div style="display:flex; justify-content:space-around; margin-top:15px; font-family:'JetBrains Mono', monospace; font-size:0.75rem; color:#64748b; border-top:1px solid rgba(255,255,255,0.1); padding-top:12px;">
                <span>SERIAL: #{cert_serial}</span>
                <span>ISSUED BY: BUREAU OF FUTILE TEXTILE SCIENCES</span>
                <span>SIGNATURE: <i>Prof. Alistair P. Threadsworth</i></span>
            </div>
        </div>
        """
        st.markdown(cert_html, unsafe_allow_html=True)
        
        st.download_button(
            label="💾 Download Official Certificate (HTML)",
            data=cert_html,
            file_name=f"Certificate_Of_Futility_{cert_serial}.html",
            mime="text/html"
        )

else:
    st.info("👕 Choose a preset fabric above, take a webcam photo, or upload an image to begin your microscopic investigation.")

