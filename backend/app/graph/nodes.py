import asyncio

from app.config import settings
from app.graph.state import AgentState
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.output_parsers import JsonOutputParser
from app.schema.ReviewerOutput import ReviewerOutput
from openai import OpenAI
from app.helpers.helpers import generate_image_sync
from app.services.generate_image_sync import generate_image_sync

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI



openai_image_client = OpenAI(api_key=settings.openai_api_key)

llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.openai_api_key)
dalle = DallEAPIWrapper(
    api_key=settings.openai_api_key, model="gpt-image-1-mini", size="auto"
)

# --- PROMPT TEMPLATES ---

strutturazione_prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""# Persona
Sei un tech writer senior specializzato in contenuti per sviluppatori.

# Task
Analizza l'idea tecnica e strutturala per un post LinkedIn.

# Context
Pubblico: sviluppatori, tech lead, CTO.
Idea: {user_input}

# Format
Rispondi SOLO con:
CONCETTO PRINCIPALE: (1 frase)
PUNTI CHIAVE:
- (max 4 bullet concreti)
ESEMPIO PRATICO: (1 caso reale)
MESSAGGIO FINALE: (1 frase, il takeaway)""",
)

scrittore_prompt = PromptTemplate(
    input_variables=["structured_info"],
    template="""# Persona
Sei un copywriter tecnico esperto di LinkedIn, tono diretto e mai pomposo.

# Task
Scrivi un post LinkedIn che generi engagement tra sviluppatori.

# Context
- Pubblico: sviluppatori, tech lead, CTO
- Tono: tecnico ma accessibile, no buzzword, esempi concreti
- Hook: domanda o affermazione forte in apertura
- Emoji: max 3-4, solo dove aggiungono valore
- Lunghezza: 150-250 parole
- Struttura: hook → bullet brevi → call to action

Topic:
{structured_info}

# Format
Scrivi SOLO il testo del post, inizia direttamente con l'hook.""",
)

revisore_prompt = PromptTemplate(
    input_variables=["post_text", "format_instructions"],
    template="""# Persona
Sei un editor senior specializzato in personal branding tecnico su LinkedIn.

# Task
Valuta la qualità del post e fornisci feedback actionable.

# Context
- Pubblico target: sviluppatori, tech lead, CTO
- Criteri: hook forte, no buzzword, max 4 emoji, tono tecnico ma accessibile, 150-250 parole
- Il campo "esito" deve essere ESCLUSIVAMENTE "APPROVATO" oppure "DA_RIVEDERE", nessun altro valore

POST DA VALUTARE:
{post_text}

# Format
{format_instructions}"""
)


revisore_parser = JsonOutputParser(pydantic_object=ReviewerOutput)

# --- CHAINS ---

strutturazione_chain = strutturazione_prompt | llm
scrittore_chain = scrittore_prompt | llm

# --- NODI ---


async def strutturazione_node(state: AgentState) -> dict:
    print("STRUTTURAZIONE - avviato")
    response = await strutturazione_chain.ainvoke({"user_input": state["user_input"]})
    print("STRUTTURAZIONE - completato")
    return {"structured_info": response.content}

async def scrittore_node(state: AgentState) -> dict:
    print("SCRITTORE - avviato")
    response = await scrittore_chain.ainvoke({"structured_info": state["structured_info"]})
    print("SCRITTORE - completato")
    return {"post_text": response.content}

# DA IMPLEMENTARE QUANDO SI é SICURI CHE FUNZIONA - GENERAZIONE IMMAGINI CONSUMA CREDITO
# async def diagrammatore_node(state: AgentState) -> dict:
#     style_prompt = """Minimal SaaS workflow diagram, Linear/Notion style.
# White background, monochrome, blue accent #0070F3, rounded rectangles, thin arrows, clean spacing.
# No gradients, no shadows, no futuristic imagery."""
# 
#     full_prompt = f"{style_prompt} Technical workflow: {state['structured_info'][:200]}. Max 5 nodes, short labels, arrows."
# 
#     loop = asyncio.get_event_loop()
#     image_url = await loop.run_in_executor(None, generate_image_sync, full_prompt)
#     return {"image_url": image_url}

async def diagrammatore_node(state: AgentState) -> dict:
    
    # TODO: implementare generazione immagine reale
    return {"image_url": "https://placehold.co/1024x1024"}


async def revisore_node(state: AgentState) -> dict:
    revisore_chain = revisore_prompt | llm | revisore_parser

    result = await revisore_chain.ainvoke(
        {
            "post_text": state["post_text"][:300],
            "format_instructions": revisore_parser.get_format_instructions(),
        }
    )

    review_notes = f"ESITO: {result['esito']}\nFEEDBACK: {result['feedback']}"
    return {"review_notes": review_notes}
