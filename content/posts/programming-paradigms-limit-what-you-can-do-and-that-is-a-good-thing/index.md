---
title: "Programming Paradigms Limit What You Can Do (and that is a good thing!)"
slug: "programming-paradigms-limit-what-you-can-do-and-that-is-a-good-thing"
date: "2022-12-22T06:34:29.416Z"
lastmod: "2022-12-22T06:34:29.416Z"
author: "Devlin Bentley"
description: "Junior engineers are told that programming paradigms are a way to accomplish new things! Inheritance, pure functions, monads, polymorphism; paradigms unlock new powers!\nBut, the truth is quite the opposite. Programming paradigms limit what you are al..."
tags: ["Software Engineering", "Functional Programming", "Object Oriented Programming", "software architecture"]
draft: false
sourceURL: "https://meanderingthoughts.hashnode.dev/programming-paradigms-limit-what-you-can-do-and-that-is-a-good-thing"
---

Junior engineers are told that programming paradigms are a way to accomplish new things! Inheritance, pure functions, monads, polymorphism; paradigms unlock new powers!

But, the truth is quite the opposite. Programming paradigms limit what you are allowed to do, but that is ok! In fact, here is my thesis statement:

> Programming paradigms are a ways to simplify how we code complex systems so our tiny human brains can grasp what is going on.

A direct example: Class-based object-orientated code requires all functions are attached to a class. This is restricting what the programmer can do, in exchange for simplifying how the code is laid out.  
[No additional power has been gained by forcing all functions to be owned by a class](http://steve-yegge.blogspot.com/2006/03/execution-in-kingdom-of-nouns.html) the only benefit reaped is future maintainers of the code don't have to go around trying to find out where a function is implemented, they know it can be found in the class definition. Boom! One less detail for our limited wetware to keep track of.

Functional enthusiasts are more likely to admit to the truth of this, as arguments for FP typically start as "if you stop mutating data structures, your life gets a lot easier!"[^1] and then they make some good points about pure functions that don't rely on internal or global state.

But, OO peeps, you can still find some of them out there saying that OO gives you additional power!

When writing code, here is the thing I want you to remember, above all else:

> At the end of the day, everything is compiled/interpreted/JITTed to assembly, therefore no additional capability is gained by a paradigm that could not be implemented by hand in assembly if one so wished.

That is the crux of it. Paradigms limit things so that you and I, the human meat that writes code, can try and understand these incredibly complex systems we build. Some paradigms offer more tools, for sure, but you can do OO in C, heck [you can make a runtime multi-dispatch system in C](https://en.wikipedia.org/wiki/Multiple_dispatch#C), and again, if C isn't powerful enough, then quite literally any idea can be implemented in raw assembly because that is what every programming language has to do at the end of the day.

It is worth saying again, paradigms limit us. The first programming paradigm was [structured programming](https://en.wikipedia.org/wiki/Structured_programming), it is something so fundamental to how programming is taught that we don't even think of it as a paradigm anymore. The idea of arranging programs into blocks, having variables only live within those blocks, and having these things called functions, and that those functions are independent from each other, these are all limits placed upon the programmer. And once upon a time, these rules were considered very controversial! [^2]

Microservices are another paradigm; separation of concerns taken to the extreme limit. The only code that is allowed to touch the user profile lives in the user profile services! You cannot even accidentally touch the user profile from anywhere else. Again, simplifying what the old wetware has to deal with.

tl;dr: Paradigms make you think less but also restrict what you can do, pick the paradigm that works best for the problem you are trying to solve, no one paradigm is superior to all others for every single use case.

---

[^1]: I used to believe this then I witnessed redux reducing websites to a crawl when people typed data into simple textbox. Turns out that copying entire strings to change a single letter, is, to put it bluntly, stupid.

[^2]: Of course, nowadays we know we can break these rules in some circumstances, e.g. Exception handling violates the gotos are harmful rule.

---

---
