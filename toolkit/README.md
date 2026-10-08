# Sioux Falls Mutual Aid: website notes

Things we built for [siouxfallsmutualaid.org](https://www.siouxfallsmutualaid.org) that other mutual aid groups can copy. Mostly small, mostly WordPress, all of it written down because we had to work it out once and nobody should have to work it out twice.

Nothing here is a framework or a plugin. Every piece is a few dozen lines you can paste into a site you already have.

## What's here

| File | What it is | Needs WordPress? |
|---|---|---|
| [Quick Exit](../components/quick-exit/README.md) | A button that leaves your site and takes the current page out of the visitor's immediate Back-button path. Plus an Escape-key shortcut. | No |
| [`click-to-load-map.md`](click-to-load-map.md) | An embedded map that sends nothing to Google until the visitor asks for it. | No |
| [`wordpress-privacy-checklist.md`](wordpress-privacy-checklist.md) | The things a default WordPress install can tell third parties about your visitors, and what we changed on ours. | Yes |
| [`synced-facts.md`](synced-facts.md) | How to stop the same phone number being right on one page and wrong on another. | Mostly |

## Why a mutual aid group is publishing web code

Because the failure modes are different for us.

A broken contact form on a restaurant site costs someone a reservation. A stale phone number on a resource page sends a person in crisis to a line that does not ring. An embedded map hands a third party the IP address of everyone who looked up a domestic violence shelter. The stakes change which engineering decisions are correct, and most web advice is not written with those stakes in mind.

So these notes include the reasoning, not just the code. The reasoning is the part that transfers.

## Who this is for

Whoever keeps your group's website running. We assume you can paste HTML into a page and find your stylesheet. We do not assume a build step, a framework, a budget, or a developer.

## Use it

Copy it. Change it. Strip our names off it if you need to.

**Please share it freely, and we will happily accept the tiny gold star if somebody wants to give one.**

No permission needed. Credit is appreciated, not required.

If you improve something, especially the copy that tells people what is and is not safe on their own devices, we would like to hear about it. That is the part we are least sure we got right.

## A warning about trusting this

Everything here worked on our site, on the versions we were running, on the day we wrote it down.

Where a finding is specific to our install rather than universal, we say so in the file. Check it on your own site before you rely on it, and especially before you tell a visitor that something protects them.
