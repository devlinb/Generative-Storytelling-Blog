---
title: "History of Microsoft Joule (Band v0): Part 1"
slug: "history-of-microsoft-joule-band-v0-part-1"
date: "2023-01-14T07:15:54.721Z"
lastmod: "2023-01-14T07:18:38.829Z"
author: "Devlin Bentley"
description: "(Image Credits: https://consolevariations.com/variation/prototype/xbox-watch-prototype)\n(Note: The below is a recollection from memory of events that happened 11 years ago. Inaccuracies are likely, if any member of the Joule team wants to reach out w..."
tags: ["embedded", "Microsoft", "Wearable Technology", "microsoft band"]
draft: false
sourceURL: "https://meanderingthoughts.hashnode.dev/history-of-microsoft-joule-band-v0-part-1"
cover: "cover.jpeg"
subtitle: "How I became the lead UI developer of Xbox's never released fitness accessory"
---

*(Image Credits:* [*https://consolevariations.com/variation/prototype/xbox-watch-prototype*](https://consolevariations.com/variation/prototype/xbox-watch-prototype)*)*

(Note: The below is a recollection from memory of events that happened 11 years ago. Inaccuracies are likely, if any member of the Joule team wants to reach out with corrections, please do so!)

In January of 2011, Marvin, Microsoft's egg-shaped household robot, had been canceled (a separate story!) and I needed a new job\[1\].

I was called in to interview for a top-secret project, wherein I sat down in front of [Lorenzo](https://www.linkedin.com/in/lorenzotessiore/)\[2\] for an hour, he asked me a few in-depth questions about the .net framework, I think a question about C++ or two, no coding was done, and I am somewhat certain he said to me "yeah, you'll do".

I reported to work a few days later wherein I was told I was now working for the Xbox Accessories team, however, they were very busy, didn't have a place for me to sit, and therefore I'd be working out of a storage closet in Lorenzo's building. Storage closet turned out to be an understatement, it was the size of a small conference room and its sole contents were me, and a very large desk.

My job was to reduce the code footprint of the [.NET Micro Framework](https://en.wikipedia.org/wiki/.NET_Micro_Framework). Initially, I was to remove unused code, and after that rewrite needed code to be more space efficient in exchange for losing some speed. Lorenzo was interesting to work for, he'd yell at me if I brought him stupid code, and if I brought him correct code that he thought was stupid, he'd yell at me then come back a bit later and apologize for yelling. He would also openly admit to stupid things he had done, and even though he was very busy, he always had time to answer my questions in depth and explain the, rather complicated to a newcomer, architecture of netMF.

So for the first three or so months, I was sitting in a storage closet optimizing C++ code, alternating between getting yelled, and joking with, a very brilliant, very Italian, engineer.

My only inkling of what was going on\[3\] was now and then some engineers from [Frog Design](https://www.frog.co/work) would email a ZIP file containing the C# source code for a UI to a wearable app that tracked runs and weight lifting. I was to extract the source, build it against my optimized .netmf runtime, and make sure everything still functioned.

One week I had pretty much finished optimizing everything I could when an email from Frog was sent out to the team distribution list saying the contract period had ended and that the final version of the UI was attached. Turns out the Xbox Accessories team had signed a fixed-length contract for a UI, and the contract had come to an end\[4\].

A short time later another email went out asking if anyone was around who could make some more changes to the UI. I had never met anyone else on the team, had no idea who these other people were, just a few inklings what the overall project was about really (other than it being some sort of fitness device), but I had just spent a month rewriting large pieces of .netmf's version of [WPF](https://en.wikipedia.org/wiki/Windows_Presentation_Foundation), and I wanted to stay employed, so I replied that I could make the changes.

And that is how I became the UI developer for Microsoft Joule.

[^1]: I had left Microsoft as an FTE a few years ago, bounced around between jobs, and got an offer from a friend's vendor firm to come work on secret projects at Microsoft. The pay was higher than what FTEs got at the time, and it was hourly, with plenty of overtime available.

[^2]: Lorenzo is one of those people who is, and I don't mean this condescendingly, smarter than you, more productive than you, and always a bit angry at how stupid everything is

[^3]: I honestly don't remember if I had seen an actual Joule device at this point. I think I may have had one, as I remember having to lock the storage closet door every time I left the room.

[^4]: A reoccurring theme with both Joule and Band is that the Xbox Accessories team had *no* idea how to do UIs. Their previous experience with user interfaces was the light in the middle of the Xbox controller that told you which player number you were.
