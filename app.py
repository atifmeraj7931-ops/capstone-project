import time  # ⏱️ ADDED: The built-in time module
import streamlit as st
from auditor import analyze_code
from engine import RefactorEngine
from executor import execute_code  

st.set_page_config(page_title="Refactor Engine AI", layout="wide")

st.title("🛡️ Hybrid Refactoring Engine")
st.markdown("### AI Diagnosis • Deterministic Execution • Efficiency Scoring")

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("⚙️ Control Panel")
    language = st.selectbox("Language", ["Python", "JavaScript", "Java", "C++"])
    opt_type = st.radio(
        "Optimization Goal",
        ["Readability & Clean Code", "Performance (Time Complexity)", "Memory Efficiency (Space)", "Security Hardening"]
    )

# --- INPUT SECTION ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Source Code")
    code_input = st.text_area("Paste your code here:", height=500, key="source_code")

analyze_click = st.button("🚀 Analyze & Refactor Code", type="primary", use_container_width=True)

# --- AI EXECUTION & STATE SAVING ---
if analyze_click:
    if not code_input:
        st.warning("Please paste some code first.")
    else:
        # ⏱️ START AI STOPWATCH
        ai_start_time = time.time()
        
        with st.spinner("🧠 AI Architect is analyzing code structure..."):
            plan = analyze_code(code_input, opt_type, language)
            
            if "error" in plan:
                if "Language Mismatch" in plan.get('error', ''):
                    st.error("🚨 " + plan['error'])
                    st.info(f"👉 **Tip:** Go to the Sidebar and switch the language to match your code.")
                else:
                    st.error(plan.get('error', 'Unknown AI Error'))
                st.stop()
        
        with st.spinner("⚙️ Engine is applying patches..."):
            engine = RefactorEngine(code_input)
            new_code, logs = engine.apply_updates(plan)
            
            # ⏱️ STOP AI STOPWATCH & CALCULATE
            ai_end_time = time.time()
            ai_latency = ai_end_time - ai_start_time
            
            # SAVE TO MEMORY (Included the new timer!)
            st.session_state['new_code'] = new_code
            st.session_state['plan'] = plan
            st.session_state['orig_code'] = code_input
            st.session_state['ai_latency'] = ai_latency  # ⏱️ Save the time to memory

# --- DISPLAY RESULTS & SANDBOX ---
if 'new_code' in st.session_state:
    
    plan = st.session_state['plan']
    new_code = st.session_state['new_code']
    orig_code = st.session_state['orig_code']
    ai_latency = st.session_state.get('ai_latency', 0.0)

    st.divider()
    st.subheader("📊 Efficiency Analysis & Metrics")
    
    raw_scores = plan.get("scores", {})
    if not isinstance(raw_scores, dict): raw_scores = {}
    
    try:
        orig = int(raw_scores.get('original', 0))
        new = int(raw_scores.get('refactored', 0))
    except:
        orig, new = 0, 0
    
    delta_val = new - orig

    # ⏱️ UPDATED METRICS ROW: Added a 4th column for the Time Metric!
    m_col1, m_col2, m_col3, m_col4 = st.columns([1, 1, 1, 2])
    m_col1.metric("Original Score", f"{orig}/100")
    m_col2.metric("Refactored Score", f"{new}/100", delta=delta_val)
    m_col3.metric("🤖 AI Response Time", f"{ai_latency:.2f}s") # ⏱️ Displays the AI Time!
    m_col4.info(f"**Architect's Notes:**\n\n{plan.get('explanation', 'No notes provided.')}")

    with col2:
        st.subheader("✨ Refactored Code")
        st.code(new_code, language=language.lower())

    # --- LIVE EXECUTION SANDBOX ---
    st.divider()
    st.subheader("🧪 Automated Regression Testing (Local testing)")
    st.markdown("Append function calls or print statements to test functional equivalence.")

    col_test, col_stdin = st.columns([2, 1])
    
    with col_test:
        test_cases = st.text_area(
            "Append Execution Code (Leave blank for C++/Java main methods):", 
            placeholder="print(my_function())",
            height=150
        )
        
    with col_stdin:
        user_stdin = st.text_area(
            "Standard Input (Optional):", 
            placeholder="For input() or cin >>",
            height=150
        )

    if st.button("▶️ Run & Compare Outputs", type="secondary", use_container_width=True):
        
        full_original_code = orig_code + "\n\n" + test_cases
        full_refactored_code = new_code + "\n\n" + test_cases

        # ⏱️ START SANDBOX STOPWATCH
        exec_start_time = time.time()

        out_col1, out_col2 = st.columns(2)

        with out_col1:
            st.markdown("**Terminal: Original Code**")
            with st.spinner("Compiling & Running..."):
                orig_output = execute_code(full_original_code, language, user_stdin)
            st.code(orig_output, language="text")

        with out_col2:
            st.markdown("**Terminal: Refactored Code**")
            with st.spinner("Compiling & Running..."):
                new_output = execute_code(full_refactored_code, language, user_stdin)
            st.code(new_output, language="text")
            
        # ⏱️ STOP SANDBOX STOPWATCH & DISPLAY
        exec_end_time = time.time()
        exec_latency = exec_end_time - exec_start_time
        st.metric(label="⚡ Local Sandbox Execution Time (Compiled Both)", value=f"{exec_latency:.4f} seconds")

        if orig_output == new_output:
            st.success("✅ **Verification Passed!** Both versions produced the exact same output. Logic is preserved.")
        else:
            st.error("❌ **Verification Failed!** The outputs are different. The AI hallucinated or broke the logic.")