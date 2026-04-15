---

title: "A Vision For Useful Company Wide Agents"
date: "2026-04-15T15:30:00-07:00"
author: "Devlin"
authorTwitter: "thedevlinb"
cover: ""
tags: ["AI", "agents", "workplace"]
description: "A vision for company-wide agents that manage knowledge, attention, and cross-tool workflows."
showFullContent: false
readingTime: false
hideComments: false

--- 



# A Vision For Useful Company Wide Agents

Current business focused agents suck. Some are more useful than others (Notion), some try to be useful (Claude's business offering) but none of them is holistic.

Current agents can search across multiple sources of data. A few can take some actions, moving linear tickets around, even writing code and committing code.

Your company probably has a transcription agent listening to every meeting, shoving a transcript into a folder somewhere for it to never be looked at again. 

You likely have multiple agents running through Slack fetching information on demand, or handling some repetitive tasks.

Your agents should be doing a lot more.



## Your Company's Knowledge Graph

Imagine this world - every meeting transcript is gone through and what people are working on gets tagged, even better what people *know* about gets tagged. What people are good at is tracked. When someone needs to know who is the subject matter expert on a topic, your company's AI instantly knows.

Duplicate work or common complaints are automatically tagged and identified. A problem that is happening across multiple teams is brought to attention right away.

From an individual's perspective, all Slack conversations that are relevant to me are highlighted each morning when I sit down at my desk. I can ask my computer what I need to get started on for the day and I'm given a list of what needs my attention.

Work streams across Slack, email, Linear, Github issues, PR comments, Notion threads, asks for feedback in Figma, are all brought together into one holistic view of what needs to get done.

As we progress into an agentic world, what is most important for people is knowing what needs their attention. Where do I need to focus to oversee what is going on right now?



## Pulling This Off

The technology is actually there. Heck this can be built in one of two ways - a centralized solution works, but local models are powerful enough now that Gemma 4 or Qwen 3.5 can do it all locally. Setup MCP servers to Slack and Notion and you are good to go. Just use your favorite meeting recording tool that does diarization. 

Local first preserves privacy and is a lot less creepy (an important point to consider for AI products right now). Run a local graph DB, every coworker has an entry, links to all meetings you've had with them, information on what they are working on, what topics they are most knowledgeable about. The next type of nodes in this DB are topic nodes, areas of work within the company. Categories are automatically created, regular cleanup tasks consolidate tags and keep the DB clean. Periodically an agent goes through Slack channels, email, Linear, and so on, pulling new content and prioritizing what needs attention. 


Local lets this scale well. You really do want each person to have their own view of the world, and this is one of those problems that scales O(n²) with the number of users. Doing this work on the edge saves a lot of resources, but it limits your target audience. An initial product launch would probably be Mac only.



Of course this can be centralized, and that makes it more palatable to investors. I've previously written about how a focus on SaSS has introduced myopia across our industry, and this may be another example, but one does what one must to build a viable business. 



# A Day In The Life

I sit down at my computer at login. CompanyAI lets me know there are 2 new surveys I need to fill out for my team in a manager's Slack channel. I am reminded of 2 new code reviews seeking my approval, and one of my employee's has a code review that needs approval from a third party team and he's been waiting 2 days so I may want to intervene. In a meeting yesterday another team discussed new work items that will impact us, and I'm given the name of the dev leading the effort so I can reach out and discuss the work she's doing.



Mid day, those items completed, I ask CompanyAI if there is anything else I should be focusing on. I am told the Figmas for our team just got updated and I may want to take a look. Using STT (ASR) I am able to easily add items to my own to do list. Optionally I can create Linear tickets for those to do items that need to be tracked. I've been thinking about some of our data normalization needs lately and I ask my Company AI to create me a new spike in Linear, assign it to me, create a new page in my team's Notion, and link the Linear ticket to the Notion page, and add the spike to my to do list for tomorrow.


After each meeting I attend through the day I am able to quickly tell my CompanyAI what takeaways are most important to me, and also add any to do items to my personal list using just my voice. I can also specifically add new tags or categories that may have come up during the meeting, to help the categorization system with its job.

Throughout the day, my attention is focused and purposeful. When distractions do come up, I can quickly prioritize them for later if need be, and know they won't be lost. When I am done with a distraction I can just ask my computer what I was doing, and then jump right back into it.

Focus and attention are the most valuable resources we have, let's use AI to amplify them.












