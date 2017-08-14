# Notes 14 Aug 2017

## Where are we?

I haven't kept good notes in recent weeks as I've found a good rhythm in programming but unfortunately some of my project have turned into mush while I started new things and didn't finish old things.  Bummer.

On this project, we're at this point:
1. I can easily get a commit from github
2. I know which commits I'm interested in
3. I *cannot* store them in the database yet
4. I *cannot* retrieve or parse the requirements.txt or package.json file
5. I *cannot* filter projects by multiple criteria yet.

We will solve these problems, they are all general CRUD type issues.


## TODO

1. Get the database piece working and maybe make it a little more 'config-as-code' stable.
2. Start writing target commits to the database
3. Somehow wire in a script to parse and update the target files.


## Notes 2

Some things I have noticed:
- GitHub repos can contain dot, underscore or dash.  I did not plan on this.
- Some people check in package.json from other repos into theirs.  I will filter for these.
