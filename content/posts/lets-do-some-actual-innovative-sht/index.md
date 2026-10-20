---
title: "Let's Do Some Actual Innovative Sh*t"
slug: "lets-do-some-actual-innovative-sht"
date: "2025-02-13T08:27:53.019Z"
lastmod: "2025-04-29T05:06:38.605Z"
author: "Devlin Bentley"
description: "Remember back before everything was SaSS and companies had original ideas? Back when tech companies designed cool stuff under the expectation that they’d sell cool stuff to customers for money and the customers would be happy?\nWell all that is dead b..."
tags: ["llm", "RAG", "smart home"]
draft: false
sourceURL: "https://meanderingthoughts.hashnode.dev/lets-do-some-actual-innovative-sht"
---

Remember back before everything was SaSS and companies had original ideas? Back when tech companies designed cool stuff under the expectation that they’d sell cool stuff to customers for money and the customers would be happy?

Well all that is dead because everything has to run in the cloud to justify a monthly fee. This is why 90% of the AI product ideas are not ambitious, they have an underlying need to force an always on internet connection to a cloud service provider so they can justify charging you a bunch of money every month.

Let’s fix all that and return to the halcyon days of the late 90s when people tried to dream up of cool stuff technology might do some day.

# Ground Rules

This post will cover stuff that is either possible right now, or at most 1 to 2 years out.

# Around The House

You wake up in the morning, you say “computer, turn on the lights”. A microphone array in your bedroom picks up your voice and sends the command to a locally hosted AI server. The server uses ASR (automatic speech recognition) to understand what you said. The AI knows what room you are based on what mic you used, it can control the lights by sending local commands to the bulbs, no matter what “standard” is being used. The LLM has a RAG database of commonly used scripts to do things around your house, it calls upon these snippets to get things done, filling in parameters as needed. All of this happens locally, no internet connection needed.

Getting out of bed, you ask “house, will it rain during recess today?” Even a quantized 40B parameter LLM is smart enough to know you are asking about your son’s recess. Looking at today’s school schedule (School calendar PDF → RAG) and today’s weather report, the LLM sees it will rain after 4pm but that recess is from ten to eleven. Your house replies “It’ll rain this afternoon, no need to waterproof Nathan today, but bring an umbrella when you pick him up after school.”

