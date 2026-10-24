# Sunwise — Solar energy optimization and panel care

Sunwise is a responsive Streamlit prototype for solar owners. It combines a photo-based **visual documentation check**, a safety-first troubleshooting guide, a generation estimator, a manual equipment-reading checker, and an in-session service-report form in a three-screen website.

## Run locally

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

Open the local URL printed by Streamlit (normally `http://localhost:8501`). The interface starts in dark mode; use **Light mode** in the header to switch manually.

## What is in the prototype

- **Home:** full-width solar photography, welcome message, and direct entry to the tools.
- **Solar care:** six tabs for photo screening, a troubleshooting chat guide, usage- and tariff-aware solar estimates, generation-trend monitoring, manual equipment checks, and service reports.
- **Why solar:** benefits, maintenance guidance, and ideas for making each generated kilowatt-hour count.
- **Photo screening:** checks whether an uploaded image is readable and lets the user label visible observations. It does **not** claim to identify internal cell, wiring, insulation, or electrical faults.
- **Solar guide:** provides local, rule-based answers for common symptoms. It is not an AI model and is not a replacement for an electrician.
- **Equipment check:** compares manually entered voltage against a user-provided reference and calculates voltage × current. No hardware is connected.
- **Service reports:** stored only in Streamlit's per-user session memory; users can download the current session's report log. No technician receives the report automatically.
- **Calling:** accepts a technician's phone number and creates a `tel:` link. Add a real provider's contact after deployment.
- **Energy planner:** estimates generation, household solar use, grid imports, and a potential bill offset from user-entered system size, sun hours, efficiency, shade, household demand, use timing, and tariff. Emissions use an explicitly illustrative factor.
- **Performance watch:** compares the latest three entered daily-generation readings with the previous three and flags a notable decline for follow-up. It cannot account for weather or diagnose a fault.

## Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub and choose **Create app**.
3. Select the repository and branch, set the main file path to `app.py`, then deploy.
4. Share the app URL shown by Streamlit after deployment.

The repository includes `requirements.txt` and `.streamlit/config.toml` for deployment. A public link is created by Streamlit Community Cloud after the owner authorizes deployment; it cannot be generated from a local prototype alone.

## What is needed for a production-ready, more unique product

1. **Real panel diagnosis:** collect consented, expert-labelled visible and thermal images; train and validate a vision model across panel types, lighting, and climates. Add an IR/thermal camera or certified IV-curve testing to detect many issues that ordinary photos cannot reveal. Show confidence, uncertainty, and an escalation path; never label a panel safe based on a regular photo.
2. **Actual AI assistant:** connect an LLM through a server-side API key, ground it in manufacturer manuals and local safety guidance, cite sources, and add emergency escalation. Store credentials in deployment secrets, not source code.
3. **Hardware integration:** connect supported inverter/monitor APIs or an authenticated gateway, validate units and timestamps, and show live/history data with manufacturer-specific limits. Do not ask users to probe energized DC equipment.
4. **Real report delivery:** add secure authentication, a database, image storage with retention controls, notifications, technician assignment, status tracking, and consent/privacy controls. Current reports are deliberately session-only.
5. **Mechanic network and calling:** verify local providers, their service areas, availability, and qualifications; route users through a consent-based booking/call flow. The present `tel:` link uses a number the user enters.
6. **Local accuracy:** use a location-aware weather source, local grid-emissions factors, utility tariffs, and installer-verified system details for trustworthy savings and generation estimates.

### Hackathon differentiators to build next

- A **solar passport** per installation: equipment, commissioning readings, photos, maintenance, generation history, and technician sign-offs.
- A **weather-aware load-shifting coach** that suggests when to run flexible appliances using the next-day forecast, live production, and the user's tariff.
- **Community fault mapping** with opt-in, anonymized service patterns to highlight recurring area-wide problems without exposing household data.
- An **explainable reliability score** based on measured production and verified inspections—not a single uploaded photo—with a clear breakdown and confidence.

## Safety and data notes

This is a demonstration, not electrical equipment, medical advice, or a certified inspection. Do not touch, open, or attempt to repair live solar equipment. For smoke, fire, electric shock, sparks, or exposed wiring, stay away and contact emergency services or a licensed solar electrician. Do not upload private documents or sensitive personal information. Session reports are temporary and may disappear when the app session ends.
