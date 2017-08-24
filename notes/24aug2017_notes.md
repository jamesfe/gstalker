# Notes 24 Aug 2017

It's been a little while since I noted on this project.  I'm stalled on a few things:

1. How do I parse the versions in a meaningful manner?
2. What kind of queries d oI receive?
3. How do I interpret things like `~` and `^` in the `package.json` files?  There's a spec for this but they imply ambiguity.  
4. What kind of UI do I use to render this?  (God please something lightweight).

For now though, I have done the following:

- Many tests
- Many stability increases
- Focus on scraping
- Set up a quick web sever to answer API calls


My strategy is this:

- Leave the UI for last
- Create a usable REST API
- Start to parse the `requirements.txt` files at some point
- Start with small features and iterate bigger and bigger
