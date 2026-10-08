# Helping with the SFMA website

First: thank you. Seriously.

There is a lot of information on this site, and a shocking amount of it can go stale because somebody changed a phone number, moved offices, stopped taking applications, changed Tuesday hours, or quietly updated a PDF nobody knew existed.

You do **not** need to know how to code to help.

## Before you post anything

Please read [PRIVACY.md](PRIVACY.md).

The short version: this is public. Do not put somebody's mutual-aid request or private information into an issue.

## Things you can help with

You can:

- tell us a resource is outdated;
- suggest a resource we should investigate;
- check phone numbers, hours, addresses, eligibility, documentation, service areas, or official links;
- research what is actually available in smaller towns and rural areas;
- test the website on a phone;
- test it with keyboard-only navigation, screen readers, zoom, large text, or reduced motion;
- make confusing wording less confusing;
- fix website code;
- review work before it goes live.

If you notice something useful, you are useful here.

## When you're fact-checking

A few rules save us a lot of grief:

1. **Go to the source first.** The organization's own current website, a government page, or another primary source beats an old directory listing.
2. **Say what you actually verified.** "Website is live" is not the same thing as "hours, phone number, and eligibility are current."
3. **If two current sources disagree, stop and flag it.** Please do not flip a coin and make us all regret it later.
4. **Some things need a phone call.** Especially waitlists, program availability, service-area rules, and anything that could send somebody on a wasted trip.
5. **Location does not equal service area.** An office being in Sioux Falls does not automatically mean it serves all of southeast South Dakota.
6. **Funding cuts do not automatically mean a program closed.** Verify what actually changed.

## What a useful resource listing should answer

Ideally, somebody should be able to look at a listing and figure out:

- What can they help me with?
- Do they serve where I live?
- How do I get help?
- Can I call, text, walk in, or do I need an appointment?
- When are they available?
- Do I need ID, paperwork, a referral, or proof of something?
- Does it cost anything?
- Is there anything important I should know before I go?
- When did somebody last check this information?

If there is **no local option**, that is okay to say. "We have not confirmed one here; here's the nearest useful next step" is much better than pretending.

## Our workflow

The board goes:

**Backlog → In progress → Needs verification → In review → Ready to publish → Done**

A useful distinction:

**Needs verification** means we still have a factual question.

**In review** means the facts are settled and we're checking the finished work: wording, accessibility, layout, usability, tone, etc.

## Accessibility

We are not building a separate "accessible website."

The normal site should already work with screen readers, keyboards, zoom, sensible headings, labeled forms, visible focus, and ordinary assistive technology.

Then people can choose presentation options such as Large Text, High Contrast, Simplified, or Reduced Motion.

For crisis information, the basic rule is even simpler:

**Do not hide the thing somebody needs to do next.**

Phone numbers and primary actions should not disappear inside collapsed accordions. Core crisis information should still work if JavaScript decides to have a bad day.

## If you're changing code

Keep the change small enough that another human can understand it.

Tell us:

- what problem you're fixing;
- what you changed;
- what you tested;
- whether it affects crisis information, resource data, mobile layouts, or accessibility.

And please don't hard-code another copy of resource information into a template if that information belongs in the canonical resource record. Future Us deserves better.

## Not sure where your thing belongs?

That's fine. Open the closest issue form and explain what you found.

Just leave private people's information out of it, and we'll sort out the rest.
