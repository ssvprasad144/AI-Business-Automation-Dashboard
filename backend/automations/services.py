import os
from openai import OpenAI

def generate_workflow_suggestion(description):
    api_key=os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"configured":False,"message":"Add OPENAI_API_KEY to enable AI workflow suggestions."}
    client=OpenAI(api_key=api_key)
    response=client.responses.create(
        model=os.getenv("OPENAI_MODEL","gpt-5-mini"),
        input=f"""You are an automation architect. Turn this business process into a concise workflow proposal.
Business process: {description}
Return a workflow name, trigger, three action steps, and expected business value."""
    )
    return {"configured":True,"proposal":response.output_text}

def run_lead_demo(enquiry):
    """Sandboxed portfolio demo: no email, CRM, or external side effects."""
    api_key=os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            client=OpenAI(api_key=api_key)
            response=client.responses.create(
                model=os.getenv("OPENAI_MODEL","gpt-5-mini"),
                input=f"""Analyze this fictional sales enquiry for a live portfolio demo.
Return JSON with keys: category, priority, needs, suggested_response.
Enquiry: {enquiry}"""
            )
            return {"mode":"ai","workflow":"Lead Qualification Demo","input":enquiry,"result":response.output_text}
        except Exception:
            pass
    text=enquiry.lower()
    hot_terms=["urgent","asap","buy","pricing","quote","hire","deadline","ready"]
    priority="High" if any(term in text for term in hot_terms) else "Medium"
    category="Website / software enquiry" if any(term in text for term in ["website","app","software","crm","automation"]) else "General enquiry"
    return {
        "mode":"sandbox",
        "workflow":"Lead Qualification Demo",
        "input":enquiry,
        "result":{
            "category":category,
            "priority":priority,
            "needs":["Clarify requirements","Confirm timeline","Confirm budget"],
            "suggested_response":"Thanks for reaching out. I can help clarify the requirements and propose the next steps."
        }
    }
