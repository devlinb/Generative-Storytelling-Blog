---
title: "You (Probably) Don't Need Server Side Rendering"
slug: "you-probably-dont-need-server-side-rendering"
date: "2023-04-25T07:08:34.416Z"
lastmod: "2023-07-11T20:52:19.801Z"
author: "Devlin Bentley"
description: "Disclaimer: This post is explicitly talking about running JavaScript UI frameworks such as React and Vue server side to generate single-page applications. It is not about traditional MPAs, or using Go/Python/Ruby/etc. This post is specifically in res..."
tags: ["SSR", "Server side rendering", "ssg", "Nuxt", "Next.js"]
draft: false
sourceURL: "https://meanderingthoughts.hashnode.dev/you-probably-dont-need-server-side-rendering"
---

Disclaimer: This post is explicitly talking about running JavaScript UI frameworks such as React and Vue server side to generate single-page applications. It is not about traditional MPAs, or using Go/Python/Ruby/etc. This post is specifically in response to currently popular advice that new projects should be SSR+SPA first and that they should split UI JavaScript code between the server and client.

**tl;dr** SSR is a micro-optimization that is not necessary for the majority of small and medium-sized projects. It is being promoted by hosting companies that don't want to be in the low-margin business of serving up static assets. At its most complicated, SSR involves creating and scaling a backend that maintains user state and also does HTML generation, which is sweet $$ in the pockets of companies that otherwise would just be serving up static index.html and index.js bundles. Even minimally invasive uses of SSR add complexity to your build step, and application logic, and may prevent you from having simple static delivery of your HTML.

# Why UI Framework SSR is (probably) not for you

If you are reading this article, then presumably you know what Server Side Rendering is. But let's ensure we are all on the same page, and there are a few different types of SSR after all.

Modern UI framework SSR is attempting to recreate the SPA experience by assembling HTML on the server and sending it to the client by running the same JavaScript code that would typically run in the browser. The more advanced SSR frameworks will track large amounts of state server side to fully replicate a SPA experience. In the most extreme cases, every keypress in every form field gets streamed to the server.

In its most basic form, SSR is used to do two things:

1. Create an initial DOM tree (so browsers w/o JS, and web crawlers, have something to see)
    
2. Have the server make API calls needed for initial rendering (e.g. fetch user profile data), under the (fair) assumption that the web server has lower latency to the API server than clients do.
    

As part of the initial bundle of HTML/JS that gets sent down, a SPA framework (e.g. React) hitches a ride and takes over after the page has loaded. This form of SSR can be "just enough" to solve SEO problems and improve initial page load, and I take less issue with it.

The advertised benefit of SSR - the website is faster because the server can assemble everything needed all in one place and send the final results down to the client - is real it is the singular unique benefit that SSR can deliver. If you have a lot of API calls you need to make before you can display anything to the user, and if the API servers are co-located with your web hosting servers, then you reduce latency for these API calls.

This is the big win SSR gets you. To belabour the point: well-designed home/landing pages should not require any API calls before they display some content, and ideally the first page a user loads on your site is a static asset loaded from a cache of some sort. (A static page served from a cache can handle more traffic than most companies will likely ever see!) If you need to make a bunch of expensive API calls before you can show anything, then you have already gone down a dark path and SSR is a band-aid on top of a gushing wound. That said, sometimes you need to do whatever you can, and if SSR is the only hope you have for making your website perform well, sure, go for it. (An example is cellular provider websites, at least one of which I know used to look up how much your house was worth and how much you were paying each month on your mortgage, to decide if the splash page showed an Android or an iPhone, if that is your life, SSR may very well help, but a confessional of some sort may also be needed)

But if you are starting a brand new project, focus on shipping first, and look at SSR as an optimization that can come later *if* you need it.

# The problems with SSR

Listen, if you are a startup or a small business, or even a medium-sized business, your web server is probably less powerful than a 3-year-old mid-range Android phone. Your server is likely a VM, it has maybe a couple of cores and a few gigs of RAM, it is not a compute beast. However the machine is likely tuned for IO throughput, it is connected to a giant NIC and has an SSD hooked up to it. SSR is going to try and make your web host do something it is bad at, charge you a lot of $ for it, and ignore decades of improvements in client computing.

## Clients as dumb terminals

Some CPU, somewhere, needs to append a bunch of strings together to make a valid HTML document, and browsers are optimized for manipulating the DOM, it is the thing they are good at. Not great, but good enough. However, the fact is string manipulation is *obscenely* CPU intensive, and SSR asks your web server to do it for everyone who visits your site. Appending strings together is thousands upon thousands of times slower than doing math. Asking a server to run a JS framework and burn CPU cycles to generate the HTML, and in extreme cases, maintain state, for each user connected to your site is a waste of resources, especially given the marginal benefits you are getting for your trouble and expense. Problem #1 is that at its most extreme, SSR treats browsers as dumb terminals.

## Shared state stomps all over good software engineering practices

Speaking of state, there is a principle in software engineering called having a single source of truth. SPA + microservices architecture is great because the client browser has all the state, and it sends messages to stateless functions that process the message and return some result. This is ideal! Stateless functions are cheap and easy to scale, and unless you completely screw up your database, odds are a single hosted instance of PostgreSQL will scale up to tens of thousands of queries per second, which means if you have competent management, you're company/project should reach profitability before you run into DB scaling issues.

This simplicity + scalability + affordability is why so many companies have chosen SPA + microservices.

