# One fact, one place

How to stop the same phone number being right on one page and wrong on another.

## The failure

It happened to us four times before we stopped treating it as carelessness.

A crisis line changed its name. We updated it. Months later the old name was still on a different
page. A thrift store's phone number was correct on one page and belonged to the other branch on
another. A food pantry had two published numbers and our site carried the wrong one. A transit service
changed its booking rule and we fixed it in one of the two places we had written it down.

Every one of those was found by a human reading the site, not by us. A directory of resources is
mostly duplicated facts, and duplicated facts drift apart. That is not a discipline problem, it is a
structural one.

**The cost is not even.** A stale opening time wastes a trip. A stale crisis line means someone in the
worst hour of their life calls a number that does not ring.

## What does not work

**Rules.** "Always search the whole site before changing a number" is a rule that works until the day
someone is tired. We wrote that rule. We then broke it three more times.

**Search and replace.** Works only if every copy is worded identically, which they never are. One says
"24/7 and free", another says "free, 24 hours".

**A spreadsheet of the truth.** Helps you notice drift. Does not prevent it, because the website is
still storing its own copies.

## What works

Store the fact once. Render it in both places.

In WordPress this is a **synced pattern**: a block you create once and insert anywhere. Every
insertion is a reference, not a copy. Edit the pattern and every page carrying it changes at the same
moment, because there is only ever one copy.

We put our five crisis numbers in one synced pattern. It renders on the homepage and on the
help page. There is now no version of the site where those two disagree, and no rule anyone has to
remember.

Most content systems have an equivalent. Look for the word "reusable", "synced", "snippet",
"include", or "partial".

## Where the line is

Not everything belongs in a shared block. We use a simple test.

**Share it when the fact is the same fact.** A phone number, an address, an eligibility rule, an
opening time. If it changing in the world should change it everywhere on your site at once, it is one
fact.

**Do not share it when the words are doing different jobs.** The crisis page lists a shelter line as
the thing to call tonight. The housing page explains the same line as one route among several. Those
are two pieces of writing about one fact, and forcing them into one block makes both worse.

In practice: share the number, not the paragraph.

## The trap we walked into

A link inside a shared block is correct on every page except the one it points at.

We put a "more options" link inside our crisis-numbers pattern, pointing at the help page. On the
homepage it was useful. On the help page itself it was a link to the page you were already on, which
did nothing at all.

The fix was to point it at a section rather than a page, using an anchor that exists on the
destination. One href, correct in both places, no second copy.

**Buuut,**

the general lesson is bigger than that one link. **Anything inside a shared block that refers to
"here" is wrong somewhere.** Links, "see above", "on this page", "scroll down". Check every shared
block from the perspective of each page it renders on, not just the one you were editing.

## If you take one thing from this

The next time you catch yourself about to fix the same fact in two places, stop and make it one place
instead. The fix takes about as long and it is the last time you do it.
