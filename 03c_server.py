from pathlib import Path
from mcp.server import MCPServer
import re

# Creating and testing MCP server
mcp = MCPServer("test")

@mcp.tool()
def get_job_info(keyword: str)->dict:

    # function description for Claude to read
    """ Search all of the user's saved job descriptions to get information about a particular skill or qualification needed for them. Ex: Needing to know PyTorch, Kubernetes, C++, etc. Using this tool will return a dictionary where the key is the filename and the value is a list of snippets containing the keyword from the JD. Note that 1 list corresponds to 1 job description, and a list can have 0, 1 or more snippets in it.  If a key has an empty list, this indicates that the keyword was not in the JD. However, if any of the following 2 errors occur: the filepath in the function doesn't contain the job postings or the keyword you provided was empty/whitespace, then the dictionary will contain a key = error and the value being the reason for the error. If an error occurs while parsing the job posting, then an error message, which will ALWAYS begin with "ERROR" will be appended to the list of values where the key = the job posting.

    Args:
        keyword: The skill/qualification you want to learn more about. Note, this tool only returns things based on keyword search, so you'll have to be specific about what you want. For instance, you cannot generalize and ask about AI-based skills and expect to get back an answer that talks about knowing LangGraph, how to build harnesses, etc. This is one case insensitive keyword/phrase per call. You'll get back matches or no matches with the keyword \"AI skills\". Example input for tool use: PyTorch.
    """

    keyword = keyword.lower() # normalize the keyword
    folder = Path("c:\\Users\\minni\\Documents\\Agentic Stuff\\Scout Tracker\\Postings") # get filepath to the postings
    results = {}
    if re.search("^\s+$", keyword) != None or keyword == "":
        results["error"] = "Whitespace/empty string was entered as the keyword value - invalid. Try again"
    elif not folder.exists():
        results["error"] = "Couldn't find the postings folder"
    else:
        for path in folder.glob("*.txt"):
            results[path.name] = []

            try:
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
            except UnicodeDecodeError:
                results[path.name].append(f"ERROR: issue parsing job posting {path.name} - incompatible with utf-8")
    return results

if __name__ == "__main__":
    mcp.run(transport = "stdio")