More extreme forms of SSR ignore all of that, and instead, opt to have state on the client and the server. At its worst, SSR can require the webserver to scale with the number of clients because now the web server is running React/Vue/Svelte code!

Just as a reminder, React is a framework wherein it is trivial to accidentally write code that causes the entire page to redraw with every letter typed into an input field, consuming 100% of an entire core just to type in an email address. This is not a theoretical concern, I've seen many major sites with that bug in production, and I myself have written React code that behaved almost as badly (oops!). With SSR you are adding yet another part of your backend that needs to worry about scaling up.

That is problem #2 of SSR, it replaces a system that uses minimal CPU, has easy to manage state, and that scales well, with one that consumed additional CPU for every user and splits state across multiple locations, while increasing your hosting costs.

### We tried this before and it sucked, stop repeating history

Hey kids, let me tell you about this era of the internet called the late 90s/early 2000s. We did something resembling SSR back then, it sucked. Pages took seconds to render, and the more users who visited a website, the longer the page took to load.

Except back then it wasn't even as extreme as it is now, no one was trying to open persistent connections between browsers and servers to send data back and forth constantly, the poor server CPUs we had back then would have melted if anyone had tried anything that inefficient.

History lesson: before Reddit, there was another website called Slashdot that originally invented users voting on comments and stories and such, and it was slow, dog slow. When reading comments, the server had to assemble all the HTML around each comment, instead of just sending down a text payload and letting the browser handle rendering. At 2 am the website was fast and at 5 pm when everyone got home from work/school/etc the website was slow.

The current bloated version of Reddit is still worlds better than websites that came before it.

You may also remember back when servers contained session data, e.g. for a multi-page checkout form the server would keep track of what had been entered so far. Of course, server resources aren't free so servers had to time out sessions after a while to free up resources, this meant if you were buying something and you stepped away from your computer for a bit, the site would forget about you when you came back and you'd have to start the process all over again. It was bad UX then, and it demonstrates the dangers of storing session data on the server.

Problem #3: reinventing history, but worse.

## It adds mental complexity

Finally, SSR adds complexity. What gets rendered where? Some things get rendered on the server, some get rendered on the client, and if the client loses connectivity, well now you get to deal with fallback code that tries to have the client do what the server was doing.

When everything is client side a loss of connectivity isn't a big deal, it is super easy to retry an [idempotent](https://en.wikipedia.org/wiki/Idempotence) JSON fetch when connectivity gets restored. Think this is a theoretical problem? Every time I go out to eat at my favorite Cambodian restaurant in Seattle I get seated behind a pillar that somehow blocks almost all cell service, every time I want a site to load I have to lean forward before I navigate to a new page. More mundane, every time I walk outside my house and down the block a bit my phone does a poor job of switching from Wi-Fi to cellular and everything on my phone loses connectivity for a bit.

By relying on the server for some UI logic and the client for other UI logic, you have added complexity that will break down as soon as the user goes off the golden path.

That is problem #4, SSR replaces a system that works, with a dramatically more complex system that only has one benefit, but a lot of downsides.

# So who is benefiting from SSR?

Let me repeat, for large complex sites, SSR can make sense.

For tiny websites? No one benefits but cloud providers. They are actively funding SSR projects, they put out lots of training videos on making SSRs, and they employ software engineers who are promoting SSRs. They are the ones responsible for all those "getting started with &lt;....&gt;" tutorial videos and articles.

And it is dangerous to the open-source community. I've seen backend libraries that only work with Next.js, for no good technical reason! Foundational libraries should be framework agnostic, with framework wrappers created around them, doing otherwise creates vendor lock-in. Imagine if moment.js/date-fns only worked with React! That is silly, instead, you create react components that wrap independent libraries. That sounds ridiculous, but there are an increasing number of non-UI libraries that are Next.js first.

SSRs do have their place in very complex sites. But if you are at the stage where you are using an `npm init` website template project, you do not need SSR.

Remove advertising bloat, use a bundler that supports delay loading modules you don't need right away, and ensure your design can show something to the user w/o needing to hit a bunch of endpoints.

React is 40k. Svelte is almost 0k. Vue is 58k. If your website is slow, it isn't because of your framework. It might be because you imported 2 megabytes of Google Fonts, or 4 megabytes of SVG icons, and yes SSR is a workaround for many types of import stupidities, but there are lots of workarounds for doing the wrong thing, including *doing the right thing*.

# Bonus: points of rebuttal

## Using SSR just for initial page load (hydration)

This nets the largest win, you only have to deal with the complexity surrounding your initial page load logic, and if your site is completely dynamic it solves the SEO problem. This is a reasonable use of SSR.

## Code Splitting

You can do this with SPAs. It requires carefully designing your app so larger libraries aren't pulled in until they are needed (or right before they are needed), but doing it with SSR is also extra work.

## Modern frameworks are faster than in the past

Indeed, the days of PHP scripts that take 3 seconds to render a page are, mostly, gone. But even if you can make SSR scale perfectly, you are still adding complexity to the already incredibly complex web development stack, for what is likely marginal benefit. "Because we can" shouldn't be the sole argument to deploy customer-facing technology. (For personal projects, go for it!)

## Internal business web app that will only ever have 20 concurrent users

Some developers really like technology like Phoenix LiveView (note: not JS based on the backend), and it helps them write web apps really fast. For internal LOB apps, use whatever technology gets the job done. The 90s were powered by Visual Basic and Microsoft Access and by most measures the business productivity gains of "Getting Shit Done(tm)" is more important than idealism.
