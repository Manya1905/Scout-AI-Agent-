import os
from anthropic import Anthropic
import json
from pathlib import Path
import uuid
import datetime
import sys

def get_job_info(keyword: str):
    keyword = keyword.lower() # normalize the keyword
    folder = Path("postings") # get filepath to the postings
    results = {}

    for path in folder.glob("*.txt"):
        results[path.name] = []
        text = path.read_text(encoding="utf-8").lower()
        i = 0
        end = len(text)
        # find all instances of the keyword
        while i != -1:
            pos = text.find(keyword, i, end)
            if pos != -1:
                if pos >= 60:
                    results[path.name].append(text[pos-60:pos+61])
                else:
                    results[path.name].append(text[0:pos+61])
                i = pos + len(keyword)
            else: i = -1
    return str(results)

def get_profile():
    # encoding = "utf-8" tells Python which rule to use when turning the file's bytes into characters. UTF-8 is the standard rule modern text uses.
    # It covers every character in every language, including special characters like ● and curly quotes.
    f = open("profile.md", encoding="utf-8")
    profile = f.read()
    f.close()
    return profile

def save_note(job_title: str, note_draft: str):
    print("\n")
    print(job_title)
    print(note_draft)
    return "Draft note printed successfully!"

def get_full_jd(job_title: str):
    path = "Postings/"+ job_title + ".txt"
    f = open(path, encoding="utf-8")
    jd = f.read()
    f.close()
    return jd

tools = [
    {
        "name": "get_job_info",
        "description": "Search all of the user's saved job descriptions to get information about a particular skill or qualification needed for them. Ex: Needing to know PyTorch, Kubernetes, C++, etc. Using this tool will return a dictionary where the key is the filename and the value is a list of snippets containing the keyword from the JD. Note that 1 list corresponds to 1 job description, and a list can have 0, 1 or more snippets in it.  If a key has an empty list, this indicates that the keyword was not in the JD.",
        "input_schema": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "The skill/qualification you want to learn more about. Note, this tool only returns things based on keyword search, so you'll have to be specific about what you want. For instance, you cannot generalize and ask about AI-based skills and expect to get back an answer that talks about knowing LangGraph, how to build harnesses, etc. This is one case insensitive keyword/phrase per call. You'll get back matches or no matches with the keyword \"AI skills\". Example input for tool use: PyTorch. ",
                },
            },
            "required": ["keyword"],
        },
    },

    {
        "name": "get_profile",
        "description": "Use this tool to view the user's profile: this includes her skill set, projects, timelines she's looking for, constraints/notes you should know, etc.",
        "input_schema": {
            "type": "object",
            "properties": {}
        },
    },

    {
        "name": "get_full_jd",
        "description": "Get the full job description of jobs you think the user is best qualified for.",
        "input_schema": {
            "type":"object",
            "properties":{
                "job_title": {
                    "type": "string",
                    "description": "Provide the title the EXACT SAME way it was listed in the get_job_info tool responses. Ex: DoorDash SWE"
                },
            },
            "required": ["job_title"]
        },
    },

    {
        "name": "save_note",
        "description": "Use this tool to return a first-draft message (brief cover note/outreach message) to the employer, grounded in information from the user's profile. This tool will print your first draft. You must title it based on the job posting the note is for.",
        "input_schema": {
            "type": "object",
            "properties":{
                "job_title":{
                    "type": "string",
                    "description": "the job posting that the draft-note is for. Ex: PIMCO Tech Analyst, SWE Draft Note."
                },
                "note_draft":{
                    "type": "string",
                    "description": "Add the actual note you've drafted here. Nothing more, nothing else"
                },
            },
            "required": ["job_title", "note_draft"]
        }
    }
]

run_id = str(uuid.uuid4())
user_query = input("Ask Scout a question: ").strip()

if not user_query:
    print("No question entered... Exiting.")
    sys.exit(1)

