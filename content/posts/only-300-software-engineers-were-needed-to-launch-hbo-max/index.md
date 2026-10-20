---
title: "Only 300 software engineers were needed to launch HBO Max"
slug: "only-300-software-engineers-were-needed-to-launch-hbo-max"
date: "2024-01-11T22:00:42.786Z"
lastmod: "2024-01-11T22:18:23.255Z"
author: "Devlin Bentley"
description: "(As with any of my posts this is all from memory and I was an IC at HBO Max and numbers are just hearsay I heard from other engineers)\nHBO Max launched as a nation's third largest streaming service with only 300 software engineers on staff. The app l..."
tags: ["HBOMax", "video streaming"]
draft: false
sourceURL: "https://meanderingthoughts.hashnode.dev/only-300-software-engineers-were-needed-to-launch-hbo-max"
---

(As with any of my posts this is all from memory and I was an IC at HBO Max and numbers are just hearsay I heard from other engineers)

HBO Max launched as a nation's third largest streaming service with only 300 software engineers on staff. The app launched on all available platforms, and a few months later scaled an entire order of magnitude when popcorn movie releases got redirected from theaters on to streaming.

Expanding internationally to Latin America and Europe the back end service team grew minimally.

The ratio of TPMs to engineers was around 10:1 and engineers actually requested more TPMs be hired.

The organization was incredibly flat, as I recall only four layers, and the leader of the entire organization was highly technical and participated in architectural discussions and reviews.

# How

This was all made possible by incredibly powerful tooling that allowed for bringing up a new service and little as 3 days. A single command would setup auto scaling, secrets management, network configuration for service endpoints, and a build pipeline.

Because services were so easy to set up there was no worry about deprecating old broken out of date code and the simplest solution to a problem was to experiment with new code and a new service. Rapid iteration was the name of the game and the small team size meant that communication was smooth and without conflict. Communication was greatly aided by the number one hiring criteria within HBO Max: don't hire people who aren't nice to work with. Any mention of ego or bad mouthing previous teams or coworkers was an almost instant guaranteed no hire, no matter how good someone did technically.

Teams freely went into each other's code to add features and fix bugs and not once did I see politics crop up to prevent work from getting done.

The tooling and the culture combined together to make an incredible place to work.

There's a separate discussion about the quality of the initial streaming apps HBO Max launched with, but I will just say that writing good code across the fragmented streaming media device market is hard unless you have spent years investing in the technological foundations needed to pull off such a feat.

In the first year we operated my team had two on call incidents. The next year sadly saw another two or three all bunched up together, which made me sad as that ruined a good 9+ month streak of nothing breaking.

As a testament to the quality of infrastructure HBO Max was built on, after the merger with Discovery the HBO Max infrastructure continued to work running on its own with no intervention and only one on call engineer per week per business area.

HBO Max had a true CI/CD pipeline. Changes, once approved, were deployed after having passed integration and end to end tests, typically within a couple of hours after having been committed. Teams deployed multiple times per day and the organization itself pushed out hundreds of changes to prod on any given day of the week except for Friday.

There were no Open API specs, no protocol buffer definitions, just teams communicating with each other to ensure code kept working.
