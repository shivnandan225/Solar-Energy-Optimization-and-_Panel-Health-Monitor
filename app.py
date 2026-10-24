from __future__ import annotations

from datetime import datetime
from io import BytesIO

import streamlit as st
from PIL import Image, ImageStat


st.set_page_config(
    page_title="Sunwise | Solar, made smarter",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

HERO_IMAGE = (
    "https://images.unsplash.com/photo-1509391366360-2e959784a276"
    "?auto=format&fit=crop&w=2000&q=85"
)
ROOFTOP_IMAGE = (
    "https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9"
    "?auto=format&fit=crop&w=1400&q=85"
)
FIELD_IMAGE = (
    "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e"
    "?auto=format&fit=crop&w=1400&q=85"
)


def initialize_state() -> None:
    defaults = {"page": "Home", "light_mode": False, "reports": [], "messages": []}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def apply_theme(light_mode: bool) -> None:
    background = "#f4f5ef" if light_mode else "#080b0a"
    surface = "#ffffff" if light_mode else "#111715"
    text = "#17211d" if light_mode else "#f4f7f3"
    muted = "#59675f" if light_mode else "#aab6ae"
    border = "#d8dfd9" if light_mode else "#26312b"
    st.markdown(
        f"""
        <style>
        .stApp {{ background: {background}; color: {text}; }}
        [data-testid="stHeader"] {{ background: transparent; }}
        [data-testid="stSidebar"] {{ background: {surface}; }}
        [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"],
        [data-testid="stCaptionContainer"], .stSelectbox, .stTextInput,
        .stTextArea, .stNumberInput, .stDateInput, .stFileUploader,
        .stRadio, .stCheckbox, .stMetric {{ color: {text}; }}
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stCaptionContainer"] {{ color: {muted}; }}
        [data-testid="stVerticalBlockBorderWrapper"] {{
            background: {surface}; border-color: {border};
        }}
        [data-testid="stImage"] img {{ border-radius: 16px; }}
        h1, h2, h3 {{ color: {text}; letter-spacing: -0.035em; }}
        .eyebrow {{ color: #b8f36b; font-size: .8rem; font-weight: 700;
                    letter-spacing: .14em; text-transform: uppercase; }}
        .hero-title {{ font-size: clamp(2.5rem, 6vw, 5.3rem); line-height: .98;
                       font-weight: 850; letter-spacing: -.06em; color: {text}; }}
        .hero-copy {{ color: {muted}; font-size: 1.1rem; line-height: 1.7;
                      max-width: 680px; }}
        .callout {{ padding: 1rem 1.2rem; border-left: 3px solid #b8f36b;
                    background: {surface}; border-radius: 0 12px 12px 0; }}
        .tag {{ color: #b8f36b; font-weight: 700; }}
        div.stButton > button[kind="primary"] {{
            background: #b8f36b; color: #10150e; border: 0; font-weight: 750;
        }}
        div.stButton > button[kind="primary"]:hover {{
            background: #c9ff80; color: #10150e; border: 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_heading(kicker: str, title: str, copy: str | None = None) -> None:
    st.markdown(f'<p class="eyebrow">{kicker}</p>', unsafe_allow_html=True)
    st.header(title)
    if copy:
        st.write(copy)


def estimate_daily_reply(question: str) -> str:
    text = question.casefold()
    if any(word in text for word in ("fire", "smoke", "burn", "spark", "shock")):
        return (
            "**Treat this as an emergency.** Keep away from the panels, inverter, "
            "and wiring. Do not touch wet or damaged equipment. Call local emergency "
            "services if there is fire or immediate danger, then contact a licensed "
            "solar electrician. Do not attempt a live electrical repair."
        )
    if any(word in text for word in ("low", "less", "drop", "not generating", "output")):
        return (
            "A production drop can come from cloud cover, shade, dirt, a tripped "
            "breaker, or an inverter alert. Compare today's output with a similar "
            "sunny day and check the inverter display/app for an error code. Don't "
            "open the inverter or touch rooftop wiring. Add a photo and the error "
            "code to a service report if the drop persists."
        )
    if any(word in text for word in ("inverter", "error", "fault code", "alarm")):
        return (
            "Write down the exact inverter model and displayed code, then check the "
            "manufacturer's user manual for its meaning. A normal reboot is only "
            "appropriate if the manual explicitly recommends it. Leave covers, "
            "isolators, and wiring to a qualified electrician."
        )
    if any(word in text for word in ("clean", "dust", "bird", "dirt")):
        return (
            "Light soiling may reduce output. Never climb onto a roof or clean a "
            "hot, cracked, or electrically damaged panel. For safe ground-level "
            "maintenance, follow the panel maker's instructions; otherwise book a "
            "qualified cleaning service."
        )
    if any(word in text for word in ("crack", "broken", "glass", "hotspot", "hot spot")):
        return (
            "A photo can document visible damage, but it cannot verify the cells, "
            "insulation, or internal connections. Keep clear of cracked glass and "
            "exposed wiring. Photograph it from a safe location and submit a "
            "technician report for an on-site electrical and thermal inspection."
        )
    return (
        "I can help with common production drops, inverter alerts, visible damage, "
        "and safe maintenance. Tell me what the inverter shows, when the issue "
        "started, and whether any alarms or visible damage are present. For any "
        "smoke, sparks, shock, or exposed wiring, keep away and contact emergency "
        "services or a licensed solar electrician."
    )


def render_home() -> None:
    left, right = st.columns([1.05, 0.95], vertical_alignment="center")
    with left:
        st.markdown('<p class="eyebrow">A brighter way to run solar</p>', unsafe_allow_html=True)
        st.markdown(
            '<div class="hero-title">Know your panels.<br>Own your power.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="hero-copy">A friendly solar companion for photo-based '
            'visual checks, practical troubleshooting, performance planning, '
            'and getting the right human help.</p>',
            unsafe_allow_html=True,
        )
        if st.button("Explore solar care", type="primary", icon=":material/arrow_forward:"):
            st.session_state.page = "Solar care"
            st.rerun()
        st.caption("Built for homeowners, communities, and the people who keep solar working.")
    with right:
        st.image(HERO_IMAGE, caption="Turn sunshine into a smarter everyday resource.")

    st.write("")
    section_heading("Your solar toolkit", "From first photo to next step")
    cards = st.columns(3)
    with cards[0]:
        with st.container(border=True):
            st.markdown("### :material/photo_camera: Visual panel check")
            st.write("Upload a panel photo to check image quality and prepare a useful inspection record.")
    with cards[1]:
        with st.container(border=True):
            st.markdown("### :material/chat: Solar guide")
            st.write("Get clear, safety-first guidance for common panel and inverter symptoms.")
    with cards[2]:
        with st.container(border=True):
            st.markdown("### :material/monitoring: Performance planner")
            st.write("Estimate monthly generation and explore how shade and system size affect it.")

    st.info(
        "A photo cannot prove that a panel's cells or internal electrical connections are healthy. "
        "This demo screens image quality and helps you prepare for a qualified inspection."
    )


def render_photo_check() -> None:
    section_heading(
        "01 / Visual screening",
        "Start with a clear photo",
        "Upload a close, well-lit image taken from a safe place. This check measures image quality "
        "and helps package evidence for a technician; it does not diagnose internal panel faults.",
    )
    photo = st.file_uploader(
        "Choose a panel photo",
        type=["jpg", "jpeg", "png", "webp"],
        help="JPG, PNG, or WebP. Do not climb onto a roof or approach damaged wiring to take a photo.",
    )
    if photo:
        try:
            image = Image.open(BytesIO(photo.getvalue())).convert("RGB")
            stats = ImageStat.Stat(image)
        except (OSError, ValueError) as error:
            st.error(f"That image could not be opened: {error}")
            return
        preview, detail = st.columns([1, 1], vertical_alignment="center")
        with preview:
            st.image(image, caption=f"Uploaded image · {image.width} × {image.height}")
        with detail:
            brightness = sum(stats.mean) / 3
            contrast = sum(stats.stddev) / 3
            st.metric("Image dimensions", f"{image.width} × {image.height}")
            if image.width < 600 or image.height < 400:
                st.warning("Small image: retake closer, without zoom, if you can do so safely.")
            elif brightness < 45:
                st.warning("The image is quite dark; a daylight photo may show more detail.")
            elif brightness > 235:
                st.warning("Strong glare may hide surface details; try a different angle.")
            elif contrast < 18:
                st.warning("Low image contrast; a sharper, evenly lit photo may help.")
            else:
                st.success("Image quality looks suitable for documenting a visual inspection.")
            st.caption(
                f"Average brightness: {brightness:.0f}/255 · image contrast: {contrast:.0f}/128. "
                "These are image-quality indicators, not a panel-health score."
            )
        st.divider()
        st.write("**What can you see?** Select any signs you noticed. This is your observation, not automated image recognition.")
        signs = st.pills(
            "Visible observations",
            ["Cracked glass", "Heavy dirt", "Shade", "Discoloration", "Loose cable", "No obvious issue"],
            selection_mode="multi",
            key="photo_signs",
        )
        location = st.text_input("Panel location or label", placeholder="For example: roof east / panel 04")
        if st.button("Prepare technician notes", icon=":material/description:"):
            notes = [
                f"Panel: {location or 'Not specified'}",
                f"Image: {image.width} × {image.height}",
                f"Observations: {', '.join(signs) if signs else 'None selected'}",
                "Please inspect panel cells, connectors, insulation, and string performance on site.",
                "Image screening does not verify electrical or internal panel health.",
            ]
            st.code("\n".join(notes))
            st.download_button(
                "Download inspection notes",
                data="\n".join(notes),
                file_name="solar-inspection-notes.txt",
                mime="text/plain",
            )


def render_assistant() -> None:
    section_heading(
        "02 / Solar guide",
        "A calm first step",
        "Ask about common symptoms. This offline demo uses a small, transparent troubleshooting guide "
        "and is not a substitute for a licensed solar professional.",
    )
    suggestions = st.pills(
        "Try a question",
        ["My output is lower than usual", "The inverter shows an error", "There is cracked glass"],
        key="question_suggestions",
    )
    if suggestions and not st.session_state.messages:
        st.session_state.messages.append({"role": "user", "content": suggestions})
        st.session_state.messages.append(
            {"role": "assistant", "content": estimate_daily_reply(suggestions)}
        )
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    with st.form("solar_chat_form", clear_on_submit=True):
        prompt = st.text_input(
            "Describe the problem",
            placeholder="For example: my inverter shows an error code",
            max_chars=500,
        )
        submitted = st.form_submit_button("Ask the solar guide", type="primary")
    if submitted and prompt.strip():
        st.session_state.messages.append({"role": "user", "content": prompt})
        answer = estimate_daily_reply(prompt)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()
    if st.button("Clear conversation", icon=":material/delete_outline:"):
        st.session_state.messages = []
        st.rerun()
    st.warning(
        "If you notice smoke, sparks, electric shock, exposed wiring, or fire: stay away, "
        "do not touch the equipment, and contact emergency services or a licensed electrician."
    )


def render_optimizer() -> None:
    section_heading(
        "03 / Energy planner",
        "Find your solar sweet spot",
        "A quick estimate helps you explore system size, sunshine, shading, and self-consumption. "
        "Use your installer or utility data for real decisions.",
    )
    controls, results = st.columns([0.9, 1.1], vertical_alignment="center")
    with controls:
        with st.container(border=True):
            capacity = st.number_input("System size (kW)", min_value=0.5, max_value=100.0, value=5.0, step=0.5)
            sun_hours = st.number_input("Average peak sun hours / day", min_value=1.0, max_value=10.0, value=5.0, step=0.5)
            efficiency = st.slider("System efficiency", min_value=50, max_value=100, value=80, format="%d%%")
            shade = st.slider("Estimated shade loss", min_value=0, max_value=60, value=10, format="%d%%")
            daily_demand = st.number_input(
                "Household electricity use (kWh / day)",
                min_value=0.0,
                max_value=1000.0,
                value=15.0,
                step=1.0,
            )
            self_use = st.slider(
                "Solar generation available while you use power",
                min_value=0,
                max_value=100,
                value=70,
                format="%d%%",
            )
            tariff = st.number_input(
                "Electricity price (your currency / kWh)",
                min_value=0.0,
                max_value=10000.0,
                value=8.0,
                step=0.5,
            )
    daily_kwh = capacity * sun_hours * efficiency / 100 * (1 - shade / 100)
    monthly_kwh = daily_kwh * 30
    annual_kwh = daily_kwh * 365
    monthly_demand = daily_demand * 30
    direct_use = min(monthly_kwh * self_use / 100, monthly_demand)
    grid_import = max(monthly_demand - direct_use, 0)
    estimated_offset = direct_use * tariff
    exported_or_unused = max(monthly_kwh - direct_use, 0)
    with results:
        st.metric("Estimated generation", f"{monthly_kwh:,.0f} kWh / month")
        st.metric("Estimated solar used at home", f"{direct_use:,.0f} kWh / month")
        st.metric("Estimated grid electricity needed", f"{grid_import:,.0f} kWh / month")
        st.metric("Potential bill offset", f"{estimated_offset:,.0f} currency units / month")
        st.caption(f"Estimated exported or unused solar: {exported_or_unused:,.0f} kWh / month.")
        st.metric("Indicative avoided emissions", f"{annual_kwh * 0.7:,.0f} kg CO₂ / year")
        st.caption(
            "Illustrative estimate only. Actual generation depends on local weather, orientation, "
            "equipment, consumption timing, export rules, and your tariff. Bill offset assumes "
            "self-used solar replaces grid electricity at the price you entered; 0.7 kg CO₂/kWh "
            "is a placeholder emissions factor."
        )
        st.bar_chart(
            {"Estimated generation (kWh)": [round(daily_kwh * days, 1) for days in (28, 30, 31)]},
            x_label="Example month length (days)",
            y_label="Energy (kWh)",
        )
    st.markdown(
        '<div class="callout"><b>Optimization tip:</b> If it is safe and practical, run flexible '
        'appliances during sunny hours to use more of your own solar. A real schedule should use '
        'your actual tariff, forecast, and inverter data.</div>',
        unsafe_allow_html=True,
    )


def render_generation_trend() -> None:
    section_heading(
        "04 / Performance watch",
        "Spot a change in generation",
        "Compare recent daily output with your own earlier readings. This can flag a trend worth "
        "checking, but it cannot identify a fault or account for changing weather.",
    )
    st.caption(
        "Enter daily inverter production in kWh from oldest to newest. Use similar-length days "
        "and include units from the same system."
    )
    if st.button("Load example readings", icon=":material/analytics:"):
        st.session_state.generation_readings = "22.4, 23.1, 21.8, 22.7, 22.2, 21.9, 17.8, 17.2, 16.9"
    readings_text = st.text_area(
        "Daily generation readings (kWh, comma-separated)",
        placeholder="Example: 22.4, 23.1, 21.8, 22.7, 22.2, 21.9, 17.8, 17.2, 16.9",
        key="generation_readings",
        help="Enter at least six daily readings to compare the latest three with the previous three.",
    )
    if not readings_text.strip():
        st.info("Add readings above, or load the example, to see your trend.")
        return
    try:
        readings = [float(value.strip()) for value in readings_text.split(",") if value.strip()]
    except ValueError:
        st.error("Use comma-separated numbers only, for example: 22.4, 23.1, 21.8.")
        return
    if any(value < 0 for value in readings):
        st.error("Generation readings cannot be negative.")
        return
    if len(readings) < 2:
        st.info("Enter at least two daily readings to display a trend.")
        return
    st.line_chart({"Daily generation (kWh)": readings}, x_label="Day (oldest to newest)", y_label="kWh")
    if len(readings) < 6:
        st.info(f"Add {6 - len(readings)} more daily reading(s) to compare two three-day averages.")
        return
    baseline = sum(readings[-6:-3]) / 3
    recent = sum(readings[-3:]) / 3
    if baseline == 0:
        st.warning("The previous three-day average is zero; enter valid production readings to compare.")
        return
    change = (recent - baseline) / baseline * 100
    first, second, third = st.columns(3)
    first.metric("Previous 3-day average", f"{baseline:.1f} kWh / day")
    second.metric("Latest 3-day average", f"{recent:.1f} kWh / day")
    third.metric("Change vs. previous 3 days", f"{change:+.0f}%")
    if change <= -20:
        st.warning(
            "Recent generation is notably lower than the entered baseline. Check whether the "
            "weather or shading changed, then review inverter alerts. If the drop persists in "
            "comparable sunny conditions, contact a qualified installer."
        )
    else:
        st.success(
            "No 20% drop appears in this comparison. This does not certify the panels as healthy; "
            "continue monitoring under comparable weather conditions."
        )


def render_hardware_check() -> None:
    section_heading(
        "05 / Equipment check",
        "A guided equipment snapshot",
        "Enter readings from your inverter display or a properly installed monitor. This prototype "
        "does not connect to hardware or replace manufacturer limits.",
    )
    with st.form("equipment_form"):
        system_name = st.text_input("Equipment name", placeholder="For example: Inverter A / string 1")
        voltage = st.number_input("Measured DC voltage (V)", min_value=0.0, max_value=2000.0, value=0.0, step=1.0)
        current = st.number_input("Measured current (A)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        expected_voltage = st.number_input(
            "Expected voltage from equipment documentation (V)",
            min_value=0.0,
            max_value=2000.0,
            value=400.0,
            step=5.0,
        )
        submitted = st.form_submit_button("Check this snapshot", type="primary")
    if submitted:
        output_w = voltage * current
        st.metric("Calculated DC power", f"{output_w:,.0f} W")
        if voltage <= 0 or current <= 0:
            st.error("No usable reading entered. Check the display or sensor, and follow the manual.")
        elif expected_voltage <= 0:
            st.warning("Enter the expected range from the equipment documentation before comparing.")
        elif abs(voltage - expected_voltage) / expected_voltage > 0.15:
            st.warning(
                f"{system_name or 'Equipment'}: voltage differs from your entered reference by more "
                "than 15%. Recheck conditions and report it to your installer; this is not a fault diagnosis."
            )
        else:
            st.success(
                f"{system_name or 'Equipment'}: this reading is within 15% of the reference you entered. "
                "That alone does not prove the equipment is healthy."
            )
    st.caption(
        "For a real hardware checker, integrate a supported inverter/monitor API or certified sensor gateway, "
        "authenticate securely, and compare readings with the manufacturer's limits."
    )


def render_reports() -> None:
    section_heading(
        "06 / Human help",
        "Send a service report",
        "Record the symptom and request a manual follow-up. In this demo, reports are held only in this "
        "browser session; no report is sent to a real technician.",
    )
    with st.form("service_report", clear_on_submit=True):
        contact_name = st.text_input("Your name")
        phone = st.text_input("Phone number for callback")
        issue_type = st.selectbox(
            "What needs attention?",
            ["Low energy output", "Inverter warning", "Visible panel damage", "Hardware reading", "Other"],
        )
        urgency = st.selectbox("Urgency", ["Routine", "Soon", "Safety concern"])
        description = st.text_area("Describe what happened", max_chars=1200)
        attachment = st.file_uploader("Attach a photo or screenshot (optional)", type=["jpg", "jpeg", "png", "webp"])
        consent = st.checkbox("I agree this demo stores this report only for this browser session.")
        sent = st.form_submit_button("Save report for this session", type="primary")
    if sent:
        if not description.strip():
            st.error("Please describe the issue before submitting.")
        elif not consent:
            st.error("Please confirm the session-only storage notice before submitting.")
        else:
            st.session_state.reports.append(
                {
                    "id": f"SW-{datetime.now().strftime('%y%m%d-%H%M%S')}",
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "name": contact_name,
                    "phone": phone,
                    "issue": issue_type,
                    "urgency": urgency,
                    "description": description.strip(),
                    "attachment": attachment.name if attachment else "None",
                }
            )
            st.success(f"Saved report {st.session_state.reports[-1]['id']} in this session.")
    if st.session_state.reports:
        st.subheader("Session reports")
        st.dataframe(st.session_state.reports, width="stretch", hide_index=True)
        csv = "Report ID,Created,Name,Phone,Issue,Urgency,Description,Attachment\n" + "\n".join(
            ",".join(
                '"' + str(row[key]).replace('"', '""') + '"'
                for key in ("id", "created", "name", "phone", "issue", "urgency", "description", "attachment")
            )
            for row in st.session_state.reports
        )
        st.download_button("Download report log", csv, "sunwise-reports.csv", "text/csv")
    st.markdown("**Need to call someone?** Add your local provider’s number after deployment:")
    phone_link = st.text_input("Licensed solar technician phone number", placeholder="+1 555 010 1234")
    if phone_link.strip():
        tel_number = "".join(char for char in phone_link if char.isdigit() or char == "+")
        st.markdown(f"[Call your technician: {phone_link}](tel:{tel_number})")
    st.caption("Safety concern? Do not wait for this demo to be reviewed. Keep away and call local emergency services.")


def render_solar_why() -> None:
    section_heading(
        "A better energy future",
        "Why solar is worth it",
        "Solar turns a daily resource into cleaner electricity close to where it is used. Pairing it "
        "with good maintenance, smart timing, and informed communities makes the benefits go further.",
    )
    st.image(ROOFTOP_IMAGE, caption="Rooftop solar can bring generation closer to homes and businesses.")
    benefits = st.columns(3)
    items = [
        (":material/energy_savings_leaf:", "Cleaner electricity", "Solar can reduce dependence on fossil-fuel electricity, depending on the local grid."),
        (":material/savings:", "More control", "Self-consumed solar can reduce grid purchases; savings depend on tariffs and system cost."),
        (":material/groups:", "Resilient communities", "Distributed generation can support local resilience when paired with appropriate storage and planning."),
    ]
    for column, (icon, title, copy) in zip(benefits, items):
        with column:
            with st.container(border=True):
                st.markdown(f"### {icon} {title}")
                st.write(copy)
    st.image(FIELD_IMAGE, caption="A clean-energy transition works best when it is reliable, safe, and community-led.")
    st.subheader("Make every kilowatt-hour count")
    st.write(
        "Clean panels only when it is safe and recommended, keep an eye on inverter alerts, use "
        "flexible appliances during sunny hours, and ask a qualified installer to investigate "
        "persistent performance changes. Never touch live electrical equipment."
    )
    st.caption(
        "Environmental impact and bill savings vary by location, grid mix, weather, installation, "
        "and electricity plan. Use local, verified sources for published claims."
    )


initialize_state()
apply_theme(st.session_state.light_mode)

brand, theme_control = st.columns([0.78, 0.22], vertical_alignment="center")
with brand:
    st.markdown("## :material/wb_sunny: Sunwise")
with theme_control:
    st.session_state.light_mode = st.toggle(
        "Light mode", value=st.session_state.light_mode, key="theme_toggle"
    )
    apply_theme(st.session_state.light_mode)

selected_page = st.segmented_control(
    "Main navigation",
    ["Home", "Solar care", "Why solar"],
    default=st.session_state.page,
    key="navigation",
    label_visibility="collapsed",
)
st.session_state.page = selected_page or "Home"
st.divider()

if st.session_state.page == "Home":
    render_home()
elif st.session_state.page == "Solar care":
    st.title("Your solar care desk")
    st.write("A practical path from a visible symptom to a safe, informed next step.")
    photo_tab, chat_tab, optimize_tab, trend_tab, hardware_tab, service_tab = st.tabs(
        ["Photo check", "Solar guide", "Energy planner", "Performance watch", "Equipment check", "Service report"]
    )
    with photo_tab:
        render_photo_check()
    with chat_tab:
        render_assistant()
    with optimize_tab:
        render_optimizer()
    with trend_tab:
        render_generation_trend()
    with hardware_tab:
        render_hardware_check()
    with service_tab:
        render_reports()
else:
    render_solar_why()

st.divider()
st.caption("SUNWISE · Demo prototype · Visual screening and educational estimates only")
