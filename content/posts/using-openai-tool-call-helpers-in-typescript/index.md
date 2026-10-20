---
title: "Using OpenAI Tool Call Helpers in Typescript"
slug: "using-openai-tool-call-helpers-in-typescript"
date: "2024-09-05T06:42:07.739Z"
lastmod: "2024-09-06T20:37:13.265Z"
author: "Devlin Bentley"
description: "The documentation for how to use the new beta tool call helpers API is pretty lackluster, so here is a very brief example.\nOverview and Assumptions:\n\nI tend to store all my tools+prompts in a separate file, while some of my tool handlers are private ..."
tags: ["openai", "TypeScript", "llm"]
draft: false
sourceURL: "https://meanderingthoughts.hashnode.dev/using-openai-tool-call-helpers-in-typescript"
---

The documentation for how to use the new beta tool call helpers API is pretty lackluster, so here is a very brief example.

Overview and Assumptions:

1. I tend to store all my tools+prompts in a separate file, while some of my tool handlers are private class methods that I cannot just import and assign when defining my tools. To work around this, I create functions that take in the tool and assign it to the `function` field of the tool. (Update: Now with full type safety!)
    
2. I know that type inference can in theory do this, but it is *much* easier to have errors at the place of declaration of the variable, rather than have them at the call site that takes the variable in. This is especially true with how these runnable functions are typed in TS, I ran into a 30 minute "what is happening" debugging session when the TS compiler gave me an absolutely horrible error
    
    message when I was passing in an array of multiple tools to [`openai.beta.chat`](http://openai.beta.chat)`.completions.runTools`
    

```typescript

// businessLogic.ts
export type ToolCb = (args: {cbNumberParam: number, cbStringParam: string}) => void;
```

```typescript
// tools.ts
import { RunnableToolFunctionWithParse } from "openai/lib/RunnableFunction";
import { ToolCb } from "./businessLogic";
export const createMyFancyTool = (functionCallback: ToolCb): RunnableToolFunctionWithParse<Parameters<ToolCb>[0]> => {
    return {
        type: 'function', // if you don't declare as RunnableToolFunctionWithParse up above you'll need to write 'function' as 'function' here!
        function: {
            function: functionCallback,
            parse: JSON.parse,
            name: "My fancy tool", // naming tools is actually really important for getting ChatGPT to accurately call them!
            description: "A fancy tool you should call when needed", // descriptions are also super important and should be considered part of prompt engineering
            parameters: {
                type: "object",
                properties: {
                    cbNumberParam: {
                        type: "number",
                        description: "the numeric data"
                    },
                    cbStringParam: {
                        type: "string",
                        description: "the string data"
                    },
                    required: ["cbNumberParam", "cbStringParam"]
                }
            }
        }
    }
}
```

Astute readers will notice that this is only 2 fields different than what the regular tool definition is. As mentioned above, I ran into an issue where after I added the function and parse fields, I got some really gnarly errors, which where the result of me not having written `type: 'function' as 'function'` which you'll likely need to do if you don't explicitly type everything. OpenAI's example code neglects this. However after fully typing everything, I no longer needed to cast the string.

Finally, if you don't like using the parameters built in, you can create a separate type for the arguments and use that directly.
