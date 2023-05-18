# Motivation
AI's rise is changing the way we code. Like many developers, I've found myself frequently switching between ChatGPT and my IDE, often copying files between them. If you're in the same boat, you know how much of a time sink it can be. This got me thinking about how we could improve this workflow - and that's where the idea for this hack comes from.

The core of this project is the script projectGPT.py, essentially a plug-in for ChatGPT which runs on localhost. It's a straightforward but handy tool. It lets me query my project documentation right from the chat, cutting down a lot of the manual back-and-forth. Plus, when I feed the general descriptions into the chat, it helps ChatGPT to provide more effective code-writing assistance.

If you're looking for a smarter way to manage your coding workflow, give this a shot. By blending AI with our coding environments, we can save time, cut down on the tedious parts of the job, and focus more on the coding itself. This is what this project is all about - finding better ways to work with the tools we have.

# Prerequisites
* A Computer with pyhon 3 installed
* A ChatGPT developer Account 

# Setup
Setup your virtual environment (recommended)
```bash
virtualenv .venv
source .venv/bin/activate to enter the virtual environment
pip install -r requirements.txt
```
# Run
1. use:
```bash
python projectGPT.py --docpath examples/website --name interstallar_voyages --port 3334
```
to start up the script, now it is serving the api on pert 3334 of your localhost

2. Log into ChatGPT and start a new chat with the GPT-4 model with plugins.
3. On the top, choose the Plugin selector, select "Plugin store" at the bottom
4. Select "Develop your own plugin" (if you cannot see this, your not allowed to use localhost plugins, register for developer access)
5. enter ```localhost:3334```


# Start Chatting
prompt as follows:
```
I want to start working on the project interstellar_voyages please read Readme.md 
```
Now you sould see, that ChatGPT is calling the plugin and retreiving the information of Readme.md. The Readme.md links to other
documentation, so let us read this as well.
```
Also, please read the related documents
``` 
ChatGPT now reads all linked documents, this takes a couple of seconds.

Let's start with the project...
```
Now, considering a the instructions you know about the project, please write the fully styled app.component.html for me 
``` 
As you might see ChatGPT is taking the instructions from the Markdown files and creates an angular startpage with tailwind css stylings
and the component-structure, we described in our Markdown files.

Now we want to create pictures:
```
read the documentation on midjourney
```

```
I want to create the pictures for the carousel so please write me the midjourney prompts with the given colors and aesthetics
```
# How to Continue and what I learned so far
As this project continues to evolve, I've come to realize the value of putting a little extra effort into documentation over source code. It's all about achieving clarity and mutual understanding, which, in turn, leads to more effective collaboration.

My projects often find me oscillating between refining design-level documentation and diving deep into the nitty-gritty of code. The balance, I've found, is vital - it ensures that while the details are being worked out, the big picture remains clear and accessible to all.

As a newcomer to ChatGPT plug-in development, this project has been a real learning experience, especially in terms of interacting with an LLM over an API. The learning curve has been steep but rewarding. I hope this tool proves to be as useful for you as it has been for me.

Feel free to dive in, explore, tweak, and test it. And if you have any thoughts or ideas about it, or just want to discuss ChatGPT and AI in development further, don't hesitate to get in touch. The exchange of ideas is what drives progress, and I'd be delighted to hear from fellow developers who are interested in this space. Here's to pushing boundaries and coding smarter!


