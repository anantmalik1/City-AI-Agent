import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="City AI Agent",
    page_icon="🌨️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Fetch weather helper ──────────────────────────────────────────────────────
def fetch_weather(city: str):
    api_key = os.getenv("OPENWEATHER_API_KEY", "")
    if not api_key:
        return None
    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city},IN&appid={api_key}&units=metric"
    )
    try:
        data = requests.get(url, timeout=5).json()
        if str(data.get("cod")) == "200":
            return {
                "temp": data["main"]["temp"],
                "feels": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "desc": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"],
            }
    except Exception:
        pass
    return None


# ── Demo cities ───────────────────────────────────────────────────────────────
CITIES = ["Delhi", "Mumbai", "Bengaluru", "Kolkata", "Chennai", "Hyderabad", "Dehradun", "Jaipur"]

# ── Inject all custom CSS / JS ────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ═══════════════════════════════════════════════════════
       IMPORTS
    ═══════════════════════════════════════════════════════ */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;900&family=Rajdhani:wght@300;400;600&display=swap');
    /* ═══════════════════════════════════════════════════════
       ROOT VARIABLES
    ═══════════════════════════════════════════════════════ */
    :root {
        --ice:   #a8d8f0;
        --frost: #d4eeff;
        --deep:  #0a1628;
        --mid:   #0d2044;
        --glow:  #00c6ff;
        --accent:#ff6b35;
    }
    /* ═══════════════════════════════════════════════════════
       GLOBAL RESET
    ═══════════════════════════════════════════════════════ */
    html, body, [data-testid="stAppViewContainer"],
    [data-testid="stApp"], .main {
        background: transparent !important;
    }
    /* ═══════════════════════════════════════════════════════
       SNOW CANVAS BACKGROUND
    ═══════════════════════════════════════════════════════ */
    #snow-canvas {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        z-index: 0;
        pointer-events: none;
    }
    /* ═══════════════════════════════════════════════════════
       DEEP SKY GRADIENT BEHIND EVERYTHING
    ═══════════════════════════════════════════════════════ */
    body::before {
        content: '';
        position: fixed;
        inset: 0;
        background:
            radial-gradient(ellipse at 20% 10%, #1a3a6e 0%, transparent 55%),
            radial-gradient(ellipse at 80% 80%, #0a2240 0%, transparent 55%),
            linear-gradient(160deg, #050e1f 0%, #0a1a35 40%, #060d1a 100%);
        z-index: -1;
    }
    /* ═══════════════════════════════════════════════════════
       STREAMLIT STRUCTURAL OVERRIDES
    ═══════════════════════════════════════════════════════ */
    [data-testid="stAppViewContainer"] { z-index: 1; }
    [data-testid="stSidebar"]          { z-index: 10 !important; }
    section.main                       { z-index: 1; }
    .block-container {
        padding: 2rem 2rem 4rem !important;
        max-width: 900px !important;
    }
    /* ═══════════════════════════════════════════════════════
       SIDEBAR — Frosted glass panel
    ═══════════════════════════════════════════════════════ */
    [data-testid="stSidebar"] > div:first-child {
        background: rgba(8, 20, 45, 0.78) !important;
        backdrop-filter: blur(22px) saturate(160%) !important;
        border-right: 1px solid rgba(0,198,255,0.18) !important;
        box-shadow: 4px 0 40px rgba(0,198,255,0.08) !important;
    }
    [data-testid="stSidebar"] * { color: var(--frost) !important; }
    /* Sidebar animated left accent line */
    [data-testid="stSidebar"] > div:first-child::before {
        content: '';
        position: absolute;
        left: 0; top: 0;
        width: 3px; height: 100%;
        background: linear-gradient(180deg,
            transparent 0%,
            var(--glow) 25%,
            var(--ice) 50%,
            var(--glow) 75%,
            transparent 100%);
        animation: sidelineScroll 3s linear infinite;
        z-index: 999;
    }
    @keyframes sidelineScroll {
        0%   { background-position: 0 -200%; }
        100% { background-position: 0  200%; }
    }
    /* ═══════════════════════════════════════════════════════
       CITY TEMPERATURE CARDS
    ═══════════════════════════════════════════════════════ */
    .city-card {
        position: relative;
        background: linear-gradient(135deg,
            rgba(0,198,255,0.08) 0%,
            rgba(10,30,70,0.6)  100%);
        border: 1px solid rgba(0,198,255,0.22);
        border-radius: 14px;
        padding: 12px 16px;
        margin: 8px 0;
        cursor: default;
        overflow: hidden;
        transition: transform .25s ease, box-shadow .25s ease;
        animation: cardIn .5s ease both;
        transform-style: preserve-3d;
    }
    .city-card:hover {
        transform: translateX(6px) scale(1.02);
        box-shadow: 0 6px 30px rgba(0,198,255,0.25),
                    inset 0 0 20px rgba(0,198,255,0.06);
    }
    .city-card::after {
        content: '';
        position: absolute;
        top: -50%; left: -60%;
        width: 40%; height: 200%;
        background: linear-gradient(90deg,
            transparent, rgba(255,255,255,0.07), transparent);
        transform: skewX(-20deg);
        transition: left .5s ease;
    }
    .city-card:hover::after { left: 160%; }
    @keyframes cardIn {
        from { opacity: 0; transform: translateX(-20px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    .city-name {
        font-family: 'Orbitron', monospace;
        font-size: .7rem;
        letter-spacing: .12em;
        text-transform: uppercase;
        color: var(--glow) !important;
        opacity: .85;
    }
    .city-temp {
        font-family: 'Orbitron', monospace;
        font-size: 1.6rem;
        font-weight: 900;
        color: var(--frost) !important;
        line-height: 1.1;
        text-shadow: 0 0 18px rgba(0,198,255,0.5);
    }
    .city-desc {
        font-family: 'Rajdhani', sans-serif;
        font-size: .78rem;
        color: rgba(168,216,240,0.7) !important;
    }
    .city-hum {
        font-family: 'Rajdhani', sans-serif;
        font-size: .7rem;
        color: rgba(0,198,255,.6) !important;
    }
    /* ═══════════════════════════════════════════════════════
       SIDEBAR HEADER
    ═══════════════════════════════════════════════════════ */
    .sidebar-header {
        font-family: 'Orbitron', monospace;
        font-size: .65rem;
        letter-spacing: .25em;
        text-transform: uppercase;
        color: var(--glow) !important;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(0,198,255,.25);
        animation: pulse 2.5s ease infinite;
    }
    @keyframes pulse { 0%,100%{opacity:.6} 50%{opacity:1} }
    /* ═══════════════════════════════════════════════════════
       MAIN TITLE / HERO
    ═══════════════════════════════════════════════════════ */
    .hero-title {
        font-family: 'Orbitron', monospace;
        font-size: clamp(2rem, 5vw, 3.4rem);
        font-weight: 900;
        text-align: center;
        letter-spacing: .06em;
        background: linear-gradient(120deg, #ffffff 0%, var(--glow) 45%, var(--ice) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
        margin-bottom: 0;
        animation: heroGlow 3s ease infinite alternate;
        line-height: 1.15;
    }
    @keyframes heroGlow {
        from { filter: drop-shadow(0 0 12px rgba(0,198,255,.4)); }
        to   { filter: drop-shadow(0 0 32px rgba(0,198,255,.9)); }
    }
    .hero-sub {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        letter-spacing: .3em;
        text-transform: uppercase;
        color: rgba(168,216,240,.55) !important;
        text-align: center;
        margin-top: 6px;
        margin-bottom: 2rem;
    }
    /* ═══════════════════════════════════════════════════════
       3-D CHAT CONTAINER
    ═══════════════════════════════════════════════════════ */
    .chat-wrap {
        perspective: 1200px;
        margin: 0 auto;
    }
    .chat-box {
        background: linear-gradient(135deg,
            rgba(5,18,45,0.82) 0%,
            rgba(8,26,60,0.72) 100%);
        backdrop-filter: blur(28px) saturate(180%);
        border: 1px solid rgba(0,198,255,.25);
        border-radius: 24px;
        padding: 28px 32px;
        box-shadow:
            0 40px 80px rgba(0,0,0,.55),
            0 0 0 1px rgba(255,255,255,.04),
            inset 0 1px 0 rgba(255,255,255,.07);
        transform: rotateX(2deg) rotateY(-1deg);
        transition: transform .4s ease, box-shadow .4s ease;
        animation: floatBox 5s ease-in-out infinite;
    }
    .chat-box:hover {
        transform: rotateX(0deg) rotateY(0deg) scale(1.008);
        box-shadow:
            0 50px 100px rgba(0,0,0,.65),
            0 0 60px rgba(0,198,255,.12),
            inset 0 1px 0 rgba(255,255,255,.09);
    }
    @keyframes floatBox {
        0%,100% { transform: rotateX(2deg) rotateY(-1deg) translateY(0);   }
        50%     { transform: rotateX(2deg) rotateY(-1deg) translateY(-6px); }
    }
    /* ═══════════════════════════════════════════════════════
       CHAT MESSAGES
    ═══════════════════════════════════════════════════════ */
    .msg-wrap { animation: msgIn .4s ease both; }
    @keyframes msgIn {
        from { opacity:0; transform: translateY(16px) scale(.97); }
        to   { opacity:1; transform: translateY(0)   scale(1);   }
    }
    .msg-user {
        background: linear-gradient(135deg,
            rgba(0,198,255,.18) 0%,
            rgba(0,100,200,.12) 100%);
        border: 1px solid rgba(0,198,255,.3);
        border-radius: 18px 18px 6px 18px;
        padding: 12px 18px;
        margin: 8px 0 8px 60px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        color: var(--frost) !important;
    }
    .msg-bot {
        background: linear-gradient(135deg,
            rgba(255,107,53,.08) 0%,
            rgba(20,10,40,.6)  100%);
        border: 1px solid rgba(255,107,53,.25);
        border-radius: 18px 18px 18px 6px;
        padding: 14px 18px;
        margin: 8px 60px 8px 0;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        color: var(--frost) !important;
        white-space: pre-wrap;
    }
    .lbl {
        font-family: 'Orbitron', monospace;
        font-size: .6rem;
        letter-spacing: .15em;
        margin-bottom: 4px;
        opacity: .55;
    }
    .lbl-u { color: var(--glow)   !important; }
    .lbl-b { color: var(--accent) !important; }
    /* ═══════════════════════════════════════════════════════
       STREAMLIT INPUT OVERRIDE
    ═══════════════════════════════════════════════════════ */
    [data-testid="stTextInput"] input {
        background: rgba(5,15,40,.75) !important;
        border: 1px solid rgba(0,198,255,.35) !important;
        border-radius: 12px !important;
        color: #e8f4ff !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.05rem !important;
        padding: 14px 18px !important;
        box-shadow: 0 0 0 0 rgba(0,198,255,0) !important;
        transition: box-shadow .25s, border-color .25s !important;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: var(--glow) !important;
        box-shadow: 0 0 20px rgba(0,198,255,.35) !important;
        outline: none !important;
    }
    [data-testid="stTextInput"] label {
        font-family: 'Orbitron', monospace !important;
        font-size: .65rem !important;
        letter-spacing: .2em !important;
        color: rgba(0,198,255,.7) !important;
    }
    /* ═══════════════════════════════════════════════════════
       STREAMLIT BUTTON
    ═══════════════════════════════════════════════════════ */
    [data-testid="stButton"] button {
        background: linear-gradient(135deg,
            rgba(0,198,255,.25), rgba(0,80,180,.35)) !important;
        border: 1px solid rgba(0,198,255,.45) !important;
        border-radius: 10px !important;
        color: var(--frost) !important;
        font-family: 'Orbitron', monospace !important;
        font-size: .7rem !important;
        letter-spacing: .15em !important;
        padding: 10px 22px !important;
        transition: all .25s ease !important;
        text-transform: uppercase !important;
    }
    [data-testid="stButton"] button:hover {
        background: linear-gradient(135deg,
            rgba(0,198,255,.45), rgba(0,80,180,.55)) !important;
        box-shadow: 0 0 20px rgba(0,198,255,.4) !important;
        transform: translateY(-2px) !important;
    }
    /* ═══════════════════════════════════════════════════════
       MISC
    ═══════════════════════════════════════════════════════ */
    hr { border-color: rgba(0,198,255,.15) !important; }
    /* hide default Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden !important; }
    </style>
    <!-- SNOW CANVAS -->
    <canvas id="snow-canvas"></canvas>
    <script>
    (function() {
        var canvas = document.getElementById('snow-canvas');
        var ctx    = canvas.getContext('2d');
        var flakes = [];
        var W, H;
        function resize() {
            W = canvas.width  = window.innerWidth;
            H = canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();
        /* Create snowflakes */
        for (var i = 0; i < 220; i++) {
            flakes.push({
                x:     Math.random() * W,
                y:     Math.random() * H,
                r:     Math.random() * 3.2 + .6,
                speed: Math.random() * 1.2 + .3,
                drift: (Math.random() - .5) * .5,
                alpha: Math.random() * .55 + .25,
                wobble: Math.random() * Math.PI * 2,
                wobbleSpeed: (Math.random() - .5) * .02,
            });
        }
        function draw() {
            ctx.clearRect(0, 0, W, H);
            flakes.forEach(function(f) {
                f.wobble += f.wobbleSpeed;
                f.x += f.drift + Math.sin(f.wobble) * .4;
                f.y += f.speed;
                if (f.y > H + 10) { f.y = -10; f.x = Math.random() * W; }
                if (f.x > W + 10) f.x = -10;
                if (f.x < -10)    f.x = W + 10;
                /* 3-D depth shimmer */
                var gradient = ctx.createRadialGradient(
                    f.x, f.y, 0,
                    f.x, f.y, f.r * 2.5
                );
                gradient.addColorStop(0,   'rgba(255,255,255,'+(f.alpha)+')');
                gradient.addColorStop(.5,  'rgba(168,216,240,'+(f.alpha*.7)+')');
                gradient.addColorStop(1,   'rgba(0,198,255,0)');
                ctx.beginPath();
                ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2);
                ctx.fillStyle = gradient;
                ctx.shadowColor = 'rgba(200,240,255,.6)';
                ctx.shadowBlur  = f.r * 3;
                ctx.fill();
                ctx.shadowBlur = 0;
            });
            requestAnimationFrame(draw);
        }
        draw();
    })();
    </script>
    """,
    unsafe_allow_html=True,
)

# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# ── Sidebar: live city temperatures ──────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-header">🌡 Live City Temps</div>', unsafe_allow_html=True)

    for city in CITIES:
        w = fetch_weather(city)
        if w:
            st.markdown(
                f"""
                <div class="city-card">
                    <div class="city-name">{city}</div>
                    <div class="city-temp">{w['temp']:.1f}°C</div>
                    <div class="city-desc">{w['desc']}</div>
                    <div class="city-hum">💧 {w['humidity']}% humidity</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="city-card">
                    <div class="city-name">{city}</div>
                    <div class="city-temp" style="font-size:1rem;opacity:.5;">No data</div>
                    <div class="city-desc">Check API key</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh"):
        st.rerun()

# ── Main content ──────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">❄ City AI Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Weather · News · Intelligence</div>', unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-wrap"><div class="chat-box">', unsafe_allow_html=True)

if not st.session_state.history:
    st.markdown(
        """
        <div style="text-align:center;padding:30px 0;opacity:.45;">
            <div style="font-family:'Orbitron',monospace;font-size:.75rem;
                        letter-spacing:.2em;color:#a8d8f0;margin-bottom:8px;">
                AGENT ONLINE
            </div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:.95rem;color:#7ab4d4;">
                Ask about weather or news for any Indian city.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    for role, text in st.session_state.history:
        if role == "user":
            st.markdown(
                f'<div class="msg-wrap"><div class="lbl lbl-u">YOU</div>'
                f'<div class="msg-user">{text}</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="msg-wrap"><div class="lbl lbl-b">AGENT</div>'
                f'<div class="msg-bot">{text}</div></div>',
                unsafe_allow_html=True,
            )

st.markdown("</div></div>", unsafe_allow_html=True)  # close chat-box / chat-wrap

# ── Input row ─────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Ask the Agent",
        placeholder="e.g. What is the weather in Mumbai?",
        key=f"user_input_{st.session_state.input_key}",
        label_visibility="visible",
    )
with col2:
    st.markdown("<div style='margin-top:28px'>", unsafe_allow_html=True)
    send = st.button("Send ➤")
    st.markdown("</div>", unsafe_allow_html=True)

# ── Handle submission ─────────────────────────────────────────────────────────
if send and user_input.strip():
    query = user_input.strip()
    st.session_state.history.append(("user", query))

    # ── Try to run the real LangChain agent ──────────────────────────────────
    response_text = None
    try:
        from langchain_mistralai import ChatMistralAI
        from langchain.tools import tool as lc_tool
        from tavily import TavilyClient

        @lc_tool
        def get_weather_tool(city: str) -> str:
            """Get current weather of a city"""
            w = fetch_weather(city)
            if w:
                return (
                    f"Weather in {city}: {w['desc']}, {w['temp']}°C "
                    f"(feels like {w['feels']}°C), humidity {w['humidity']}%"
                )
            return f"Could not fetch weather for {city}."

        @lc_tool
        def get_news_tool(city: str) -> str:
            """Get latest news about a city"""
            tavily_api_key = os.getenv("TAVILY_API_KEY", "")
            if not tavily_api_key:
                return "Tavily API key not set."
            tc = TavilyClient(api_key=tavily_api_key)
            res = tc.search(
                query=f"latest news in {city}",
                search_depth="basic",
                max_results=3,
            )
            results = res.get("results", [])
            if not results:
                return f"No news found for {city}."
            lines = []
            for r in results:
                title   = r.get("title", "No title")
                url     = r.get("url", "")
                snippet = r.get("content", "")[:120]
                lines.append(f"• {title}\n  {url}\n  {snippet}...")
            return f"Latest news in {city}:\n\n" + "\n\n".join(lines)

        llm   = ChatMistralAI(model="mistral-small-2506")
        tools = [get_weather_tool, get_news_tool]
        llm_with_tools = llm.bind_tools(tools)
        tool_map = {t.name: t for t in tools}

        from langchain_core.messages import HumanMessage, ToolMessage

        messages = [HumanMessage(content=query)]
        ai_msg   = llm_with_tools.invoke(messages)
        messages.append(ai_msg)

        # tool calls loop
        while ai_msg.tool_calls:
            for tc in ai_msg.tool_calls:
                tool_result = tool_map[tc["name"]].invoke(tc["args"])
                messages.append(
                    ToolMessage(content=str(tool_result), tool_call_id=tc["id"])
                )
            ai_msg = llm_with_tools.invoke(messages)
            messages.append(ai_msg)

        response_text = ai_msg.content

    except Exception as e:
        # Graceful fallback when keys / packages missing
        lower = query.lower()
        for city in CITIES:
            if city.lower() in lower:
                w = fetch_weather(city)
                if w and ("weather" in lower or "temp" in lower):
                    response_text = (
                        f"🌡 **{city}** — {w['desc']}\n"
                        f"Temperature : {w['temp']}°C  (feels like {w['feels']}°C)\n"
                        f"Humidity    : {w['humidity']}%"
                    )
                    break
        if response_text is None:
            response_text = (
                f"⚠️ Agent unavailable: {e}\n\n"
                "Please ensure OPENWEATHER_API_KEY, TAVILY_API_KEY, "
                "and MISTRAL_API_KEY are set in your .env file."
            )

    st.session_state.history.append(("bot", response_text))
    st.session_state.input_key += 1
    st.rerun()
