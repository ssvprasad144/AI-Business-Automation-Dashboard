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