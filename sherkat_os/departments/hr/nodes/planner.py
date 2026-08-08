import json
from langchain_core.messages import AIMessage
from sherkat_os.departments.hr.state import HRState
from sherkat_os.services.logger import logger

async def hr_planner_node(state: HRState) -> HRState:
    logger.log_node_start("HR Planner", "Formatting staffing roadmap and milestones...")
    
    draft = state.get("hr_draft") or {}
    
    hr_plan = {
        "total_headcount_target": draft.get("headcount", 3),
        "roles_list": [
            {
                "title": role["title"],
                "department": role["dept"],
                "years_experience_required": role["exp"],
                "core_skills": role["skills"],
                "target_salary_range_usd": role["salary"]
            } for role in draft.get("roles", [])
        ],
        "hiring_timeline_description": "First 4 weeks: Engineer sourcing. Next 2 weeks: Onboarding.",
        "recruitment_milestones": [
            {"milestone_name": "Source Lead Agent Engineer", "estimated_weeks_to_fill": 4, "priority": "Critical"},
            {"milestone_name": "Source Next.js Specialist", "estimated_weeks_to_fill": 3, "priority": "High"}
        ]
    }
    
    if state.get("critic_feedback"):
        logger.log_node_start("HR Planner", f"Refining staffing plan based on critic feedback: '{state['critic_feedback']}'")
        hr_plan["roles_list"].append({
            "title": "Part-time UI/UX Designer",
            "department": "Design",
            "years_experience_required": 3,
            "core_skills": ["Figma", "Design Systems"],
            "target_salary_range_usd": "$40k - $60k"
        })
        hr_plan["total_headcount_target"] += 1
        
    msg = AIMessage(content=f"Generated HR plan: {json.dumps(hr_plan)}")
    return {
        **state,
        "hr_plan": hr_plan,
        "messages": [msg]
    }
