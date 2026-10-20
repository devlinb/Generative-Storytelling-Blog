---
title: "How Microsoft Tested Compilers Circa 2006"
slug: "how-microsoft-tested-compilers-circa-2006"
date: "2022-12-28T07:27:17.559Z"
lastmod: "2022-12-28T17:50:30.479Z"
author: "Devlin Bentley"
description: "My first job out of college was working on the Windows Mobile Compiler Team (which had previously been the Windows CE compiler team).\nA warning, everything in this post is from memory, and old long-term cached memories at that, so some numbers may be..."
tags: ["compilers", "compiler", "C++", "ARM", "mcu"]
draft: false
sourceURL: "https://meanderingthoughts.hashnode.dev/how-microsoft-tested-compilers-circa-2006"
subtitle: "And how a team of 3 testers ran over 3 million tests a week"
---

My first job out of college was working on the [Windows Mobile](https://en.wikipedia.org/wiki/Windows_Mobile) Compiler Team (which had previously been the [Windows CE](https://en.wikipedia.org/wiki/Windows_Embedded_Compact) compiler team).

A warning, everything in this post is from memory, and old long-term cached memories at that, so some numbers may be a bit off, and details not exactly right, but the gist of things should be correct.

The team consisted of 4 developers and 4 testers, the dev team was 1 lead dev, 2 senior devs, and 1 junior dev, the test team consisted of a non-technical manager who also managed another team, 2 senior SDETs, a vendor, and myself. (I honestly don't recall if we had 2 senior SDETs or just one senior SDET...)

The 8 of us were responsible for the backend code generation for the following CPU platforms:

* SH4
    
* MIPS16
    
* MIPS III/IV/V
    
* ARMv5
    
* ARMv6
    
* StrongARM
    
* Thumb16
    
* Thumb-2
    

And possibly some others I am forgetting.

To maintain the quality bar one expects of a compiler, especially one shipping in the embedded space, and a compiler that came with a 5+ year support agreement (if you paid the extra $), the team focused a lot on testing.

# How do you test a compiler?

To test most software, you ask it to do a thing, the program does that thing, and you check if the output of what it did matches the expected output. But with compilers, the output is machine code, and what exact code is generated is always changing based on new optimizations.

In reality, for the majority of compiler functional testing (lots of exceptions to this!), you don't care about what exact code the compiler outputs, you just care that the code it outputs performs correctly. For example, if you are compiling a JPEG compressor, the JPEG compressor should, once ran, always output the same images no matter what compiler optimizations are applied. (ignoring opt-in fast math libraries, SSE vs x87 FPU, etc).

So to test a compiler you compile a bunch of programs that do complicated things, and you run those programs, and make sure they still do those complicated things correctly. Physics simulations, compression algorithms, A/V codecs, encryption, those sorts of things are the perfect way to test that compiler changes don't break real-world code.

This is just a general overview, there are of course many other types of compiler tests, diving into the depths of [ABI](https://en.wikipedia.org/wiki/Application_binary_interface) adherence and calling conventions, correctness against the C and C++ standards (there are industry standard test suites that have tests for almost every single line of the various C standards), and plain old fashion stress tests. Negative tests also exist, ensuring the compiler doesn't accept code that looks "almost" valid.

# 3 million tests?

Here are the steps to generate a test run:

1. Select which instruction sets you want to test generating code for, e.g. say we want to test ARMv4 and MIPS16
    
2. Select which sets of compiler flags you want to test with, imagine we want to test with the following compiler flags:
    
    * `/o2 /gw` `/o1 /EHc /GF`
        
3. Select which sets of linker flags you want to test with, again imagine we choose:
    
    * `/LTCG /OPT:NOREF` `/INCREMENTAL /DEBUG`
        
4. For each test, run it using all combinations of the above architectures, compiler, and linker flags. For the given example here is what each test would compile/link with:
    
    1. ARMv4
        
        * `/o2 /gw` - `/LTCG /OPT:NOREF`
            
        * `/o2 /gw` - `/INCREMENTAL /DEBUG`
            
        * `/o1 /EHc /GF` - `/LTCG /OPT:NOREF`
            
        * `/o1 /EHc /GF` - `/INCREMENTAL /DEBUG`
            
    2. MIPS16
        
        * `/o2 /gw` - `/LTCG /OPT:NOREF`
            
        * `/o2 /gw` - `/INCREMENTAL /DEBUG`
            
        * `/o1 /EHc /GF` - `/LTCG /OPT:NOREF`
            
        * `/o1 /EHc /GF` - `/INCREMENTAL /DEBUG`
            

With this very small set of architectures and flags, every single test is going to run 8 times. A typical test run could easily have 6 architectures, 4 or 5 sets of compiler flags, and another 3 or 4 sets of linker flags.

That is how we ended up running millions of test cases per week.

# Inventing Distributed Computing Before It Was Cool

Microsoft was a pioneer in advanced test systems that distributed a large number of tests across network-attached machines, but the tool the WinCE compiler team used was way beyond anything that existed in the company at the time.

Made by one engineer, who rightfully got promoted to senior afterward (and who promptly left the team, opening the headcount for my hiring), the tool, called CLTT (Compiler Linker Testing Tool), was one of the most advanced testing tools I've ever had the pleasure of using, while also being coded to one of the strangest coding standards I've ever seen.

## What Made It Cool

3 million tests, over 90% code coverage. Remember this was before SSDs, heck it was before multi-core CPUs. What's more, we didn't have accurate emulators for most of the platforms we were testing on, (even virtual machines were a new concept at the time) so a very large percentage of the tests ran on various non-x86 hardware.

Remember, a compiler test is: compile a program; run that program; verify the output of the program is correct.

3 million tests, running on a wide (wide!) variety of different hardware platforms, how was that possible?

The answer is CLTT's insane, distributed, self-healing architecture. It looked something like this:

1. A lab full of ~50 Windows PCs, running actual Windows installs, each had a CLTT client app running on them ready to receive commands
    
2. A few dozen hardware test devices encompassing the different CPU architectures we supported
    
3. A network-controllable USB switch that allowed connecting any of the test devices to any of the lab PCs
    
4. A pretty good ARM emulator
    

That starts to cover the distributed part of things, so what did I mean by self healing?  
To understand that, let's first go over what a test run is in more detail:

1. A test run is defined with a set of compiler and linker flags
    
2. A test suite is a collection of tests, a test suite can override the compiler and linker flags of the test run. (I don't recall all the details here, the system was obscenely flexible)
    
3. A test case is a bunch of source files and also whatever the execution command was that should be run after compilation, again IIRC test cases could have pre-test steps that did stuff (e.g. generating source files on the fly) and may have also had the ability to override flags. Test cases also contained metadata about what platforms the test could run on, did that test support being run in an emulator, and so forth. Finally test cases had cleanup logic to reset the test machine back to a known good state (tests could literally do anything and some of them did quite a lot!)
    

When a test run is generated, the resultant permutations of test cases + flags were packaged up into bundles of similar settings, so for example 10 test suites that amounted to a thousand ARMv6 tests with the same compiler and linker flags would be placed into a bundle together. After these bundles were created, they were dispatched to the lab machines.

This is where the self-healing aspect comes in:

1. If a test machine fails to respond to the test control server, the test team got an email, and the test machine was automatically taken out of rotation
    
2. If a test suite failed to execute all its tests (not just if a test failed, but if a test failed to run/return results), the test suite was re-tried on another test machine before it was marked as failed
    
3. After so many occurrences of a test device failing to execute a test (return results), the test device was taken out of the test device pool
    

The system retried as hard as it could and even retried tests on a different machine in case there was some random fluke, before giving up. Throughout the 2 or 3 days it took to complete a test run, as lab machines and test devices died (as they were wont to do), the test run kept on going.

By the end of it all, over 96% of tests would pass. CLTT had a web front end that allowed us to quickly re-run entire test suites and update their status within the overall test run if we suspected that a large number of failures were due to things like "all test devices for this CPU architecture died before this test suite ran".

Typically another 3 or 4 days would be spent manually verifying the remaining failures, which brings me to the next cool part about CLTT

# The world's best repo button

Reproducing test failures locally sucks, unless you are working with CLTT.

Here is how you locally reproduce a test failure in CLTT:

1. Press the "reproduce test locally" button and a ZIP file of the test is emailed to you
    
2. Download and extract the ZIP, there is a repo.bat inside that literally does everything for you
    
3. If needed, connect to a test device before running repo.bat
    

That is it! It was absolutely wonderful. Step 3 was a bit interesting, but that was an internal MS networking detail that isn't pertinent to the overall idea.

I've yet to see another test tool take the effort to make reproducing test case failures this easy.

# About that weird part

So I said CLTT was a bit weird.

Every single function returned a boolean. As a result, every function call was wrapped in an `if` statement. Any data that needed to leave a function was returned though `out` parameters

In defense of the programmer, this was .NET 2.0, there were no `maybe` types, or tuples even. If you squint hard enough, this was a strange way to implement [option](https://en.m.wikipedia.org/wiki/Option_type) types.

The benefit of this was absurdly robust code; almost every layer of the code was designed to be retriable. For example, if the server failed to deploy a bundle to a test machine, the deployment function returned false and the enclosing function incremented the "failures seen on this test machine" counter and went tried to deploy the bundle to the next test machine. If deploying the bundle kept failing, the server would mark the entire bundle as failed and go on to the next bundle, and so on and so forth up throughout the entire workflow of the test run.

As mentioned above, the test client was similarly robust, it'd keep trying to do its thing, and if one layer of code couldn't complete its task, the next layer above it almost always had some well-thought-out method of somehow progressing the test run forward.

But, wow, it was a weird code base to work in.

Also, there was a completely pointless use of dependency injection in one particular place that broke IntelliSense's "Find references". I say pointless because there were only two possibilities at the point of DI, so an `if` statement would have worked just as well.

# Other misc technical details

Tests were ran on a low footprint windows ce 6/7 image, iirc it was about 4 or 8 megabytes in size and only had a console, the C runtime, filesystem, and USB drivers loaded. Super cool that wince could shrink that much.

When I joined the team the SQL database was missing indexes on some crucial columns, it took me almost a year to get help from someone who knew SQL well enough to get the DB optimized, afterwards query times dropped dramatically.

There was also a performance framework that had fallen into bit rot that I got back up and running, but I completely forget all details about it.

Microsoft did code coverage long before it was an industry thing, we had to use a tool suite from Microsoft Research to do code coverage runs!

# Summary

I have likely gotten some things wrong in my recollection, in fact I know there are details about test suites and test cases that I am forgetting. The system was powerful enough that it didn't even have to run compiler tests, it really was one of the most powerful general-purpose test systems I've ever seen, that happened to be put to use testing the Windows CE team's compilers and linkers. I also didn't describe the absolutely bonker SQL database that test results were put into, or the crazy hardware build that the database ran on (this was back when splitting a database up across multiple machines was not commonly done!).

It is an unfortunate statement on the lack of progress within the industry (more on that in a future post!) that the first test system I ever used was the best test system I ever used. I hope someday to see another test system that approaches what a lone engineer was able to build all those years ago.
