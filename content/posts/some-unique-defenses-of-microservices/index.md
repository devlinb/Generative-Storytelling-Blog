---
title: "Some (unique) Defenses of Microservices"
slug: "some-unique-defenses-of-microservices"
date: "2022-12-09T07:47:26.397Z"
lastmod: "2022-12-22T23:27:45.125Z"
author: "Devlin Bentley"
description: "Intro\nMicroservices have become a widely used architectural approach for building and deploying applications. However, there has been a recent backlash against this approach, with many people arguing that microservices are nothing more than an antipa..."
tags: ["backend", "Microservices", "Programming Blogs", "Software Engineering", "software development"]
draft: false
sourceURL: "https://meanderingthoughts.hashnode.dev/some-unique-defenses-of-microservices"
---

# Intro

Microservices have become a widely used architectural approach for building and deploying applications. However, there has been a recent backlash against this approach, with many people arguing that microservices are nothing more than an antipattern brought about by consultants. In this post, I aim to show that microservices are a valid, and valuable, technique for handling complexity. I hope to do this by highlighting some not as often discussed benefits of microservices.

I hope this post provides a bit of a different take on the benefits microservices. Instead of being written from a blog spam POV, I'm writing it as someone who is part of a mid-size team of engineers who work on a massive, globe spanning, service.

Upfront, I'll say that microservices are not the solution to all problems, or for all teams, but I believe the current backlash against them is, in many ways, unwarranted. I also think that there are advantages of microservices that aren't often talked about, which I hope to highlight in this post.

I'll start out with going over some benefits of microservices, and then to add some balance, I'll go over some of their disadvantages.

# Where I am coming from

My first encounter with microservices was when I joined my current software engineering org. The tl;dr is we launched one of the nation's largest domestic streaming platform with a bit under 300 engineers, running on top of several dozen microservices.

Prior to that I was technical founder of a startup that was built around serverless, running on Google's Firebase platform. Prior to that, I was at Microsoft for around a decade, working on a very (very) wide variety of technologies.

# Benefits of microservices

## Updating dependencies is easier

To me, this is one of the largest but rarely talked about benefits to microservices.

