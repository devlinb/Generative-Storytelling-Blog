---
title: "Cooperative Multitasking on Microsoft Band"
slug: "cooperative-multitasking-on-microsoft-band"
date: "2023-03-31T18:06:01.473Z"
lastmod: "2025-08-14T06:42:48.268Z"
author: "Devlin Bentley"
description: "tl;dr\nThis is going to be a very technical post, if you are not familiar with different concurrency models and subscription (pub/sub) systems, then I'll be throwing a lot of new knowledge your way. To make suffering through more enticing, I'm going t..."
tags: ["embedded", "Wearable Technology", "Microsoft", "microsoft band", "multitasking"]
draft: false
sourceURL: "https://meanderingthoughts.hashnode.dev/cooperative-multitasking-on-microsoft-band"
---

# tl;dr

This is going to be a *very* technical post, if you are not familiar with different concurrency models and subscription (pub/sub) systems, then I'll be throwing a lot of new knowledge your way. To make suffering through more enticing, I'm going to summarize how we did things first, then dive into details.

1. Band used [Cooperative multitasking](https://en.wikipedia.org/wiki/Cooperative_multitasking) along with an async, (mostly) lock free IO model. No kernel forcing threads to switch contexts, and no waiting on locks. This dramatically reduces overhead.
    
2. The single primitive of concurrency was Asynchronous Procedure Calls, basically a function that you can schedule to run at a later time.
    
    * Statically allocated equivalent of closures, no capture, any state that a module needed was statically allocated at compile time, and passed through callbacks. Frequently modules made their callers allocate storage for the module's state, which is downright magical.
        
3. 100% Async IO with callbacks on completion
    
4. The Microcontroller Unit (a [K24](https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/general-purpose-mcus/k-series-arm-cortex-m4/k2x-ks2x-usb/kinetis-k24-120-mhz-full-speed-usb-256kb-sram-microcontrollers-mcus-based-on-arm-cortex-m4-core:K24_120)) had a very powerful [DMA engine](https://en.wikipedia.org/wiki/Direct_memory_access#Third-party) that was used to offload the majority of IO
    
5. The CPU slept in an ultra low power state over 96% of the time, except when the screen was on and almost all UI elements were were changing every frame, then it was only asleep ~70% of the time.
    

# Intro To Microsoft Band

[Microsoft Band 2](https://en.wikipedia.org/wiki/Microsoft_Band_2) was a wearable smart watch that had a 90mhz CPU (downclocked from 120mhz to save power), 256KB of SRAM, 4MB of external SRAM, and a *lot* of sensors that needed to be read from, some of which had soft real time requirements.

With only 1MB of flash to store the all executable, code, and one of the world's first tiny curved batteries, power and space was at a premium.

(I'll mix up Band 1 and 2 freely, at a block diagram level you can treat them as being siblings, Band 2 was an iteration on Band 1).

Not only was Band powering a lot of sensors, but the UI team was pushing the hardware to its limits: full anti-aliased TrueType fonts, real alpha blending, VSync'd at 30FPS, and the touch controller had a worse case latency of 2 frames. At launch, the Microsoft Band dropped fewer frames than an Apple Watch ,while running at less than 1/10th the CPU power, without a dedicated GPU of any sort, and had a battery that could last for up to 3 days. (Fun fact: If a different accelerometer chip had been used, Band 2 would could have reached 5 days of battery life!)

The rest of this post will describe how modern asynchronous programming practices, written in C, without any heap allocations, were used to provide the impressive performance, and amazing battery life.

# Cooperative Multitasking

(If you are familiar with how Node works, what we did will sound familiar, however as an embedded development team we were not familiar with Node and we ended up independently choosing many of the same software engineering patterns.)

There are two popular ways to handle concurrency, cooperative multitasking and preemptive multitasking. Preemptive systems also often, but not always, use a traditional threading model.

Everyone reading this is likely familiar with preemptive multithreading: Every few hundred microseconds whatever code is running is suspended, all its state is saved off, and another thread is loaded up and starts running. This all takes a little bit of time, and each thread has a bit of memory overhead, typically the size of the stack plus some book keeping. Because multiple pieces of code are running "at the same time", it can result in race conditions when multiple threads try to access the same data of memory. [Locks or some alternative](https://en.wikipedia.org/wiki/Spinlock#Alternatives) are used to solve resource contention issues, but it is still easy to run into bugs.

Band does not have threads or preemption. Band does what many low power systems have historically done, and uses [cooperative multitasking](https://en.wikipedia.org/wiki/Cooperative_multitasking), more specifically Band has one thread of execution, and code uses cooperative multitasking on that one thread.

With cooperative multitasking, one function runs until it's finished, then returns control to a dispatcher, which then starts running the next function. This avoids worrying about threads, and it side steps race conditions. Everything is controlled by a single loop that keeps track of what function is in line to run next.

The large downside to cooperative multitasking is if a function gets stuck in an infinite loop, the entire system will become unresponsive because that function never returns control to the dispatcher. Similarly, if one function takes too long to run the entire system will appear laggy and unresponsive.

Because all code on Band was written in house, we didn't have these particular worries. During internal testing we used a [watchdog timer](https://en.wikipedia.org/wiki/Watchdog_timer) set to 20ms for the UI, and ~2ms for everyone else, if any module took more than 2ms before it returned, a crash dump was created and the code was investigated and optimized.

Used carefully, cooperative multitasking can be a significant savings on CPU and memory vs using threads, and it boasts a simpler mental model that avoids worrying about data races; all in all it was a perfect fit for Band. After we threw in some Async IO and a pub/sub system (deep dive on Band's pub/sub in a future blog post!) we had a lean mean, power, memory, and CPU efficient, personal sensor machine.

# Asynchronous Procedure Calls

I mentioned that the dispatch loop is responsible for determining which function gets run next, but what are those functions exactly?

Asynchronicity is at the heart of Band, including function calls. Band provides a primitive called an Asynchronous Procedure Calls, basically the capability to schedule a function to run at some future point in time, write this line of code:

```markdown
ScheduleApc(myFunctionPointer, 20)
```

and your function will run 20 milliseconds from now.

That is the basics of an APC, and it is an incredibly powerful concurrency primitive, but what I presented above isn't enough, what you actually need is this:

```markdown
AbortAndEnqueue(functionPtr, contextPtr, delay)
```

If your function is already set to run, it needs to be removed from the queue of upcoming functions and added back in again[^1], and you need the ability to pass parameters into your function, thus a context pointer that should ideally point to a structure containing all the values your function needs to run. (Because this was done in straight C, we used a `void *`. ;) )

From a functional programming perspective, this context pointer is basically used to manually capture any state, but it is very flexible and can be used for a lot of other things as well.

Band's dispatch loop maintained an ordered queue of APCs, by way of [intrusive linked lists](https://www.data-structures-in-practice.com/intrusive-linked-lists/), sorted by `delay`. Because Band had no heap, the code in charge of managing APCs could not allocate linked list nodes at runtime. Instead, any code that wants to schedule an APC has to statically declare (compile time allocate) a structure like this:

```markdown
typedef void (*ApcCallback)(void* context);
typedef struct Apc {
    ApcCallback callback;
    void* context;
    uint32_t delay;
    // Internal use only below this line
    *Apc previousApc;
    *Apc nextApc;
}
```

At the end of this article is a full example showing usage of APCs.

Band's usage of intrusive linked lists was an improvement over the original design where the dispatcher maintained its own fixed size ordered queue. The fixed queue size limited the number of APCs in system, and after bumping into the limit enough times we switched over to intrusive lists.

As an aside on the use of linked list, Band used SRAM with 1 cycle access latency, meaning linked lists were almost as fast as arrays, and as a result Band used them all over the place.

APCs themselves got used for everything on Band:

* The calendar reminder, just schedule an APC for whenever the next event should fire and pass in the event's details through the `context` pointer.
    
* Screen timeout, when the screen turns on, schedule an APC for *delay* milliseconds to turn the screen off. Every time the user touches the screen, abort the APC and re-enqueue it, thereby resetting the countdown.
    
    * If the user turns the screen off early, just abort the timeout APC
        
* The entire sunscreen reminder experience is just a handful of APCs that I designed the logic for in a couple of hours.
    

APCs with 0 delay are how all IO was done, after the IO finished up, a 0 delay APC was scheduled, which means as soon as the CPU was available, the results of the IO could be handled. No waiting on locks!

Until you have programmed with them, it is hard to explain just how powerful this concept is.

Returning to the dispatch loop, we can now understand that it was responsible for determining which Asynchronous Procedure Calls (basically functions that are called when a timer goes off) to run, [coalescing timers](https://en.wikipedia.org/wiki/Timer_coalescing) to save power on those APCs, setting hardware timers for waking up the CPU, and finally, controlling power states.

# Async IO with callbacks

Band did not allow blocking IO. Instead, IO worked by requesting an operation, and passing a callback that was to be used to notify of either the result or an error. This is a pretty common pattern now days, but back in 2014 we needed a non-blocking, no malloc, embedded filesystem that was resilient against power loss and data corruption (CRC's at minimum preferred) and we could not find one on the market. Multiple file system vendors outright told us what we wanted was impossible, their basic attitude was that asking for 100% non-blocking was insane, and that we must be fools[^2]. So we had one man on the team, Bob Lockhart (LinkedIn profile not available sadly), wrote a file system for us from scratch.

This is another topic I'll need to explore more of in a future post.

# Aggressive Sleeping

As mentioned above, Band used APC coalescing to save on power. Timer coalescing is common on mobile products, and in general it means if three tasks are scheduled close together; one in 10 milliseconds, one in 15 milliseconds, and one in 20 millisecond, rather than wake up 3 times in a row, just push the first 2 events back by a bit and run all three tasks 20 milliseconds from now.

For Band, the contract for scheduling an APC is that the APC would be called *no sooner than* its delay, but possibly an *indefinite time after* its delay. Band actually had maximum skew value of several milliseconds, so things never got too out of hand.

# Putting it all together

I'll now show some an example of what writing for Band was like. This code is by no means real, it exists to demonstrate the basic principals of programming with APCs. Business logic is simplified and edge cases are ignored.

The below code handles sun exposure reminders and is designed to remind people to apply sunscreen when they are outside. The spec for the feature is as follows:

1. Sun exposure is defined as a UV Index of at least 3
    
2. If the user has an initial 15 minutes of continuous sun exposure, fire off an alert reminding them to put on sun screen, then every 4 hours (in the actual product is was configurable from 90 minutes to 4 hours) after that show a reminder to re-apply.
    
3. If after sun exposure starts and an alert has been fired off, a continuous interruption in sun exposure for more than 10 minutes cancels the 4 hours reminder timer a. An interruption for less than 10 minutes does not reset the timer, (bathroom break at the beach) b. After the 4 hours timer is cancelled, subsequent 15 minutes of continuous exposure afterwards will fire off another initial alert
    

These simple rules are designed to prevent Band from reminding someone to put on sunscreen when they are walking from their car to go inside a store, while at the same time if someone is playing in the sun and goes to the bathroom, the system should track that as being part of a single session. It also will start a new session if someone is at the beach, sits down for lunch inside a restaurant, then goes back outside.

The code below is simplified from what was on Band, the actual Band combines reading from the screen's automatic light sensor (ALS) and the UV sensor to determine if the wearer is inside or outside, and on an actual Band reminder times were customizable.

The UI was codenamed Fireball (because we wanted it to be called something cool), which is why you see that mentioned in regards to the UI below.

Some things to note, the UV sensor takes in a callback an every minute it reports the current UV index to everyone who subscribes. This subscription system was based on C# events.

And again, apologizes for the rusty, likely very incorrect, C code.

```c
bool inited = false;
Apc uvInitialAlertApc;
Apc uvFourHourAlertApc;
Apc uvCancellationApc;

// Only show UV alerts if UV index is at least 3
// Cancel alerts if index falls below 3 for 10 minutes.
#DEFINE UVINDEX_ALERT_THRESHOLD 3

/*
structure that describes a subscription, future
blog post coming, if you know C# subscriptions 
you get the gist of it. When the UV sensors
reads a value, sends to all subscribers via callbacks.
*/
UvExposureSubscription uvSub; 

// Called on system boot
init() {
    if(inited) return;
    
    inited= true;

    uvInitialAlertApc.callback = &uvInitialAlert;
    uvInitialAlertApc.context = &GLOBAL_UI_CONTEXT; // Handle to UI framework
    uvFourHourAlertApc.callback = &uvFourHourAlert;
    uvFourHourAlertApc.context= &GLOBAL_UI_CONTEXT;
    uvCancellationApc.callback = &cancelAlerts;
    uvCancellationApc.context = null;
    uvSub.callback = &uvExposureHandlerInitial;
    
    // Subscribe to the UV module
    UvExposureModule_Subscribe(uvSub);
    return;
}

// Subscription handler from the module that calculates UV exposure.
// Every 1 minute UV module calls its subscribers and reports
// the detected UV Index.
void uvExposureHandlerInitial(uint8_t uvIndex) {
  if(uvIndex <= UVINDEX_ALERT_THRESHOLD) return;

  AbortAndEnqueue(uvInitialAlertApc, MINS_TO_MS(15));
  AbortAndEnqueue(uvCancellationApc, MINS_TO_MS(10));
  /*
  Next line changes what callback handles summing exposure values,
  in essence this is progressing  our state machine.
  */
  uvSub.callback = &uvExposureHandler; 
  return;
}

// Called every 1 minute after initial exposure
void uvExposureHandler(uint8_t index) {
    if(index >= UVINDEX_ALERT_THRESHOLD) {
      // Reset the cancellation APC to another 10 minutes
      AbortAndEnqueue(uvCancellationApc, MINS_TO_MS(10));
      return;
    };
    // If below alert threshold, do nothing, cancellation 
    // apc will take care of things.
    return;
}

// Will get called after 15 minutes
void uvInitialAlert(void* uiContext) {
  FireballUI_SendMessage((FbContext) uiContext, INITIAL_UV_ALERT);
  // On real Band, user was given choice after initial alert
  // if they wanted to receive future alerts.
  AbortAndEnqueue(uvFourHourApc, HOURS_TO_MS(4));
  return;
}

void uvFourHourAlert(void* uiContext) {
    // No need to check exposure threshold, if not cancelled, good to go
    FireballUI_SendMessage((FbContext) uiContext, SUNSCREEN_REMINDER);
    AbortAndEnqueue(uvFourHourApc, HOURS_TO_MS(4));
}

// This gets called if UV index has been below 3 for
// the last 10 minutes.
void cancelAlerts() {
  // We don't know which is runnign so abort both.
  // Aborting an APC that isn't scheduled is a no-op.
  AbortApc(uvFourHourApc);
  AbortApc(uvInitialAlertApc);
  // Go back to the initial uv handler, reseting our state
  uvSub.callback = &uvExposureHandlerInitial;
}
```

[^1]: When proposing APCs as our concurrency primitive I actually had to prove the need for dequeuing to the team, if you don't always dequeue first you end up in some strange situations regarding state

[^2]: Now days multiple open source solutions exist that fulfill all these requirements
