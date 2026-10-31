# Social Spark

An AI agent that turns an idea into a finished social post. It researches the web, drafts in your brand voice, generates an image, **waits for your approval**, and then publishes through Buffer or LinkedIn. It is the running project for the GDG London **Agentic DevCamp**: you build it in Lab 1.

> **Start here:** [Setup guide](docs/setup-guide.html) (do this before Saturday) → [Lab 1: Build](docs/lab-1-build.html). All docs are listed in [docs/index.html](docs/index.html).
>
> This repo is the finished reference, not step 1. In Lab 1 you build a smaller version of it yourself. Use this repo when you get stuck or want to see where the labs end up.

## How it works

<img src="docs/img/architecture-build.png" alt="The social_poster orchestrator takes your idea, uses skills, an image tool and a research sub-agent, shows a draft, and only publishes through Buffer or LinkedIn after you approve" width="800">

You give the **orchestrator** (`social_poster`) an idea. It loads **Agent Skills** for your brand voice, calls a **research sub-agent** for facts and an **image tool** for a picture, then shows you the draft. Nothing is published until you press approve. The approval gate is enforced by the framework, not by a polite instruction the model could ignore.

## Tech stack

| Layer | What we use | Why |
|---|---|---|
| Agent framework | [Google ADK](https://google.github.io/adk-docs/) (Python) | Agents, tools, sub-agents, sessions, evals |
| Models | Gemini (`gemini-flash-latest`, Gemini image model) | Reasoning, drafting, image generation |
| Agent knowledge | Agent Skills (`skills/`) | Brand voice as a reviewable markdown folder |
| Publishing | MCP servers: Buffer (remote), LinkedIn (optional, stdio) | Real posts behind a human approval gate |
| Agent-to-agent | A2A (`memory_agent`, optional) | A separate memory service the orchestrator can ask |
| Backend | FastAPI + [`ag-ui-adk`](https://github.com/ag-ui-protocol/ag-ui) | Serves the agent to the UI over AG-UI at `/api/adk` |
| Frontend | Next.js 16, React 19, [CopilotKit](https://copilotkit.ai) | Chat, draft preview and the approve button |
| Data | SQLite (local), Cloud Storage (optional images) | Post history and hosted images |
| Tooling | `uv`, `agents-cli`, `adk eval`, `gcloud` | Install, deploy, quality gate |

## What you build, lab by lab

| Session | Lab | You add | Tag to check out if you fall behind |
|---|---|---|---|
| Setup | [Setup guide](docs/setup-guide.html) | Google Cloud project, tools, coding agent | `starter` |
| 1. Build | [Lab 1](docs/lab-1-build.html) | The agent, skills, tools, approval gate, web UI | `pillar-build` |

```bash
git checkout pillar-build   # for example: the finished result of Lab 1
```


## Run it locally

You need [uv](https://docs.astral.sh/uv/), Node.js 20+, and a Google Cloud project (see the [setup guide](docs/setup-guide.html)). From the repo root:

```bash
cp .env.example backend/social_poster/.env   # set GOOGLE_CLOUD_PROJECT
uv sync
./run-backend.sh                             # terminal 1: http://localhost:8000
./run-frontend.sh                            # terminal 2: http://localhost:3000
```

Publishing is a dry run (`DRY_RUN=true`) until you switch it off, so nothing goes to a real account by accident. More detail: [backend/README.md](backend/README.md) and [frontend/README.md](frontend/README.md).

## What's where

```
backend/social_poster/   the agents, tools and guardrails (agent.py is the place to start)
backend/main.py          FastAPI app: AG-UI route, sessions and memory when deployed
skills/                  Agent Skills (brand voice)
frontend/                Next.js + CopilotKit UI
evals/                   adk eval sets (quality and governance)
docs/                    labs, setup guide, deploy and reference docs
gcp-setup.sh             one-time Google Cloud setup: APIs, templates, grants
```

## Reference docs

| Doc | Covers |
|---|---|
| [LEARNINGS.md](docs/LEARNINGS.md) | What broke and why, by pillar |

## Lab 2 - Scale screenshots

1. Deployment on Agent Runtime
   <img width="1423" height="441" alt="image" src="https://github.com/user-attachments/assets/842e1523-d43b-420a-9fd2-a2d67cb5a9b3" />

2. AG-UI server-sent event stream showing live agent execution, pipeline state updates, tool calls, and model response
   <img width="1095" height="609" alt="image" src="https://github.com/user-attachments/assets/9b9f3f5e-89f9-4872-8d13-78e444d7adea" />

3. Agent Sessions
   <img width="1420" height="491" alt="image" src="https://github.com/user-attachments/assets/ab310e6d-51f8-458e-b366-f63f69c6f73d" />

4. Memory extraction and recall
   <img width="1098" height="768" alt="image" src="https://github.com/user-attachments/assets/41d68f28-dfd1-4558-946b-34af0ae60995" />

   <img width="1110" height="679" alt="image" src="https://github.com/user-attachments/assets/d33cc1f9-6bf0-4d3d-8572-f1a1a134d4aa" />

   <img width="1878" height="659" alt="image" src="https://github.com/user-attachments/assets/89793b2e-8dcc-45e7-aa54-765cea3bb7ac" />

   <img width="1795" height="664" alt="image" src="https://github.com/user-attachments/assets/48bbaeb4-9a8e-42ab-b73f-b899b85a5e49" />


5. Full-Stack orchestration and Human-in-the-loop approval:
   <img width="1870" height="895" alt="image" src="https://github.com/user-attachments/assets/449836e6-5bfd-4c09-8095-41917ff0f13a" />

   <img width="1577" height="818" alt="image" src="https://github.com/user-attachments/assets/e71c41bb-da53-49bc-862f-f78975f20231" />

6. Frontend Cloud Run deployment
   <img width="1093" height="505" alt="image" src="https://github.com/user-attachments/assets/4a154c9e-86e8-430a-a41e-8065dfe800b9" />

7. Reasoning Engine observability
   <img width="1096" height="686" alt="image" src="https://github.com/user-attachments/assets/4569284c-1df1-4a8e-b314-2813bcb3283c" />

8. Environment clean-Up and teardown verification
   
   <img width="601" height="279" alt="image" src="https://github.com/user-attachments/assets/e199fb67-e53c-4fc8-a8dd-e3ae540886d4" />

## Lab 3 - Govern screenshots

1. Model Armor guardrail actively caught prompt injection attempt

   <img width="583" height="433" alt="image" src="https://github.com/user-attachments/assets/9100f35a-0cb0-4c6e-afde-69536fc2e1fe" />

2. Automated evaluation pass results: confirms the agent successfully blocks prompt injections in automated testing

   <img width="814" height="186" alt="image" src="https://github.com/user-attachments/assets/cd38ac59-b524-4692-a14e-e937c610be0b" />

3. Cloud DLP in action

   <img width="791" height="662" alt="image" src="https://github.com/user-attachments/assets/33c578c6-73a5-4a09-85c9-7139b8066586" />

4. Agent Registry and MCP Capabilities & Discovery

   <img width="828" height="242" alt="image" src="https://github.com/user-attachments/assets/d12fec06-ca60-4ab1-bad7-343030638c95" />

5. Policy creation

   <img width="1169" height="225" alt="image" src="https://github.com/user-attachments/assets/002807ef-baa6-40ee-b37d-3e6264abcc31" />

   <img width="1353" height="625" alt="image" src="https://github.com/user-attachments/assets/1c20e1de-6456-4c6c-abfb-13b0b0f32c40" />

6. Gateway-Level enforcement

   <img width="1049" height="250" alt="image" src="https://github.com/user-attachments/assets/848202f5-30ce-46ce-b6ff-a696725b8cf4" />

   <img width="1332" height="668" alt="image" src="https://github.com/user-attachments/assets/f05c0fb4-efc7-4d64-9079-8c94be23be54" />


## Lab 4 - Optimise screenshots

1. Golden Evaluation Gate Pass

   <img width="690" height="304" alt="image" src="https://github.com/user-attachments/assets/a645afea-42f7-4564-9259-2addcfc8e0a7" />

   <img width="691" height="237" alt="image" src="https://github.com/user-attachments/assets/e2446b7e-99fc-4648-8a30-a266953d938d" />

2. BigQuery Agent analytics output

   <img width="885" height="412" alt="image" src="https://github.com/user-attachments/assets/818c3462-6e07-4737-b5e4-92cfc428ff1b" />

3. Eval-Gate Proof (Red vs. Green / Fail Closed)

   <img width="892" height="180" alt="image" src="https://github.com/user-attachments/assets/86a70569-0eec-41cd-b8c1-dca0ea99bfeb" />

4. Model comparison / latency and cost optimization matrix

   <img width="800" height="489" alt="image" src="https://github.com/user-attachments/assets/8c218f0f-d913-4d98-a383-2c0dc2a3eb55" />

   

   

























