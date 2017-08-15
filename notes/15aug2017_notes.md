# Notes 15 Aug 2017

Here are some things I've learned from this project:

1. I use GitHub in a certain way.  I don't deviate from that generally - my username is the same (jamesfe) which is simple, no dots or dashes or underscores.  My repo names are generally simple (with an underscore, which I overlooked in writing this code).  What I failed to do here is to properly identify the requirements for each function (feature) I wrote on the way in.  Luckily, I did some unit testing and incrementally fixed the problems I saw and wrote tests for most of them.

2. I didn't plan out how to query by version.  Somewhat in plan, however, I save the exact version that I found, so I can always go back and re-parse it into something more meaningful.  I'll need to know how people expect to query the site though, so I can write an "engine" to figure out if the requirement they input should or should not match a project.

3. There is a lot of variability in scraping projects, but they are starting to seem the same:

- Scrape some data
- Follow up on the data with more scraping or processing
- Render a UI
- Search and display


Finally, I think this data will be interesting to analyze although right now I'm not sure how I should go about it.  We'll see in the future I guess.

What do I need to do?

1. Create some sort of interface to search my database
2. Host the interface somewhere
3. Keep the scraper running in the background to gather more data
4. Figure out what it means for a requirement to "match"
5. Parse Python requirements.txt files