record = {"type": "run", "run_id": run_id, "user_query": user_query}


client = Anthropic(
    api_key = os.environ.get("ANTHROPIC_API_KEY")
)

function_dict = {"get_job_info": get_job_info, "get_profile": get_profile, "save_note": save_note, "get_full_jd": get_full_jd}
MAX_TOOL_USE_ITERATIONS = 8
MAX_INPUT_TOKENS = 40000
SYSTEM_PROMPT = "Your role is to help the user find jobs to apply to. Never ask the user clarifying questions - if the question is ambiguous, make a reasonable assumption, state it, and proceed. Always start by using your tools. You have access to the following tools: (1) get_profile: returns the user's resume (skills & experiences. (2) get_job_info: You can do a keyword search on all the jobs uploaded by the user to match skills/see what they are qualified for. (3) get_full_jd to get the complete job description from a job you may have seen parts of from get_job_info. (4) save_note, which prints an outreach message for a job the applicant is suitable for. Everything you say must be grounded in something either the user says or from the tool results. Based on the question asked, you must use these tools as you see fit to answer the user's question. And as a reminder, you CANNOT ask clarifying questions to the user. Note that the output token limit for each turn is 1024 tokens, so keep that in mind as you're writing your final responses."
# saving log
with open(f"Traces/trace{run_id}.jsonl", "a") as f:
    f.write(json.dumps(record) + "\n")

messages = [{"role": "user", "content": user_query}]

started_at = str(datetime.datetime.now())

result = client.messages.create(
    model = "claude-haiku-4-5-20251001",
    max_tokens = 1024,
    system = SYSTEM_PROMPT,
    messages = messages,
    tools = tools,
    tool_choice = {"type": "auto", "disable_parallel_tool_use": True}
)
# log after Claude is called
record = {"type": "call", "run_id":run_id, "turn":0, "started_at": started_at, "ended_at":str(datetime.datetime.now()), "input_tokens": result.usage.input_tokens, "output_tokens": result.usage.output_tokens, "stop_reason": result.stop_reason}

# saving log
with open(f"Traces/trace{run_id}.jsonl", "a") as f:
    f.write(json.dumps(record) + "\n")

curr_input_tokens = 0
i = 0

curr_input_tokens = curr_input_tokens + result.usage.input_tokens

