# KICS2026-Group2

I2NSF policy generator combining a Python backend (LLM-driven XML policy synthesis and validation) with a Next.js web UI for interactive intent collection and display of generated policies.

## Repository Layout
- llm_backend/: Python policy generator, XML schema, validation utilities, and sample outputs.
- packages/ui/: Next.js 16 web client that calls the backend through an API route.
- benchmark_results/, benchmark_plots/: Generated policies and evaluation artifacts.

## System Requirements
- Python 3.10+ with pip
- Node.js 18+ (Next.js 16 requires Node 18.18+), npm
- OpenAI API key with access to GPT-4o (or equivalent reasoning-capable model)
- macOS, Linux, or Windows (WSL recommended on Windows for Python tooling)

## Backend Setup (Python)
1) From the repo root, enter the backend directory:
```bash
cd llm_backend
```
2) Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```
3) Install dependencies:
```bash
pip install openai pydantic lxml rich
```
4) Add your OpenAI API key to a token file in llm_backend (and keep it git-ignored):
```bash
echo "your-openai-api-key-here" > token
```
5) Smoke test the generator:
```bash
python generate.py "Block all SSH traffic from untrusted networks"
```
On success, generated_policy.xml is written in llm_backend and validation output prints to the console.

## Frontend Setup (Next.js)
1) From the repo root, enter the UI app:
```bash
cd packages/ui
```
2) Install Node dependencies:
```bash
npm install
```
3) Start the dev server:
```bash
npm run dev
```
The UI runs at http://localhost:3000 (Next.js will offer an alternate port if 3000 is busy).

## Run End-to-End
- Terminal 1 (frontend):
```bash
cd packages/ui
npm run dev
```
- Terminal 2 (backend availability): Ensure the llm_backend venv is prepared and python3 can run generate.py. The API route [packages/ui/src/app/api/generate/route.ts](packages/ui/src/app/api/generate/route.ts#L1-L41) invokes generate.py via child_process and reads generated_policy.xml.
- Open http://localhost:3000 and submit intents through the chat interface; responses include the generated XML policy.

## Example Intents
- Block social media during work hours Monday to Friday
- Allow VPN access only from United States and Canada
- Mitigate DDoS attacks with rate limiting of 10000 packets per second
- Block all traffic from China to government servers between 9 AM and 5 PM

## Command-Line Backend Usage
Useful for batch runs or debugging without the UI:
```bash
cd llm_backend
source venv/bin/activate      # Windows: venv\Scripts\activate
python generate.py "Whatever security policy intent - high level"
```
The resulting policy is saved to generated_policy.xml and validation feedback is printed.

## Troubleshooting
- Python module not found: Activate the venv and reinstall deps: `source venv/bin/activate` then `pip install openai pydantic lxml rich`.
- API authentication error: Ensure llm_backend/token exists and contains a valid key with no extra whitespace.
- Frontend cannot execute backend: Confirm the backend path in [packages/ui/src/app/api/generate/route.ts](packages/ui/src/app/api/generate/route.ts#L14-L22) is correct for your clone and that python3 is on PATH (use python on Windows if python3 is unavailable).
- Port already in use: Run with a custom port, e.g. `npm run dev -- -p 3002`.
