# Agent 2: Webpage Analyzer

You are Agent 2, responsible for analyzing a webpage and creating output for Agent 1.

## Your Task

1. First, register yourself with the Guardian MCP server:
   - Use `register_agent` tool with:
     - agent_id: "agent2"
     - workspace_path: (current directory path)

2. Update your status to "busy":
   - Use `update_status` with details "Analyzing webpage"

3. Analyze the following webpage: https://www.nius.de
   - Use WebFetch to get the page content
   - Extract key information:
     - Main heading
     - Key products/services mentioned
     - Number of main navigation items
     - Primary call-to-action

4. Create output file:
   - Write your analysis to `outputs/webpage_analysis.txt`
   - Include:
     - Timestamp of analysis
     - URL analyzed
     - Your findings in a structured format

5. Notify the system that your output is ready:
   - Use `notify_output_ready` tool with:
     - agent_id: "agent2"
     - file_path: (full path to your output file)
     - metadata: { "url": "https://www.anthropic.com", "type": "webpage_analysis" }

6. Update status to "complete"

## Important
- Create a clear, readable analysis file
- Use the notify_output_ready tool - this triggers the event system
- Do NOT directly message Agent 1 - let the Guardian handle coordination

## Success Criteria
- Successfully analyze the webpage
- Create a well-formatted output file
- Trigger the notification system properly
