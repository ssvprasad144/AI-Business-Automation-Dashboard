import json
import os
from openai import OpenAI

def _client():
    key=os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=key) if key else None

def _model():
    return os.getenv("OPENAI_MODEL","gpt-5-mini")

def _ai_text(instruction, fallback):
    client=_client()
    if not client:
        return fallback
    try:
        response=client.responses.create(model=_model(),input=instruction)
        return response.output_text
    except Exception:
        return fallback

def _parse_workflow(raw):
    try:
        value=json.loads(raw)
        if isinstance(value,dict) and isinstance(value.get("steps"),list):
            steps=[]
            for step in value["steps"][:6]:
                if isinstance(step,dict):
                    steps.append({"name":str(step.get("name","Workflow step"))[:160],"action_type":step.get("action_type","transform") if step.get("action_type") in {"ai","transform","webhook","email","log"} else "transform"})
            if steps:
                return {"workflow_name":str(value.get("workflow_name","AI-assisted workflow"))[:160],"trigger":str(value.get("trigger","Manual trigger"))[:200],"steps":steps,"business_value":str(value.get("business_value","Automate repetitive processing."))}
    except Exception:
        pass
    return None

def generate_workflow_suggestion(description):
    fallback={
        "workflow_name":"AI-assisted business workflow",
        "trigger":"Manual or form submission",
        "steps":[
            {"name":"Understand request","action_type":"ai"},
            {"name":"Prepare business action","action_type":"transform"},
            {"name":"Record result","action_type":"log"}
        ],
        "business_value":"Reduce repetitive manual processing and create a consistent execution trail."
    }
    client=_client()
    if not client:
        return {"configured":False,"proposal":json.dumps(fallback,indent=2),"workflow":fallback}
    try:
        response=client.responses.create(
            model=_model(),
            input=f"""You are an automation architect. Turn this business process into a concise workflow proposal.
Business process: {description}
Return JSON with keys workflow_name, trigger, steps (three objects with name and action_type using ai, transform, webhook, email, or log), and business_value."""
        )
        parsed=_parse_workflow(response.output_text)\n        return {"configured":True,"proposal":response.output_text,"workflow":parsed}
    except Exception:
        return {"configured":False,"proposal":json.dumps(fallback,indent=2)}

def run_lead_demo(enquiry):
    fallback=_lead_fallback(enquiry)
    text=enquiry.lower()
    client=_client()
    if client:
        try:
            response=client.responses.create(
                model=_model(),
                input=f"""Analyze this fictional sales enquiry for a live portfolio demo.
Return concise JSON with keys: category, priority (Hot/Warm/Cold), intent, needs, suggested_response.
Enquiry: {enquiry}"""
            )
            return {"mode":"ai","workflow":"Lead Qualification Demo","input":enquiry,"result":response.output_text}
        except Exception:
            pass
    return {"mode":"sandbox","workflow":"Lead Qualification Demo","input":enquiry,"result":fallback}

def _lead_fallback(enquiry):
    text=enquiry.lower()
    hot=["urgent","asap","buy","pricing","quote","hire","deadline","ready"]
    warm=["interested","looking","need","planning","explore"]
    priority="Hot" if any(x in text for x in hot) else "Warm" if any(x in text for x in warm) else "Cold"
    category="Website / software enquiry" if any(x in text for x in ["website","app","software","crm","automation"]) else "General enquiry"
    return {"category":category,"priority":priority,"intent":"Potential service enquiry","needs":["Clarify requirements","Confirm timeline","Confirm budget"],"suggested_response":"Thanks for reaching out. I can help clarify the requirements and propose the next steps."}

def run_support_demo(question):
    fallback={
        "intent":"General support",
        "answer":"For this portfolio demo, I can help explain the available automation workflows, demo capabilities, and integration boundaries.",
        "resolution":"Needs human review",
        "source":"Demo knowledge base"
    }
    text=question.lower()
    kb={
        "lead":"The Lead Qualification demo classifies a fictional enquiry and generates a suggested response without sending anything.",
        "email":"The Message Generator creates a preview only; it never sends a real message.",
        "document":"The Data Extraction demo converts supplied text into structured fields for inspection.",
        "integration":"Webhooks, email, AI providers, and CRM/API adapters are prepared as connection points, but public demos have external side effects disabled."
    }
    for key,value in kb.items():
        if key in text:
            fallback["intent"]=f"{key.title()} demo question"
            fallback["answer"]=value
            fallback["resolution"]="Resolved"
            break
    client=_client()
    if client:
        try:
            response=client.responses.create(model=_model(),input=f"""Answer this fictional customer-support question using only this demo knowledge base.
Knowledge base: {json.dumps(kb)}
Question: {question}
Return JSON with keys intent, answer, resolution (Resolved or Needs human review), source.""")
            return {"mode":"ai","workflow":"AI Customer Support Demo","input":question,"result":response.output_text}
        except Exception:
            pass
    return {"mode":"sandbox","workflow":"AI Customer Support Demo","input":question,"result":fallback}

def run_extraction_demo(text):
    fallback={
        "document_type":"Business enquiry",
        "customer_or_company":"Not detected",
        "service":"Not detected",
        "timeline":"Not detected",
        "budget":"Not detected",
        "priority":"Not detected"
    }
    low=text.lower()
    if any(x in low for x in ["website","web app","application","software"]): fallback["service"]="Web / software development"
    if any(x in low for x in ["urgent","asap","deadline"]): fallback["priority"]="High"
    for marker in ["₹","rs ","inr ","$"]:
        if marker in low:
            fallback["budget"]="Budget mentioned in input"
            break
    for word in ["today","tomorrow","week","month","diwali"]:
        if word in low: fallback["timeline"]=word.title()
    client=_client()
    if client:
        try:
            response=client.responses.create(model=_model(),input=f"""Extract structured business-enquiry fields from this text.
Return JSON with keys document_type, customer_or_company, service, timeline, budget, priority. Use "Not detected" when absent.
Text: {text}""")
            return {"mode":"ai","workflow":"AI Data Extraction Demo","input":text,"result":response.output_text}
        except Exception:
            pass
    return {"mode":"sandbox","workflow":"AI Data Extraction Demo","input":text,"result":fallback}

def run_message_demo(purpose,recipient,tone,context):
    fallback=f"Hi,\n\nI’m reaching out regarding {purpose.lower()}. {context.strip()}\n\nPlease let me know a convenient time to discuss the next steps.\n\nBest,\nSSVPrasad"
    client=_client()
    if client:
        try:
            response=client.responses.create(model=_model(),input=f"""Draft a professional business message. Do not claim it was sent.
Purpose: {purpose}
Recipient type: {recipient}
Tone: {tone}
Context: {context}
Return only the message text.""")
            fallback=response.output_text
            return {"mode":"ai","workflow":"AI Message Generator Demo","input":{"purpose":purpose,"recipient":recipient,"tone":tone,"context":context},"result":fallback,"sent":False}
        except Exception:
            pass
    return {"mode":"sandbox","workflow":"AI Message Generator Demo","input":{"purpose":purpose,"recipient":recipient,"tone":tone,"context":context},"result":fallback,"sent":False}
