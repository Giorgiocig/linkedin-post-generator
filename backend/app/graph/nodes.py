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

llm = ChatOpenAI(model="gpt-4o", api_key=settings.openai_api_key)
dalle = DallEAPIWrapper(
    api_key=settings.openai_api_key, model="gpt-image-1-mini", size="auto"
)

# --- PROMPT TEMPLATES ---

strutturazione_prompt = PromptTemplate(
    input_variables=["user_input", "user_context"],
    template="""# Persona
Sei un tech writer senior specializzato in contenuti per sviluppatori.

# Task
Analizza l'idea tecnica e strutturala per un post LinkedIn.

# Context
Pubblico: sviluppatori, tech lead, CTO.
Lingua: inglese.
Idea: {user_input}
Contesto personale dell'autore: {user_context}

# Format
Rispondi SOLO con:
CONCETTO PRINCIPALE: (1 frase)
PUNTI CHIAVE:
- (max 4 bullet concreti, basati sul contesto reale se disponibile)
ESEMPIO PRATICO: (usa il contesto personale se disponibile, altrimenti generalizza senza inventare dati)
MESSAGGIO FINALE: (1 frase, il takeaway)"""
)
#PTC abbandonato
scrittore_prompt = PromptTemplate(
    input_variables=["structured_info", "user_context"],
     template="""Write a LinkedIn post in English for software developers and tech leads.

Follow EXACTLY the style of these examples — short sentences, direct insights, no metaphors, no fluff:

# Esempi di post di alta qualità

ESEMPIO 1:
Most automation projects don't fail because the AI is wrong.

They fail because nobody defines who decides what. 👇

I've seen this pattern repeatedly in real implementations.

A workflow gets designed like this:

A request arrives.

The system classifies it.

The AI suggests an action.

And then… everything slows down.

Because one critical question was never answered:

Who is responsible for approving or overriding that decision?

In most cases, the answer is unclear from the start.

Teams assume "the system will handle it".

But automation doesn't remove decision-making.

It redistributes it.

Without clear ownership, every edge case becomes a bottleneck. 

What should have been an automated flow turns into a hidden approval queue.

The missing piece isn't more intelligence.

It's explicit decision routing.

Defining what runs automatically, what requires human approval, and what escalates immediately,  before the system goes live, not after the first failure.

Once that's defined, systems stop collapsing under ambiguity.

Automation works best when decision boundaries are explicit, not implicit.

Where in your workflows do decisions still have no clear owner?

#AIIntegration #Automation #WorkflowDesign #AIEngineering

ESEMPIO 2:
Most people think automation reduces work. 👇 

In many cases, it reduces waiting.

That's a very different thing.

When I analyze business processes, the biggest bottleneck is rarely the task itself.

It's what happens between tasks.

A customer submits a request.

Then it sits in an inbox.

Someone eventually reviews it.

Then it waits for approval.

Then it waits to be assigned.

Then it waits for another system to be updated.

The actual work might take 10 minutes.

The process takes 3 days.

This is why the most effective AI automations I've built weren't replacing experts.

They were eliminating the gaps between decisions.

Routing requests.
Updating systems.
Triggering the next action automatically.

The value doesn't come from doing work faster.

It comes from removing the idle time that accumulates across a workflow.
That's where most operational inefficiency lives.

When you look at your own processes, what's taking longer: the work itself or the waiting between steps?

#AIAutomation #AIIntegration #WorkflowAutomation #Operations

Esempio 3:
AI isn't struggling with SQL.

It's struggling with context. 👇 

That's something I've noticed while building text-to-SQL systems in production.

A lot of discussions focus on model quality, prompt engineering, or which LLM performs best on benchmarks.

But in many real-world scenarios, the generated SQL is technically correct.
The answer is still wrong.

Why?

Because the model doesn't know how the business defines its metrics.
Ask a simple question like:
"What's our monthly revenue?"

And suddenly you discover that Finance, Sales, and Operations all use slightly different definitions.

The database contains the data.

The SQL retrieves the data.

The missing piece is the business context.

This is why I believe one of the most valuable applications of RAG in text-to-SQL isn't schema retrieval.

It's metric retrieval.

Providing the model with the exact definition of concepts like revenue, active customer, churn, or margin often has a bigger impact than giving it more tables or a larger context window.

In my experience, the biggest source of errors isn't hallucination.

It's ambiguity.

And text-to-SQL systems expose that ambiguity very quickly.

Have you seen the same issue when deploying AI on top of business data?

what's been the biggest challenge — schema complexity, business definitions, or something else?

#TextToSQL #RAG #AIIntegration #DataAnalytics

ESEMPIO 4:
AI isn't creating data problems.

It's exposing the ones that were already there. 👇

I've seen this while building text-to-SQL systems.

People often assume the hard part is generating SQL.

But modern LLMs are already pretty good at that.

The real challenge starts when someone asks:
"Show me our revenue."

Sounds simple.

Until you realize:
• Finance and Sales define revenue differently
• Teams use different business terminology
• Metrics live in spreadsheets, dashboards and people's heads
• Nobody documented the assumptions

The SQL can be perfectly correct.

And the answer can still be wrong.

That's why I think one of the biggest impacts of AI analytics isn't automation.

It's forcing companies to clarify how they actually define their business.

In a strange way, text-to-SQL is becoming a governance stress test.

Because the moment people can ask questions directly to their data, every inconsistency becomes visible.

The AI isn't hallucinating.

It's exposing ambiguity that was already there.

Curious if others working with analytics or AI data tools are seeing the same thing 👀

#TextToSQL #DataAnalytics #LLMApplications #DataGovernance

ESEMPIO 5:
Most organizations don't have a document problem. 

They have a synthesis problem. 👇

The information is already there. 

• Contracts. 
• Technical reports. 
• Internal documentation. 
• Project files.

The challenge isn't finding it. 
It's making sense of it all at once.

When information is spread across dozens of documents, teams often end up doing it manually:

•comparing documents side by side
•searching for relevant sections
•copying information into spreadsheets
•building summaries by hand

That's hours of work before any actual analysis begins.

So I built a multi-document analysis workflow for complex, document-heavy dossiers.

The system reads the dossier, connects relevant information across documents, and returns structured findings ready for review.

Not "chat with your PDFs".

Structured extraction from fragmented, real-world documentation.

The bottleneck in document-heavy workflows isn't access to information. It's the time it takes to turn information into something actionable.

Demo below 👇

#DocumentAI hashtag#WorkflowAutomation hashtag#RAG hashtag#LLMApplications

Esempio 6:
RAG isn't a chatbot feature. It's infrastructure. 👇

Most implementations don't fail at retrieval. They fail at everything retrieval can't solve alone.

I've seen this while building RAG systems around contracts, reports and internal documentation.

The demo is always the same: upload documents, ask a question, get an answer. Clean. Fast. Impressive.

But then someone asks a question that spans three documents. 
Or the answer depends on context from six months ago. Or two sources contradict each other and the system has to decide which one to trust.

That's where most RAG systems quietly fall apart.

Because the hard part was never "can we retrieve the right chunk?"

It's:
which information actually matters in this context
how to handle contradictions across sources
how to ground answers without hallucinating connections
how to make the output something a human can actually act on

The shift I keep seeing is this: RAG is moving away from "chat with your documents", and toward structured reasoning over information.

Less Q&A interface. More decision-making layer.

That's a fundamentally different product to build. And a much more interesting one.

Curious how others are pushing RAG beyond basic retrieval 👀

#RAG #DocumentAI #LLMApplications #AIEngineering


Rules:
- English only
- Short sentences, fast rhythm
- First person, real experience
- No invented data or statistics
- Max 2 emoji
- 3-4 hashtags at the end
- End with a genuine question

Author context: {user_context}

Topic: {structured_info}

Write ONLY the post. Start directly with the hook."""
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
    response = await strutturazione_chain.ainvoke({
        "user_input": state["user_input"],
        "user_context": state.get("user_context") or ""
    })
    return {"structured_info": response.content}

async def scrittore_node(state: AgentState) -> dict:
    response = await scrittore_chain.ainvoke({
        "structured_info": state["structured_info"],
        "user_context": state.get("user_context") or ""
    })
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
