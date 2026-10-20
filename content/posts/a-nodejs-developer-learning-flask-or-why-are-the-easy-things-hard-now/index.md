---
title: "A NodeJS Developer Learning Flask - OR - Why Are The Easy Things Hard Now?"
slug: "a-nodejs-developer-learning-flask-or-why-are-the-easy-things-hard-now"
date: "2023-10-18T07:00:09.275Z"
lastmod: "2023-10-18T15:33:12.723Z"
author: "Devlin Bentley"
description: "So I decided to learn Python again. The last time I seriously dove into Python it wasn't even at version 3 yet, so it has been a while.\nI am a big believer that the best way to learn a language is to make something you are passionate about in the lan..."
tags: ["Flask Framework", "Node.js", "Python", "JavaScript"]
draft: false
sourceURL: "https://meanderingthoughts.hashnode.dev/a-nodejs-developer-learning-flask-or-why-are-the-easy-things-hard-now"
---

So I decided to learn Python again. The last time I seriously dove into Python it wasn't even at version 3 yet, so it has been a while.

I am a big believer that the best way to learn a language is to make something you are passionate about in the language, so I am making another cool LLM thing, this time a town simulator.

The tl;dr is that a fantasy town is being simulated with town residents but also an adventurer who goes off and does things, and visitors to the site can vote on what the adventurer does next by way of a poll on the homepage.

## Getting Started

Writing a REST API service in NodeJS is simple because that is the one thing Node is *really* good at. For anyone reading this who isn't familiar, a full NodeJS service with CORs looks like this

```typescript
import express from 'express'; // Webserver
import { Router } from 'express'; 
import healthcheck from './routes/healthcheck';

const corsOptions = {
  origin: 'https://www.generativestorytelling.ai/',
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Accept', 'Authorization'],
};
app.use(cors(corsOptions)); // enable cors
app.use(express.json());  // Automatically de/serialize from/to JSON

const app: express.Express = express();
router.get('/healthcheck', healthcheck); // Pass the function in that'll handle this endpoint
app.use(router);
const server = http.createServer(app);

server.listen(3000); // Start up a web server on port 3000
```

Two key things to notice here: the router takes in a function to handle the route, and this creates a full server, you are done, finished, that is it.

Python+Flask doesn't do this.

Disclaimer: The below is the result of about 1 week of playing around and I may be horribly wrong about some things.

First off, if you define your route handler in the same file as your router, you can just pass in a function. However, if the handler is defined in a different file, you have to pass in a blueprint. I am not sure why it can't just take the function in.

Second off, you have to use a separate server. Flask doesn't have a built-in server.

Third: apparently most things in Flask are synchronous blocking calls (?!?), and that server you hook Flask up to handles creating threads/processes so you can scale.

Again, for those unaware, a single NodeJS server running on the cheapest VPS you can find will easily obtain mid-100s of RPS. Put NodeJS on a not-horrible server and you can reach 1k RPS w/o too much worry, assuming you aren't shoving a compute bound load onto Node. (Please don't use NodeJS for any actual computations...)

## Creating a Poll

Now back to the poll feature.

In NodeJS, this is *trivial*. So long as I only need 1 instance of Node running (and again, for up to ~300+ people hitting that poll per second I will be fine), I simply use a global counter and write the following code

```typescript
import express from 'express'; // Webserver
import { Router } from 'express'; 
import healthcheck from './routes/healthcheck';

const pollOptions = {
    option1: number;
    option2: number;
    option3: number;
}

const corsOptions = {
  origin: 'https://www.generativestorytelling.ai/',
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Accept', 'Authorization'],
};
app.use(cors(corsOptions)); // enable cors
app.use(express.json());  // Automatically de/serialize from/to JSON

const app: express.Express = express();
router.post('/votePoll', (req) => {
        const vote = req.body();
        switch (vote):
            case "option1": pollOptions.option1++; break;
            case "option2": pollOptions.option2++; break;
            case "option3": pollOptions.option3++; break;
    }
 ); 
app.use(router);
const server = http.createServer(app);

server.listen(3000); // Start up a web server on port 3000
```

Because Node is single threaded and single process, that is *completely safe code*. A request will come in, increment a poll option, and return.

Done. Finished. Kaput. Ideally, I'd write a timer so that every 60 seconds I'd do a writethrough to an S3 bucket to preserve the value. That is literally *5* more lines of code.

### What about in Python+Flask?

Because there are multiple threads+processes some sort of synchronization scheme is needed. This is going to have a (tiny I hope) performance overhead, and also result in a lot more code. I have yet to decide how I am going to do this feature, but I do know that I am unhappy that doing something so simple is going to be a lot more work. Researching solutions I have seen repeated suggestions to just run a local DB and save the value there. Which honestly... just hurts. Megabytes of code and another process running just to store 3 numbers. Absurd.

And I'm sure experienced users of Flask would be able to get such a thing setup in just a few minutes, but oh my word it seems like so much work for such a simple thing.

### This Goes Back to Microservice First Thinking

People laugh at microservices, but if I really wanted to get a poll feature out right away and w/o worry, I'd spend all of 15 minutes developing it in NodeJS, have next to no dependencies (aside from wherever I am writing through to as a cache), and for the vast majority of loads\[1\] it could run as a standalone service on an existing VPS for literally 0 extra cost. For you k8s folks, it'd be a pod with 1 instance, assigned 0.1 CPU and 256MB of RAM (I've run NodeJS services in production that never went above 140MB of RAM, it isn't hard!)

But Flask isn't about that. Flask is about doing a *lot* of things, and I presume they figure you are likely to have a DB in there someplace, so not allowing (ab)use of global variables across requests is fine, just use the DB you already have! For the problem-solving style Flask developers are using, this is the correct mentality. If you look into it, Flask has a bunch of built-in support for serving up HTML files on routes, caching HTML files in memory, and doing other cool stuff that NodeJS *doesn't even want to do*. (Of course you can serve HTML files with Express, but it lacks Flask's niceties for doing such, and it really isn't something Express is meant to do w/o some extra libraries layered on top.)

## Final First-Week Impressions

I'd be done by now if I was writing this in NodeJS.

The single-threaded single process async everywhere mentality is incredibly simplifying for large swaths of problems. Thus that [entire embedded runtime](https://hashnode.com/post/clfwuvlkx000509jv8izzedhf) I helped build on those principles.

Of course, if I had to scale out the NodeJS solution, I'd end up with something resembling what Flask requires, but while I'll admit that, I also believe that simple things should be simple, and hard things should be possible. Flask is making this simple thing difficult, while seemingly focused on making the hard things less hard.

It is a trade-off that we see all the time in software engineering, and it can be argued that any sufficiently complex framework or tool eventually grows to this point. From Jira (or any other task management system) to languages like Rust\[2\] and C++.

IMHO the NodeJS ecosystem has remained laser-focused on simplicity. People complain that the JS ecosystem itself iterates too quickly (arguable, sometimes true, there is no way I'm trying to bring up frontend code from more than 2 or 3 years ago...), but the backend JS ecosystem hasn't changed much over the years and that is a good thing.

[^1]: Unless you try to [name a boat](https://en.wikipedia.org/wiki/Boaty_McBoatface)

[^2]: Related, doing multiple threaded stuff in Node is a lot more work. Yes, you can do it, but it isn't ergonomic, and it doesn't have the built-in safeguards like Rust does for preventing various race conditions.
