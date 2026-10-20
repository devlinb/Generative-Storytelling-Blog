---
title: "Unlock the Full Potential of LLMs: Ditch JSON for DSLs!"
slug: "unlock-the-full-potential-of-llms-ditch-json-for-dsls"
date: "2024-09-24T19:56:55.800Z"
lastmod: "2024-09-24T19:56:55.800Z"
author: "Devlin Bentley"
description: "If you're not leveraging DSLs with your LLMs, you might be missing out on significant performance and power. LLMs excel at understanding linguistic cues, making them the perfect match for English-like DSLs. Abandoning JSON tokens, which lack literary..."
tags: ["llm", "dsl", "AI"]
draft: false
sourceURL: "https://meanderingthoughts.hashnode.dev/unlock-the-full-potential-of-llms-ditch-json-for-dsls"
---

If you're not leveraging DSLs with your LLMs, you might be missing out on significant performance and power. LLMs excel at understanding linguistic cues, making them the perfect match for English-like DSLs. Abandoning JSON tokens, which lack literary significance, and leaning into DSLs, can enhance your LLM's performance.  
  
Do the current generation of LLMs handle JSON encoding? Of course, at the cost of extra tokens! If you are using smaller models you may find yourself having to fine tune the model on your output format or using tools that restrict the grammar of the output. But if you intelligently adapt a DSL you can get even reliable output even from vanilla 4B parameter models.  
  
Worried about writing a parser for your DSL to JSON? Ask Claude or ChatGPT, this is the type of make-work task that those larger models are great at!  
  
Now, in practice, what does this look like?  
  
Some of you know I've been working on (affordably, quickly!) simulating a small town with tiny locally ran LLMs. Here is a comparison of what the JSON for ChatGPT 4o looks like vs a tiny portion of a DSL that a 4b parameter model can reliably generate after only a handful of examples are fed to it.  
  
**JSON**

```json
{
    "timeOfDay": "08:00",
    "dayNumber": 2,
    "characters": {
        "BLACKSMITH": {
            "fromLocation": "BLACKSMITH_HOUSE",
            "toLocation": "BLACKSMITH_FORGE",
            "dialogue": "Time to get to work"
        },
        "INNKEEPER": {
            "fromLocation": "INN",
            "toLocation": "INN",
            "dialogue": "Come and get breakfast."
        }
    }
}
```

  
**DSL**

```markdown
time: 08:00 // 24 hour
day: 2 // day number

Blacksmith
at: Blacksmith House
going: Blacksmith Forge
dialogue: Time to get to work.

Innkeeper
at: Inn
going: Inn
dialogue: Come and get breakfast.
```

  
For just the small snippet above there is a 1/3rd reduction in tokens, a ratio which carries over to the full schema vs. DSL. The difference in input tokens becomes important when doing few shot learning in a system prompt with a small context window, and the difference in output tokens is very important when running LLMs on the edge (phones, user GPUs).  
  
The DSL above is trivial, it is just some fields separated by newlines! But being willing to step away from JSON makes the LLM happier, results in faster output generation, and simplifies the tooling needed to get reliable outputs. Now I'm still enforcing a CFG on the outputs, but leaning into the language part of Large Language Model enabled reliable output from a 4b parameter (8bit quantized!) model.
