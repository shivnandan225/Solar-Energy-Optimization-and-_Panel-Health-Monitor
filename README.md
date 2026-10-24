Live demo: **Not deployed yet** — deploy this app on [Streamlit Community Cloud](https://share.streamlit.io/) to get its public URL.

# Sunwise — Solar energy optimization and panel care

Sunwise is a Streamlit prototype that helps solar owners document visible panel concerns, understand common symptoms, estimate household solar use, watch generation trends, check manually entered equipment readings, and prepare a service report.

## Project prompt

> Build a polished, mobile-friendly solar energy optimization and panel-care website with three main screens: (1) a welcoming home page with beautiful solar imagery, (2) a solar-care workspace, and (3) an educational page about solar energy's benefits. Use a dark background by default, provide a manual light-mode switch, and make the main heading bold and prominent.
>
> In the solar-care workspace, include a photo upload that helps users document visible panel concerns without falsely claiming to diagnose internal faults; a conversational guide for common solar problems and safe next steps; an energy optimizer that estimates solar generation, household self-use, grid electricity needs, and potential bill offset; a generation-trend monitor that compares recent readings with the system's own baseline; a manual equipment-reading checker; and a service-report form with a way to call a technician. Explain which features are demonstrations and what integrations are needed for real AI, hardware monitoring, persistent reports, and technician dispatch.
>
> Prioritize safety and transparency: never tell users that an ordinary photo proves a panel is electrically healthy; direct users away from live or damaged equipment; and clearly label estimates, manually supplied readings, temporary data, and unconnected services.

## Features

- **Home:** welcome message, solar photography, and a direct route to the solar tools.
- **Visual photo screening:** checks image dimensions, brightness, and contrast; lets users record their own observations and download technician notes. It does not perform AI defect recognition or certify internal panel health.
- **Solar guide:** a local, rule-based troubleshooting assistant for common symptoms. It is not an LLM-powered chatbot or a substitute for a licensed solar professional.
- **Energy planner:** estimates generation from system size, peak sun hours, efficiency, and shading; estimates household solar use and grid imports using demand and use timing; and calculates a potential bill offset from the user-entered electricity tariff.
- **Performance watch:** compares the latest three daily-generation values against the previous three and flags a large drop. Weather is not accounted for, so this is a prompt to investigate—not a fault diagnosis.
- **Equipment check:** calculates DC power from manually entered voltage and current and compares voltage with the user-entered reference. No inverter, sensor, or hardware is connected.
- **Service report:** collects a problem description and optional photo, keeps records only in the current Streamlit session, and offers a CSV download. Reports are not delivered to a technician.
- **Technician call link:** turns a phone number entered by the user into a call link. No service provider directory is connected.
- **Why solar:** explains potential benefits and safe, practical maintenance. Real-world savings and emissions depend on location, weather, tariffs, and the electricity grid.
- **Theme:** dark by default, with a manual light-mode switch.

## Run locally

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

Open the local URL printed by Streamlit, normally `http://localhost:8501`.

## Deploy on Streamlit Community Cloud

The app source is in the public GitHub repository. To create a public live demo:

1. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/) and authorize access to GitHub.
2. Select `shivnandan225/Solar-Energy-Optimization-and-_Panel-Health-Monitor`.
3. Select the `shivnandan225-solar-energy-platform` branch.
4. Set **Main file path** to `app.py` and deploy.
5. After deployment succeeds, copy the app's public `*.streamlit.app` URL and replace the first line of this README with `Live demo: https://YOUR-APP.streamlit.app/`.

The app URL is assigned by Streamlit during deployment; it cannot be safely guessed in advance. The current local preview at `http://localhost:8501` is only accessible on the developer's machine and is not a public demo.

## Making this production-ready

1. **Verified panel diagnostics:** collect consented, expert-labelled panel photos and thermal imagery. Train and evaluate a vision model across different panel types and conditions, show confidence and uncertainty, and refer suspected electrical faults for qualified inspection.
2. **Real AI assistant:** connect an LLM through a server-side API key, ground answers in manufacturer manuals and local safety guidance, cite sources, and provide emergency escalation. Store secrets only in the deployment's secret manager.
3. **Live hardware monitoring:** connect supported inverter APIs or a certified sensor gateway with authentication, timestamps, unit validation, and manufacturer-specific alert thresholds.
4. **Persistent service reports:** add authentication, a secure database and image storage, retention controls, notifications, technician assignment, and request-status tracking. Obtain user consent before sharing contact details or photos.
5. **Technician network:** verify local providers, coverage, and qualifications before enabling booking or dispatch.
6. **Accurate optimization:** add location-aware weather forecasts, utility tariffs, actual inverter history, and local grid emissions factors.

## Safety and privacy

This is an educational demonstration, not a certified inspection or electrical repair guide. Never open, touch, or attempt to repair live solar equipment. If there is smoke, fire, electric shock, sparks, or exposed wiring, stay away and contact emergency services or a licensed solar electrician. Do not upload sensitive personal information. Demo reports are held in session memory and may disappear when the session ends.
