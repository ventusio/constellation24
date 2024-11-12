# constellation24
Repo for GitHub Constellation 2024 Hackathon

# What we're building
Feather is a community-driven platform that empowers South Africans to enhance their safety through collective awareness. The platform allows citizens to:

- Report incidents anonymously to build a comprehensive crime map
- Visualize crime patterns and hotspots in their neighborhoods
- Access safety information in their preferred local language
- Make informed decisions about travel routes and daily activities

Our mission is to transform raw incident data into actionable safety intelligence that helps communities stay informed and protected. By combining real-time reporting with geospatial visualization, we're creating a tool that serves both individuals and law enforcement in their efforts to improve public safety.

## Goals
- [ ] Create a platform for people to report crime, anonymously
- [ ] Visualize data on a map
- [ ] Provide some way for users to chat with the app - focus on SA langauges
- [ ] _Stretch Goal_ Pull in data from other sources (e.g. police reports)
- [ ] _Stretch Goal_ Provide navigation to the nearest police station
- [ ] _Stretch Goal_ Provide navigation, taking crime data into account

## Pillars
### Community
- Built by and for South African communities
- Encourages active citizen participation and reporting
- Supports multiple languages to reach all community members
- Promotes collective responsibility for safety
### Safety
- Real-time incident reporting and alerts
- Crime pattern visualization and hotspot identification
- Privacy-focused design protecting user identities
### Intelligence
- AI-powered language processing for local language support
- Data-driven insights for informed decision-making

# How we're building it
## Tech Stack
![Architecture](architecture.drawio.png)
1. Front-end: Streamlit (Python)
2. Back-end: FastAPI (Python)
3. Database: PostGIS (PostgreSQL on Docker)
4. Maps: OpenStreetMaps (through Leaflet.js/Folium)
5. Intelligence: (Meta Llama 3.2 on Together.ai)

### Architectural Decisions
*Why seperate frontend and backend?*

Decoupling the frontend and backend allows for more flexibility in the future.
For example, we could build a mobile app that uses the same backend.
Streamlit is great for prototyping and building dashboards, and it allowed us to move fast.
However, for a "real" web app, we would probably use a more traditional frontend framework like React.

*Why Postgres/PostGIS?*

We are storing geospatial data, so we need a database that can handle that.
Postgres is a great database, and PostGIS is an extension that adds geospatial functionality.

*Why Llama & Together.ai?*

Llama is _the_ premier open source family of AI models.
With it being open source, we can easily fine-tune it to better understand South African languages.
Together.ai provides a complete free tier for Llama 3.2 11B.
The alternative would be Google Gemini, which has a generous free tier.

## Open Source
## Quality and Security
## AI Tools
Due to the time constraints, and being busy with "real life", we relied heavily on GitHub copilot during the development.
We used it for the following purposes:

- Ideation - fleshing out ideas
- Scaffolding - creating the initial structure of the project
- Editing - making small changes to code
- Testing - writing tests

# Local Dev
## Prerequisites
- Docker
- Python 3.12+

## Setup
1. Clone the repo
2. Set up the Python environment
```bash
python -m venv .venv
source .venv/bin/activate
```
3. Install the dependencies
```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
pip install -r shared/requirements.txt
```
4. Install shared lib as an editable package
```bash
pip install -e shared
```
5. Run `docker-compose up -d` to start the database
6. Run the backend
```bash
fastapi run backend/src/main.py
```
7. Run the frontend
```bash
streamlit run frontend/src/main.py
```

### Executing Tests
```bash
pytest backend/tests
```