while (result.stop_reason == "tool_use") and (i < MAX_TOOL_USE_ITERATIONS) and (curr_input_tokens <= MAX_INPUT_TOKENS):

    # append Claude's request to the message list
    messages.append({"role": "assistant", "content": result.content})
    print(f"Iteration {i}, no. of input tokens: {result.usage.input_tokens}")

    started_at = str(datetime.datetime.now())

    # Processing the tool_block and setting relevant parameters
    for block in result.content:
        if block.type == "tool_use":
            tool_block = block
            break

    # calling the appropriate function
    if tool_block.name in function_dict:
        args = tool_block.input
        # ** in front of a dict, inside a function call, means: "take each key-value pair out of this dict and pass it as key=value"
        try:
            tool_res = function_dict[tool_block.name](**args)
            print(f"Iteration {i}, calling {tool_block.name} function with the the following parameters: {args}.")

            # log after tool call
            record = {"type": "tool", "run_id":run_id, "turn":i, "tool_name": tool_block.name, "args_json": json.dumps(tool_block.input), "started_at": started_at, "ended_at":str(datetime.datetime.now()), "ok": True, "error_type": None, "error_description": None,  "result_chars": len(str(tool_res))}
            with open(f"Traces/trace{run_id}.jsonl", "a") as f:
                f.write(json.dumps(record) + "\n")

            if i == MAX_TOOL_USE_ITERATIONS-1:
                messages.append({"role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_block.id,
                        "content": tool_res + " This is your last tool use turn, so you'll have to synthesize the final answer with the info you have after this turn. Make it known to the user that you may have ran out of tool_calls/couldn't finish your exploration and are reporting with incomplete information (if that truly is the case)."
                        }]
                    })

            else:
                messages.append({"role":"user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_block.id,
                        "content": tool_res
                        }]
                    })

        except Exception as e:
            record = {"type": "tool", "run_id":run_id, "turn":i, "tool_name": tool_block.name, "args_json": json.dumps(tool_block.input), "started_at": started_at, "ended_at":str(datetime.datetime.now()), "ok": False, "error_type": f"{type(e).__name__}", "error_description": f"Error description: {e}", "result_chars": 0}
            with open(f"Traces/trace{run_id}.jsonl", "a") as f:
                f.write(json.dumps(record) + "\n")

            if i == MAX_TOOL_USE_ITERATIONS-1:
                messages.append({"role": "user",
                                "content": [{
                                    "type": "tool_result",
                                    "tool_use_id": tool_block.id,
                                    "content": f"Error running the tool: {type(e).__name__}, {e}" + " This is your last tool use turn, so you'll have to synthesize the final answer with the info you have after this turn. Make it known to the user that you may have ran out of tool_calls/couldn't finish your exploration and are reporting with incomplete information (if that truly is the case).",
                                    "is_error": True
                                }]
                })

            else:
                messages.append({"role":"user",
                                "content": [{
                                    "type": "tool_result",
                                    "tool_use_id": tool_block.id,
                                    "content": f"Error running the tool: {type(e).__name__}, {e}",
                                    "is_error": True
                                }]
                })


    else:
        print(f"Iteration {i}, Claude requested an unknown tool: ", tool_block.name)

        # log after tool call
        record = {"type": "tool", "run_id":run_id, "turn":i, "tool_name": tool_block.name, "args_json": json.dumps(tool_block.input), "started_at": started_at, "ended_at":str(datetime.datetime.now()), "ok": False, "error_type": "UnknownTool", "error_description": f"Unknown tool call: {tool_block.name}", "result_chars": 0}
        with open(f"Traces/trace{run_id}.jsonl", "a") as f:
            f.write(json.dumps(record) + "\n")

        if i == MAX_TOOL_USE_ITERATIONS-1:
            messages.append({"role": "user", "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_block.id,
                        "content": "You called an unknown tool. Double check that you're calling an available tool! You've also used up all your tool use turns, so you'll have to synthesize the final answer with the info you have. Make it known to the user that you didn't finish your exploration and are reporting with incomplete information if that is actually the case.",
                        "is_error": True
                        }]
                    })

        else:
            messages.append({"role": "user", "content": [{
                "type": "tool_result",
                "tool_use_id": tool_block.id,
                "content": "You called an unknown tool. Double check that you're calling an available tool!",
                "is_error": True
                }]
            })

    started_at = str(datetime.datetime.now())

    result = client.messages.create(
        model = "claude-haiku-4-5-20251001",
        max_tokens = 1024,
        messages = messages,
        system = SYSTEM_PROMPT,
        tools = tools,
        tool_choice = {"type": "auto", "disable_parallel_tool_use": True}
    )
    print(f"Iteration {i}, Claude's result: ", result.content)
    curr_input_tokens = curr_input_tokens + result.usage.input_tokens
    i += 1

    # log after Claude is called
    record = {"type": "call", "run_id":run_id, "turn":i, "started_at": started_at, "ended_at":str(datetime.datetime.now()), "input_tokens": result.usage.input_tokens, "output_tokens": result.usage.output_tokens, "stop_reason": result.stop_reason}
    with open(f"Traces/trace{run_id}.jsonl", "a") as f:
        f.write(json.dumps(record) + "\n")


if curr_input_tokens > MAX_INPUT_TOKENS:
    print("Max input tokens were reached. Claude's answer may not be complete")

final_ans = ""
for block in result.content:
    if block.type == "text":
        final_ans = block
        print(final_ans)