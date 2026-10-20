---
title: "Introducing TinyTown.ai and Locally Ran Narrative Simulation"
slug: "introducing-tinytownai"
date: "2024-12-04T00:40:12.179Z"
lastmod: "2024-12-04T00:40:12.179Z"
author: "Devlin Bentley"
description: "TinyTown.ai has launched, if you haven’t yet, check it out and vote on what the town’s hero will do next! TinyTown.ai represents a new way of simulating RPG towns, and it can be run on even modest local GPUs. In this post I’ll describe what TinyTown...."
tags: ["llm", "AI", "Video games", "Game Development"]
draft: false
sourceURL: "https://meanderingthoughts.hashnode.dev/introducing-tinytownai"
cover: "cover.png"
subtitle: "How to simulate a small RPG town on a local GPU"
---

[TinyTown.ai](https://www.tinytown.ai) has launched, if you haven’t yet, check it out and vote on what the town’s hero will do next! TinyTown.ai represents a new way of simulating RPG towns, and it can be run on even modest local GPUs. In this post I’ll describe what [TinyTown.ai](https://www.tinytown.ai/) is and how it works!

# An Intro to TinyTown.ai

[TinyTown.ai](https://www.tinytown.ai/) aims to solve the problem in RPG video games of “I just killed a dragon in front of the entire town, but no one said anything!” No matter how many heroics the player pulls off, only a handful of characters have preprogrammed responses about your accomplishments.

[TinyTown.ai](https://www.tinytown.ai/) fixes this! Villages realistically react to everything that the hero does. If the hero brings back a large cache of armor, the blacksmith worries about his business, and if the hero slays a large group of monsters, the villagers are all impressed!

A key to making this technology actually usable was scaling it down to run on LLMs that can run on consumer GPUs. To that extent, [TinyTown.ai](https://www.tinytown.ai/) was built to work on even low parameter models. It targets 3B parameter models quantized to 8bit ints, and I believe that with proper pruning the models can be reduced to well under 2B parameters without sacrificing quality.

# How It Works

Unlike other LLM based town simulations, [TinyTown.ai](https://www.tinytown.ai/) uses a technique I call *narrative simulation*. Leaning into the strengths of LLMs, TinyTown.ai takes the players latest actions as input, and outputs a consistent narrative for the town. The actions and dialogue of NPCs naturally flows from this narrative structure. This means you can watch as NPCs organically decide to throw a party for the character, and when that happens they all know to head to the tavern at the right time. It also means that NPCs will come visit the hero when they are in town, or go and visit each other to have conversations that are appropriate to what has happened recently.

This simulation technique does not have per-character RAG or history, and LLMs are not used to simulate an NPC’s inner world. Existing RPG game engines already have rich behavioral simulations in them and TinyTown.ai doesn’t aim to replace those existing systems. Instead [TinyTown.ai](https://www.tinytown.ai/) is meant to be a small augmentation that adds a layer of depth to the world by removing one of the major immersion breaking pain points in modern games.

That said, it is possible to provide additional behavior and personality data for each NPC, and you can see examples of this on [TinyTown.ai](https://www.tinytown.ai/) right now.

Some final notes:

* The simulation timestep for [TinyTown.ai](https://www.tinytown.ai/) is set to four hours, meaning four hours of events in the town are simulated at a time. This is fully configurable, and the system can be ran in response to player actions instead of being on a timer.
    
* There are still some bugs, especially around the front end in regards to rendering. I am not a games programmer, so please excuse my half hearted attempt at a 16-bit game engine!
    

# Why I Made TinyTown.ai

I first thought of TinyTown.ai around two years ago, and then the paper [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) came out. When I read the paper and saw the implementation I was impressed, but I also felt that 80% of the results could be had for 20% of the (GPU) effort. Around June of 2024 I finally assembled my collection of loose ideas together and began working on [TinyTown.ai](https://www.tinytown.ai/). There is still more that can be done to expand the simulation w/o incurring too much additional overhead, and hey, maybe I’ll get to that! Right now though my efforts are around getting everything running on smaller and smaller models.

If you want to talk more, feel free to get in touch. I can be reached on [Bluesky](https://bsky.app/profile/thedevlinb.bsky.social), [X](https://x.com/TheDevlinB), [LinkedIn](https://www.linkedin.com/in/devlin-bentley) or email at devlin . bentley at gmail.com