After getting breakfast ready, “House, in 5 minutes start my car.” [Even though your car doesn’t support automatic warming in the morning, or have an API that can be accessed,](https://en.wikipedia.org/wiki/Chevrolet_Bolt_EUV) your personal AI machine has no problem accomplishing this. A copy of Android runs in an emulator and the multimodal LLM navigates through the app and starts your car.

Getting into your toasty warm car, you drop Nathan off at school and your spouse at the train station, and arrive home to a full day of WFH. Before your first meeting you start a load of laundry. W[hen the load is finished a microphone in proximity to the washing machine can trivially identify the “finished washing” jingle a](https://www.youtube.com/watch?v=sY9o4Ap1WCo)nd a voice will tell you that the laundry is ready to go in the dryer. Using basic ASR capabilities, such as silence detection and diarization (to distinguish when you are just talking to yourself), and looking at your calendar, your home AI doesn’t announce the laundry is done until you are finished with your morning meetings.

# At Work

After your morning standup Zoom ends, you open Hacker News. [You see that someone has said something wrong on the Internet](https://xkcd.com/386/), so of course you must reply. 5 minutes after standup has ended, a voice from your computer reminds you that you asked it to interrupt if you spent more than 5 minutes distracted on social media. Your AI promises to save off your partially written comment, you agree and the distracting browser tabs are all whisked away and you switch over to your terminal and pull down the latest changes from GitHub.

[Throughout the day, your personal LLM is a companion that you interact naturally with back and forth.](https://en.wikipedia.org/wiki/Rubber_duck_debugging) Always listening, your LLM can pull up documents in Notion, knows what Jira tickets you are working on, and can dig through your Slack DMs to find relevant conversations. A RAG system that is more than just full text search organizes your work. Metadata about those Notion and Jira tickets has been added, “Computer, add this Notion page to my V2 redesign project notes”.

After pushing some changes, you ask your LLM “Please start a PR on GitHub with my latest changes.” A browser window opens with the PR template ready for you to fill out. After opening the PR you send a request out for reviews and fire off another request “bring that Hacker News thread back up from earlier today and timebox it to the next 10 minutes.” A count down timer starts off in the corner as you resume writing your reply.

# Dinner Time

Setting some water to boil on your induction range, a microphone in the kitchen listens for the sound of water boiling and the “smart” stove’s app, again being ran in an emulator, turns the temperature down once bubbling begins. Your home AI, [using Wi-Fi location sensing](https://wballiance.com/wi-fi-sensing-101-an-introduction/#:~:text=So%2C%20what%20is%20it?,management%20markets%2C%20among%20many%20others.), knows you have left the kitchen, so it alerts you that it is time to “add the noodles”. A few minutes later your at home AI hears the oven preheat beep, and once again seeing you have left the kitchen, lets you know the oven is ready.

After putting the bread in the oven to bake, you ask “House, pull up that Pesto recipe my wife really liked onto my phone.” You verbally asked your house to track the pesto recipe last time you made it, and the page on your phone’s browser was bookmarked and saved off into a RAG database with appropriate metadata that allowed it to be quickly fetched again.

# Rest and Relaxation

Your home AI does what a half dozen smart home standards never could do - Finally integrate everything together. Your home AI can write code to directly hit endpoints for smart switches or bulbs, or it can interact with any number of smart apps as if it where a regular, human, user. Controlling your lights, TV, window blinds, everything works through your home AI, because it doesn’t care about standards or walled gardens, it is capable of doing whatever is necessary to get the job done.

Case in point, your Android TV doesn’t support remote wake on Wi-Fi, but an IR blaster + Home AI takes care of this for you. Also, annoyingly Google disables voice control on Android TV if you opt out of ads and tracking, but not a problem, as your personal home AI can search across VOD providers and chrome cast to your TV.

# Conclusion

Today’s technology, and a little bit of cleverness, can do amazing things. Unfortunately the current players in the AI market are not incentivized to make things work for customers:

1. Google needs display ads, any feature that reduces the number of ads someone sees is going to get killed. Because Google is one of two gate keepers to people’s personal lives (Apple being the other major player), it will take a lot of effort to work around all the roadblocks Google is going to erect to stop what is an existential threat to their business model.
    
2. Apple could pull a lot of the above off, but outside of a few narrow areas, they have demonstrated the repeated inability to generalize their success and market domination to move into other fields.
    
3. Facebook also relies on ads, but even if they wanted to accomplish the above, they need to work around phone limitations. Their Meta smart glasses already run into this problem, the glasses are held back due to limitations imposed by the phone.
    
4. Outside of Xbox, Microsoft is allergic to consumer hardware (read the rest of my blog for examples!), and their loss of market share in the mobile space also holds them back here. If Microsoft had a viable mobile platform they could leverage that in the ways I describe above as a “hub” to do other things, but that ship has long since sailed. Also Microsoft is currently addicted to showing off CapEx spending through massive datacenter buildouts, and edge computing would go against that vision (even if it proved more profitable in the long term! Microsoft’s empire was built selling software that ran on personal computers!)
    
5. OpenAI maybe, but again they want to show that CapEx spend.
    
6. The Rabbit M1 should have been this, they hinted at doing a hosted Android emulator thing, but rumors are that never actually happened.
    

That said, a sufficiently well funded player in the market could accomplish everything I’ve outlined here. There isn’t anything truly outlandish, just a bunch of boring engineering work with well established technologies. The only thing new would be the model to control a phone, and research in that area is progressing at a steady rate.
