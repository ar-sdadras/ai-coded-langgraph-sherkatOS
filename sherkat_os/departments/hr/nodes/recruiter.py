import json
from langchain_core.messages import AIMessage, ToolMessage
from sherkat_os.departments.hr.state import HRState
from sherkat_os.services.logger import logger

async def hr_recruiter_node(state: HRState) -> HRState:
    messages = state.get("messages", [])
    
    # If last message is a ToolMessage, process the salary benchmarking output
    if messages and isinstance(messages[-1], ToolMessage):
        tool_msg = messages[-1]
        logger.log_node_start("HR Recruiter", f"Processing tool result: '{tool_msg.content}'")
        
        draft = {
            "headcount": 3,
            "roles": [
                {
                    "title": "Lead Backend & Agent Engineer",
                    "dept": "Engineering",
                    "exp": 5,
                    "skills": ["Python", "FastAPI", "LangGraph"],
                    "salary": "$130k - $150k"
                },
                {
                    "title": "Senior Frontend Developer",
                    "dept": "Engineering",
                    "exp": 4,
                    "skills": ["React", "Next.js", "TailwindCSS"],
                    "salary": "$110k - $130k"
                }
            ],
            "benchmark_data": tool_msg.content
        }
        
        return {
            **state,
            "hr_draft": draft,
            "messages": [AIMessage(content="Staffing plan requirements drafted after role salary benchmarking.")]
        }
        
    else:
        # First call: Emit a tool call for custom salary benchmarking tool
        logger.log_node_start("HR Recruiter", "Benchmarking salary for Lead Agent Engineer role...")
        
        tool_call = {
            "name": "benchmark_salary_by_role",
            "args": {"role_title": "Lead Backend & Agent Engineer", "experience_years": 5},
            "id": "salary_bench_01",
            "type": "tool_call"
        }
        
        return {
            **state,
            "messages": [AIMessage(content="", tool_calls=[tool_call])]
        }
