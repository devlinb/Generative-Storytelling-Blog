---
title: "History of Microsoft Joule (Band v0) Part 2"
slug: "history-of-microsoft-joule-band-v0-part-2"
date: "2023-01-25T07:56:56.006Z"
lastmod: "2023-01-26T05:34:26.251Z"
author: "Devlin Bentley"
description: "When we last left off, I had just reduced the code size of the .net microframework by 50% and reduced the runtime memory requirements from 2 megabytes down to 60 Kibibytes. (Lesson learned: inexperienced people don't know what isn't possible, and can..."
tags: ["microsoft band", "Microsoft", "history", "embedded", "Joule"]
draft: false
sourceURL: "https://meanderingthoughts.hashnode.dev/history-of-microsoft-joule-band-v0-part-2"
subtitle: "Tech Specs of the Abandoned Xbox 360 Fitness Accessory"
---

[When we last left off](/blog/posts/history-of-microsoft-joule-band-v0-part-1/), I had just reduced the code size of the .net microframework by 50% and reduced the runtime memory requirements from 2 megabytes down to 60 Kibibytes. (Lesson learned: inexperienced people don't know what isn't possible, and can therefore accomplish the impossible)

This post will dive more into the technical side of Joule, and as with any technical deep dive, the first place to start is with the specs!

The same warning as last time applies: everything in this post is from my long unaccessed memory and I haven't bothered to double-check anything.

* Accelerometer, HR Sensor, GPS
    
* Two K60 MCUs
    
    * Connected via a UART
        
* 128x128 16bit LCD screen
    
* 4 (!!) capacitive screen touch sensors (typical devices have hundreds) wired directly to the A/D inputs
    
* A ludicrously oversized battery
    
* Ran the .net Microframework on both CPUs
    
* Modestly sized flash chip for storage utilizing FAT32
    
* All wrapped up in a very durable case that was plastic in front, and metal in the back.
    