Updating dependencies in a monolith can be a Stop All Development event. Large enough changes can require so many updates to code that development may have to stop for weeks at a time so the necessary work can take place. Oftentimes only the most critical of security issues are ever addressed. Even for well maintained monoliths, there will be significant organizational pushbacks to updating any part of the technology stack. (Don't believe me? How many projects are stuck on old versions of Java?)

Now, compare that to how breaking changes in dependencies are handled in a company that uses microservices:

1. A team with a bit of extra time in their schedule goes through the pain of updating one of their services

2. That team documents what they learned, and may possibly write some tooling to help other teams through the process

3. As teams have time in their schedule, and also organized by which services are most at risk from not updating, microservices are updated one by one

Alright, how about switching to a new version of tooling, such as a new version of TypeScript or the JVM?

Easy!

1. Newly created services use the latest stable version of tooling

2. Existing services are allowed to not update until their runtime is no longer on the LTS support list

This means an organization is rolling along with new services getting the benefits of the latest tools, while other services are humming along on LTS tooling until someone has time to update them. Because each service is, ideally, small, updating and testing for compatibility with new tooling/runtimes, is not a huge task.

Again, to me this is one of the biggest benefits of microservices! Having the ability to regularly update dependencies across an entire organization, and being able to roll out the latest tools.

As a real life example of this, I suspected a new service I was creating would benefit from the latest AWS SDK, which also required a newer version of TypeScript than the org's microservice template supported. I created a new service and rev'd everything to the new version of TS, then committed my changes to the new service's repo. I was able to report to our tooling team what broke (nothing!) and that gave them one more data point when they went to update the new service template to use the latest TypeScript. I was also able to document and write up the benefits from using the new AWS SDK (major reduction in in CPU usage!) and share that information with the organization.

Because each service has its own build scripts, dependencies, and tooling, teams are free to experiment as needed to find the best solution to their problems. And on that note:

## It is easy to experiment with new technologies

When my org wanted to switch over to a different backend test framework, it was a simple matter of changing the new service template to use a different test framework. New code going forward got the new hotness, old services could be updated as teams saw fit.

This naturally leads into the next point:

## Each microservice can use the best technology for its problem domain

Doing lots of binary data processing? Write your microservice in a language that can juggle large binary data blobs w/o issue. Interfacing with a ton of external services using JSON? Write your microservice in JavaScript or Typescript. Need to do some ML? Pick your favorite language.

In the world of microservices, only the interface boundaries matter. You can completely replace the codebase of a service as long as the HTTP endpoints, input data, and output formatting remain the same. This means that services can be implemented in different languages, such as Java, Python, or Rust, without affecting the rest of the system. In contrast, a monolithic architecture typically limits the ability to mix and match different languages and technologies.

Perhaps less extreme, each service can use whatever programming paradigm is a good fit. Some problems are best modeled with OO, others are best met with a pure functional approach. In a single monolithic application it would be strange to have a file with a comment at the top Pure Functional Code Only In This File. You can do that, but it isn't natural.

## They enforce a paradigm

I'll write more about my thoughts on programming paradigms in the future, but the tl;dr is that programming paradigms are a way to limit what programmers can do, thereby making understanding the code easier.

Quick and dirty example, functional programming doesn't allow mutation of global state in pure functions, meaning you don't have to go around hunting for who is changing variables, sources of mutations are very limited, perhaps the code is pure FP and there is no global state and all code is perfectly composable with no fear of side effects.

That is a limitation that simplifies code maintenance. Functional programming doesn't enable anything new, it restricts what is possible. Same goes for Class Based OO's forced marriage of functions to objects, it is a limitation that, in theory, makes understanding the code base easier because there are less things that could potentially be going on.

Microservices are also a paradigm, they force certain patterns and behaviors onto programmers, thereby limiting the complexity of the code base in some ways, while adding complexity in others.[1]

In my opinion the two largest positive results of microservice design are as follows

1. Extreme separation of concerns, the billing service is going to do billing and nothing else, and if it needs any profile data, you know it is going to be making an API call to the profile service.

2. API interfaces have to be thought of up front, hopefully encouraging reusability

That extreme separation of concerns is amazing, but combine it with the enforced need to plan out API interfaces up front, and backend systems now become composable by default. That profile service isn't coupled to billing, that billing isn't coupled to the code that emails customers. By splitting the code up, by adding hard API boundaries, you force programmers to rethink how the entire system is engineered.

Now are microservices required for this? Of course not! And you don't need to use a functional language to gain the benefits of functional programming, and you don't need to use an OO language to gain the benefits of encapsulation.

But microservices force this paradigm, even when you don't think you'll need it. Instead of creating a class that emails customers a billing receipt, you write a service that emails customers, and there is a hard API boundary, potentially a literal boundary involving a network cable (though more likely a virtual network card), that makes you completely separate those two things out. 

Then, when someone else comes along with a new use case for emailing customers, you can extend that email service out in a well defined way.

This is insanely powerful! Sure maybe in your monolith that class that emails users was well designed and easy to extend, or maybe not. Maybe someone extended the class out and now you can't change too much about the base class, and 3 years later moving people to a new email service that fixes inherited tech debt is a massive refactoring effort.

With microservices, none of that happens, everything is a black box to a far greater extent than even OO purists could ever have dreamed of.

## Each microservice can scale appropriate to its needs

Scalability is the big reason why people love microservices. I'll say it up front:  Unless you are working at a company that processes 100k+ events per second, don't use microservices. If you are dealing with only thousands of operations per second, please, write good code, and run everything on one VM. Odds are the database system(s) will be a bottle long before your service code is.

But, once you start hitting hundreds of thousands of operations per second, odds are scaling up your monolith to just more copies of your monolith is not an efficient way to do things.

Different parts of complex software systems need to scale based on different criteria, and with microservices, each service can choose its own scaling criteria.

For example, my day to day job involves working on a fancy queue processor. We scale up based on queue size!

In comparison, a user login service, upon detecting a high load, may opt to spin up a bunch of instances of in-memory caches of profile data, pick some good sharding scheme and direct login attempts to an instance of the service attached to the appropriate shard. Because that profile service stands alone from the rest of the system, this is possible! Even as website users, we've all encountered monoliths where the profile service was the first to fall apart, logins taking multiple seconds, or just timing out entirely. With microservices, the scaling story for each service is designed up front, which naturally leads to a design where each service has its own independent data stores[2], which can also be scaled independently.

# Why Not Microservices?

In an attempt to steelman the other side, I'll start by describing some of the downsides of Microservices

## Harder to manage deployments

Yes, 100% true. If all your backend traffic needs can be handled by a single medium powered, or beefy VM, in a single data center, then the complexity of deploying Microservices is probably not for you. Creating and managing infra for microservices is almost a complete sub-discipline. It can be obscenely complex compared to "deploy binary to a beefy VM in 3 different regions, setup up geo based routing".

## Harder to manage cross cutting dependencies / refactor

Also incredibly true, making breaking changes to even just internally exposed APIs is much harder with microservices, and often may not even be worth the bother. It is often easier to just version the entire API endpoint than try and update all existing callers in a well ordered fashion.

In a similar vein, type safety is much harder to ensure. If you are using JSON, you need some sort of type safety client libraries that your services use to call each other. If you are using something like gRPC, well gRPC is not a type safe schema language, so you still need something application layer on top that does real type checking. At some point you start investing in either home grown solutions, or looking at projects like OpenAPI.

## Unnecessary Overhead

Passing everything around as JSON over HTTP is, let's be honest, a huge waste of resources. Even using a binary encoding format like thrift or protobufs is still a huge waste. What could be a single function call that takes microseconds is now going to be an HTTP call that takes milliseconds at minimum, not to mention the dozens of function calls needed to receive the packets, route to the proper endpoint, and then parse the data out. You are losing orders of magnitude of performance.

# Summary

I hope I've made explained some reasons why microservices are not to be demonized. They have trade-offs and disadvantages for sure, but they also have some significant advantages as well.

# Footnotes

[1] IMHO All paradigms make this trade off, for example Rust's memory safety paradigm makes certain data structures really hard to express

[2] Of course you could do a microservice architecture where all the services talk to the same database, but why would you?
