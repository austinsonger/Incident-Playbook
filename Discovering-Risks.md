> https://github.com/magoo/minimalist-risk-management/blob/master/INTERVIEW.md

# Discovering risks with interviews.

We often have to ask experts for insight into subject matters that produce risk. This documents supports a _risk interview_, which often supports a _risk assessment_.

The **objective** is to effectively draw upon expert knowledge to discover plausible risk scenarios that require mitigation by our larger security organization.

The **key result** is written analysis and the production of *scenarios* that guide mitigation efforts.

---

### 👟 Getting Started
You’re going to be interviewing an expert. Great! This document is designed to help you with that process.

Here's some tips to get us started.

**👂 Listen:** The more you're talking, the less you're listening.

**🔨 Break the rules:** This document helps move a discussion along, but great interviews go off script and dive in.

**📋 Capture notes:** Balance conversation and notetaking. Work with a partner if possible.

---

### 🎙️The Agenda

- [ ] 1. Introduce yourself.
- [ ] 2. Get to know the interviewee.
- [ ] 3. Ask them open ended questions.
- [ ] 4. Take notes.
- [ ] 5. Organize the notes into a deliverable.

---

### 1. 👋 Introduce yourself
You’re the stranger! That’s OK. This means you have free reign to ask naive questions and ask for clarification. That’s why you’re valuable. Make sure the person knows who you are and why you’re qualified. The interviewees may think you’re sent to judge their performance. This shouldn’t be the case. Clarify this upfront.

### 2. 😎 Get to know the interviewee
Everyone is interesting. Warm up the interviewee. Ask about their place in the organization.

- How would you describe your role?
- What are you hoping to work on this week?
- What is a typical task you’re assigned?
- What are your regularly occurring meetings?
- What projects are you cheering on that make your life easier?
- Who are you frequently collaborating with?
- Can you describe a process from task to close?

### 3. ❓ Ask the interviewee open ended questions.
Conversations are never scripted. Good interviews flow naturally towards interesting subjects. A good interviewer should be prepared to explore the knowledge of the interviewee with a toolbox of questions and methods.

Everything an interviewee says can be extrapolated on.

- _We store customer data here._ ➡️ **_What's the street value?_**
- _This cluster is never offline._ ➡️ **_What breaks, if it were?_**
- _I’m afraid of RCE in this environment._ ➡️ **_Why, what’s in there?_**

Here are some underlying models that questions can be influenced by on.

#### 💥 Impacts
Describe any concept of value, either monetary or qualitative topics like “safety” or “knowledge”.

- What sort of data is very exclusive to our company?
- What could you go delete that would get you fired?
- What do we own that a competitor could monetize?
- What do we have that is worth backing up?
- Are there any “switches” you’d be afraid of flipping?
- Who has the A/C privileged conversations?
- How would you cause a severe outage?
- Are there headlines you’re worried about?

#### 👻 Threats
Describe the type of force, human or otherwise, that would act or behave in a way that would result in an impact.

- Are there outside vendors with access to this?
- What would someone do if they knew they’d be fired?
- Who would want to see a headline?
- Are there groups of people that don’t like this?
- What do adversaries need to be capable of?
- Who has succeeded before?

#### 💔 Vulnerabilities
Describe circumstances or configurations that may attract a threat or exacerbate an impact.

- Are there bugs we drag our feet on?
- What kind of “biggies” have been found in the past?
- Do people ever complain that something isn’t quite locked down?
- What sorts of bugs get a huge payout?
- Are there any surprisingly old dependencies?
- What bugs take the longest to see a fix?


#### 😨 Fears
Bring any underlying worries to the surface. Take your hands off the wheel and allow the interviewee to guide the conversation. Some interviewee's are itching to tell you about something.

- What do we try to defend against?
- What keeps you up at night?
- Have we had any “near misses?”

#### 🤔 Conditional Scenarios
Walk the interviewee one layer deep with “what if” situations. Tease out more entrenched risks with a suspension of disbelief.

- What would an adversary immediately discover on your laptop?
- What would an adversary immediately discover on the network?
- What would an adversary immediately discover on our servers?
- What would an adversary immediately discover in our source code?
- What would an adversary immediately discover in our offices?
- What would an adversary immediately discover about our supply chain?

#### 🎸 VIP Employees
Discover employees that may have overloaded capabilities if compromised. May also may reveal other valuable areas for interviewing and expand the rolodex.

- Who would you describe as "the guru" here?
- Who has access to everything?
- Who influences decisions?
- Who do you hope never goes “rogue”?
- What do we need to turn off immediately when someone is fired?

#### 📜 Best Practices
Change perspectives and see if assumptions are being made about risks being low. Interviewees will often disagree on the state of best practices.

- Are there things that aren’t encrypted, but should be?
- Have you seen things that don’t authenticate like everything else?
- Are there roles or groups that have too much access?
- Do you expect to not be alerted about certain things?
- Have things gone on without a retrospective?
- Do other companies mitigate things better than us?

#### 🐺 “In The Wild”
This follows the theory that no incident should happen more than once. We should learn from the failures of others.

- Are there incidents you’ve seen that you worry about?
- Have any incidents happened here?

### 4.  ✍️ Take Notes
Notes are very personal and open-ended. This part does not need to be prescribed. If useful, I make the following collaborative spreadsheet.

| Scenarios | Vulnerabilities | Impacts | Threat Actors | Follow Up Questions |
|-----------|-----------------|---------|---------------|---------------------|

Notes go underneath in cells, often with the interviewee in edit mode as well.


### 5.  📖 Preparing Deliverables
Right now you’re the only one who got anything from these interviews. You’ll need to prepare some written analysis for others to make use of it.

The following are useful areas to organize your findings.

#### 🔭 Scenarios
A scenario is a concrete way to articulate a risk. Scenarios are undesirable future events. The deliverable has a list. The following examples may help you author them.

This scenario includes an *impact* 💥:

> An outage in `prod002`  violates customer SLA.

This scenario includes a *vulnerability* 💔:

> The RCE in our mobile app API is used to gain persistence on a server.

This scenario includes a *threat* 👻:

> An insider on support tooling exfiltrates customer data to the media.

As you can see, _scenarios_ are effective at communicating almost any creative model you approach towards discovering risks.

A statement like: _We don't have any next-gen antivirus_... would *_not_* be a scenario. It doesn't represent an event, it's just a state of being. Risk scenarios are the _reason why_ we work towards certain states.

Without undesirable scenarios, there would be no negative outcomes to spend time avoiding.

Perhaps, instead:

> Malware has been implanted on an engineer's laptop.

A proper scenario. It may even begin a conversation on whether _next-gen antivirus_ is the right mitigation, or patch management, or so on.

#### 🧐 General Observations
Interviews will produce useful themes. These are also useful to capture and reveal themselves unpredictably. For instance, you may come across:

- Organizations that produce more risk than others.
- Mitigations that are suspected to be ineffective.
- Engineering practices that create more churn than necessary.

While these are not _risks_ in themselves, they are often useful feedback to capture in the interviewing process.
