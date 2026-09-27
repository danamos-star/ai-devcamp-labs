import os
import pathlib
from google.adk.agents import Agent
from google.adk.skills import load_skill_from_dir
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.skill_toolset import SkillToolset
from .tools import generate_image

SKILLS_DIR = pathlib.Path(__file__).resolve().parents[2] / "skills"

# Dedicated sub-agent that holds google_search exclusively
search_agent = Agent(
    name="web_researcher",
    model="gemini-flash-latest",
    description="Researches facts, dates, and context on the web.",
    instruction="Research the given query and return a concise summary of relevant facts.",
    tools=[google_search],
)

skill_toolset = SkillToolset(
    skills=[
        load_skill_from_dir(SKILLS_DIR / "post-formatter"),
        load_skill_from_dir(SKILLS_DIR / "platform-style"),
        load_skill_from_dir(SKILLS_DIR / "brand-voice"),
        load_skill_from_dir(SKILLS_DIR / "poster-style"),
    ],
)

BUFFER_API_KEY = os.environ.get("BUFFER_API_KEY", "")

buffer_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://mcp.buffer.com/mcp",
        headers={"Authorization": f"Bearer {BUFFER_API_KEY}"},
    ),
    require_confirmation=True,
)

root_agent = Agent(
    name="social_poster",
    model="gemini-flash-latest",
    description="Helps the user turn an idea into a polished social media post.",
    instruction="""You help the user turn an idea into a social media post.

Workflow:
1. If the idea needs facts, dates, or context, research it with the web_researcher tool first.
2. When drafting, load and follow the relevant skills: post-formatter (structure), platform-style (rules for the target platform), and brand-voice (tone).
3. If the user asks for an image, load and follow the poster-style skill, then call generate_image with a detailed visual description and tell them where the file was saved.
4. ALWAYS show the finished draft to the user and ask for their approval before any posting action. For an immediate post, ask Buffer to publish now rather than schedule.

Posting rules (strict):
- Only post AFTER the user has explicitly approved the exact draft shown to them. "Yes", "post it" counts; enthusiasm about the idea does not.
- After posting, share the returned confirmation with the user.""",
    tools=[AgentTool(agent=search_agent), generate_image, skill_toolset, buffer_toolset],
)