For anyone in the know about embedded, these specs raise a lot of questions. Let's go through those questions one at a time; it's [story time](https://escapepod.org/).

# What Exactly Was Joule Supposed To Do?

The way I heard it, and this is one of those "friend of a friend told me" types of things, some [boffins](https://en.wikipedia.org/wiki/Boffin) from [Microsoft Research](https://en.wikipedia.org/wiki/Microsoft_Research) showed a cool demo where they attached accelerometers up to the arms of a volunteer, had that person go on stage, do push-ups, jumping jacks, bench presses, and the like, and at the end of it all a beefy computer hidden behind a curtain counted how many repetitions of each exercise the person did. I'll also take a guess and say that the demo was very carefully staged.

Sometime after the demo, orders went out to productize this technology as a wearable device that cost under $100. (As always, if anyone has firsthand accounts that better explain the history of Joule, please get in touch! I'd love to perform more accurate historical documentation!)

Joule was an exercise accessory that counted how many reps users did of different exercises. A GPS was thrown in there for running, and a heart rate monitor was added presumably because that was the single most obvious thing to add to the product.

Please remember that fitness wearables were not yet a well-defined thing. The most common wearable that you'd see around 2011/2012 was people running with an [iPod nano strapped to their arm](https://duckduckgo.com/?q=ipod+nano+armband&va=l&t=hc&iar=images&iax=images&ia=images). Single-purpose step counters were huge, but that was the extent of the fitness wearables market.

Since Joule was designed by the Xbox Accessories team, one assumes it would pair with the Xbox 360 and ship with some cool at-home fitness game, and that idea was indeed proposed, but at some point shuttered. (If you are reading this and you know anything more about the aborted efforts in this direction, please [get in touch](https://meanderingthoughts.hashnode.dev/contact)!)

This does bring up a question: Why was the Xbox Accessories team working on a hardware product that didn't have any guaranteed software support? Well, Xbox 360 work largely happened across two buildings, Studio A did software stuff, and Studio B did hardware stuff. To greatly simplify a complex topic, the relationship was frequently dysfunctional\[1\], and Joule requiring pairing with a 360 was always an on-again-off-again sort of thing (at least the way I heard it) and from the get-go Joule was perfectly happy functioning without an accompanying Xbox.

# Why 2 MCUs

For people who are not familiar with the world of embedded MCUs, it is important to understand that MCUs have a very small amount of onboard storage called program flash (p-flash), and that space cannot be expanded. Code stored in p-flash can be executed in place, meaning it doesn't have to be loaded into RAM, and likewise, resources in p-flash (such as fonts) can be used without consuming RAM. Code on external flash has to be first loaded into RAM before it is executed (exceptions exist, none of which apply to Joule). The same logic applies to things like images, icons, and fonts. If you have 100KB of fonts, they have to live in p-flash, because the entire MCU only has 128KB of RAM!

As I regaled previously, I was originally brought on to reduce the size of the .netMF runtime to fit on the K60, which has 512 Kilobytes of Flash. (I don't recall if the K60 variant we used had the full 512KB but I assume it did.) Prior to my efforts, the framework clocked in at around 2 megabytes\[2\]. I was successful in my reduction efforts, but once application code, fonts, and icons were added, we still didn't fit all on one MCU.

There was of course a lot of other code that ran on the MCU. Primarily lots of ML models to count repetitions, followed by the necessary custom math libraries, and some super wacky 3rd party licensed code for step counting that internally measured everything in [mils](https://en.wikipedia.org/wiki/Thousandth_of_an_inch) (we had to convert from and to metric whenever we got close to that section of the code)\[3\]

Math was done, and it was realized that there was no way we were going to fit everything, ML models, fonts, and the .netMF runtime, in 512KB. The K60 was already the largest MCU around at that time (512KB p-flash and 128KB SRAM were obscene back then!), there just wasn't anything larger on the market.

When all seemed lost, someone (probably [Vinod](https://www.linkedin.com/in/hingov/)) had a crazy idea: Put two K60s in the product and wire them together. Put the ML stuff, drivers, and fancy math libraries on the primary CPU, and put the UI and all its assets on the secondary MCU.

And thus the day was saved.

# Why The Tiny Screen?

I have no idea, I presume it was cheap. Joule had some horrible display controller hooked up over SPI, and the device couldn't even manage 30 FPS. I am 99.99% sure it didn't use DMA for data transfers, which was at least partially why the FPS was so low. The screen was so bad you could easily count the pixels without a magnifying glass. Everything looked terrible on it.

On the plus side, cheap plastic screens are durable, I would frequently play hacky sack with Joules up and down the hallways of Studio B at night. They were virtually indestructible.

# Four Touch Sensors

Typically a phone screen has thousands, if not tens of thousands, of touch sensors, each one incredibly tiny.

Joule had this touch sensor layout:

![](image-48872dc11049.png)

Each one of those squares is a distinct "touch", as in only 1 button could be supported in each square, and movements within a square could not be detected. It is hard to even describe what this means and how bad it is. Later in the project efforts were taken to improve things, and maybe someday I'll write a post just about the touch screen adventures we had.

Why only four sensors? Presumably, because no one thought to add a touch controller. Why no touch controller? Good question.

# Giant Battery

The battery was obscenely large. That was a good thing because no power management existed. While turned on, Joule ran its 2 CPUs at full speed, all the time. If I recall, battery life was 4 to 6 hours, which was deemed good enough for a week of hour-long workout sessions.

# Why Use The .NET Microframework?

I am not sure why .netMF was chosen as the framework for Joule. I suspect it was because Lorenzo had worked with some of the senior and principal engineers in Xbox Accessories, and they went to him asking for help.

If it isn't obvious by now, the Xbox Accessories team, at the time, wasn't super experienced in making complex UIs. My best guess is they thought doing absolutely everything from scratch would be too large of a task to undertake, and using .netMF at least gave them a UI framework to start with, and finding C# WPF developers back then was pretty darn easy.

Also the ecosystem for "advanced runtimes for MCUs" was not as mature back then as it is today. Nowadays you can just throw something like [Mbed](https://en.wikipedia.org/wiki/Mbed) on a chip, pick an open source UI framework, and be done with it.

# That External Flash Chip

Guided Workouts and user profiles. I'll go into great depth about Guided Workouts in the future. They are awesome. On a closely related note, FAT32 is a horrible filesystem for battery powered devices and accordingly, data was very easy to corrupt.

# Durable

I already mentioned hacky sack. I also frequently roundhouse kicked Joules. One of the test engineers took some Joule's diving, and apparently even the pre-production units had 0 issues with water ingress.

# In Summary

Anyone familiar with product design may have noticed that I haven't explained why these decisions came about. Important steps of product design were all skipped, starting with such fundamentals as requirements gathering. The next post will dive into what was going on behind the scenes that allowed this hot mess of a hardware+software design to come into being.

# Footnotes

[^1]: Understatement of the year. Employees from each building had plenty of tales to tell of how foolish people in the other building were. However this being the year 2012, "foolish" wasn't the word people used, rather stories involved a lot of f-bombs and tales of literally tens to hundreds of millions of dollars in potential profits were squandered away. If you ever want to hear some interesting stories, get some Xbox 360 era employees drunk at a bar.

[^2]: That number might have been framework + Joule UI, but I honestly forget.

[^3]: This experience had a direct impact on Microsoft Band! We'll get back to that in a few months.
