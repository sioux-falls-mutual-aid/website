# What a default WordPress install tells other people about your visitors

A fresh WordPress site contacts several third parties on behalf of every reader, without asking them
and without telling you. None of it is malicious. All of it is on by default.

This is what we found on our own site and what we did about it. Work down the list.

## 1. Gravatar

**What it does.** WordPress shows commenter avatars by asking gravatar.com for them. That request
carries your reader's IP address to Automattic, on every page with comments. The URL it requests is
built from a hash of the commenter's email address, which is published in your page source.

**Why it matters for us.** An email hash is not an encryption. Common addresses can be looked up in
precomputed tables, so publishing the hash can expose who commented.

**Fix.** Settings > Discussion > uncheck "Show Avatars". If you do not run comments at all, also turn
comments off entirely.

## 2. Emoji

**What it does.** Put an emoji in a post and WordPress may replace it with an image file served from
`s.w.org`, which is WordPress.org. Every one of those images is a request carrying your reader's IP.

**How bad it got for us.** One page used a warning emoji fourteen times as a visual marker. That was
fourteen requests to WordPress.org per page load, per reader.

**Fix.** Do not put emoji in post content. We replaced ours with a bold word used consistently as the
caution marker, which also reads better to a screen reader than an emoji does.

**Checking it.** View source and search for `s.w.org`. You will probably find two matches even after
fixing this, inside a settings script. Those are inert. What matters is whether any `<img>` tag points
at that host. Ours shows zero.

## 3. Embedded maps, video, and widgets

**What it does.** Any iframe loads when the page loads, which tells that host who your readers are
before the reader has done anything.

**Fix.** See [`click-to-load-map.md`](click-to-load-map.md). The pattern works for any embed.

## 4. Fonts and scripts loaded from someone else's server

**What it does.** A theme or plugin that pulls a webfont or a library from a CDN hands that CDN a
request per visitor.

**Fix.** Host them yourself, or pick a theme that already does.

**Checking it.** List every external script source on a page. Ours returns exactly one hostname: our
own.

## 5. Site health phoning home, and plugin telemetry

Some plugins send usage data by default and ask forgiveness in a settings page you never opened.
Check the settings of anything you installed, especially anything free with a paid tier.

## 6. Your own analytics

Worth asking whether you need any. We decided we did not. A resource page does not get better because
we know how many people read it, and the people reading it have the most to lose from being counted.

If your group does want numbers, pick something that does not profile individuals, and say so in your
privacy policy in plain words.

## 7. The privacy policy itself

WordPress generates a boilerplate privacy policy that describes a site that is not yours. Ours was
1,800 words of text about embedded content and analytics we do not run.

Replace it with a short, true description of what you actually collect. If the honest version is
"almost nothing", that sentence is worth more to a reader than four pages of template.

## How to check the whole thing at once

Load a page with developer tools open, look at the network panel, and read the list of hostnames your
page contacted. Everything on that list that is not you is something a reader did not agree to.

Do this on your busiest resource page, not your homepage. The homepage is rarely the one with the
embeds.

**Buuut,**

none of this protects anyone from someone with access to their device. It stops your site from
broadcasting your readers to third parties. It does nothing about monitoring software on a phone, a
shared account, or someone reading over a shoulder. Those need different answers, and your site should
say so rather than letting a privacy policy imply a safety it cannot provide.

## What we have not solved

- **Hosting logs.** Our host keeps access logs with IP addresses. We do not control the retention and
  have not yet asked what it is. If you have, we would like to know what you found.
- **Backups.** Ours are kept indefinitely, which means "deleted after 30 days" is not a promise we can
  honestly make about anything a reader submits. We are rewording rather than pretending.
