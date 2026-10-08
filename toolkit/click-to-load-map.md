# Click-to-load map

An embedded map that sends nothing to Google until the visitor presses a button.

## The problem

The normal way to put a map on a page is to paste the iframe Google gives you. That iframe loads as
soon as the page does, which hands Google the IP address, browser and referring page of everyone who
opens it. The visitor never chose that and is never told.

On a mutual aid site the people opening that page are looking up a domestic violence shelter, a food
pantry, a needle exchange. A third party learning that a given IP address loaded that specific page is
not a theoretical privacy concern.

Click-to-load fixes it without giving up the map. The iframe does not exist until someone asks for it.

## What our visitors see

> **The map is off until you turn it on.**
> It is hosted by Google, so loading it tells Google your IP address. Nothing has been sent yet.
>
> [ Load the map ]
>
> Or open it on Google Maps in a new tab

The second line is doing real work. "Nothing has been sent yet" is the part people do not expect and
the reason they trust the button.

## The code

Replace `YOUR_EMBED_URL` with the `src` from the iframe Google gives you, and `YOUR_MAP_LINK` with a
normal Google Maps link to the same place.

```html
<div class="map-holder" data-map-src="YOUR_EMBED_URL">
  <div class="map-prompt">
    <p class="map-note"><strong>The map is off until you turn it on.</strong></p>
    <p class="map-note">It is hosted by Google, so loading it tells Google your IP address. Nothing has been sent yet.</p>
    <p><button type="button" class="map-button">Load the map</button></p>
    <p class="map-alt"><a href="YOUR_MAP_LINK" rel="noreferrer nofollow" target="_blank">Or open it on Google Maps in a new tab</a></p>
  </div>
</div>
```

```css
.map-holder {
  border: 1px solid currentColor;
  padding: 1.25rem;
}

.map-holder iframe {
  display: block;
  width: 100%;
  height: 420px;
  border: 0;
}

.map-note { margin: 0 0 0.5rem; max-width: 60ch; }
.map-alt { margin: 0.75rem 0 0; font-size: 0.9em; }
.map-button {
  font: inherit;
  font-weight: 700;
  border: 2px solid currentColor;
  background: transparent;
  color: inherit;
  padding: 0.6rem 1.25rem;
  min-height: 44px;
  cursor: pointer;
}

.map-button:focus-visible { outline: 3px solid currentColor; outline-offset: 2px; }
```

```js
(function () {
  var holders = document.querySelectorAll(".map-holder");
  for (var i = 0; i < holders.length; i++) {
    wire(holders[i]);
  }

  function wire(holder) {
    var button = holder.querySelector(".map-button");
    if (!button) { return; }
    button.addEventListener("click", function () {
      var src = holder.getAttribute("data-map-src");
      if (!src) { return; }
      var frame = document.createElement("iframe");
      frame.setAttribute("src", src);
      frame.setAttribute("loading", "lazy");
      frame.setAttribute("allowfullscreen", "");
      frame.setAttribute("referrerpolicy", "no-referrer");
      frame.setAttribute("title", "Map");
      var prompt = holder.querySelector(".map-prompt");
      if (prompt) { prompt.remove(); }
      holder.appendChild(frame);
      frame.focus();
    });
  }
})();
```

## Notes on the code

**The URL lives in a data attribute, not in a `src`.** That is the whole mechanism. A `src` on an
iframe fetches immediately; a string in `data-map-src` is inert until JavaScript uses it.

**`referrerpolicy="no-referrer"`** stops the embed telling Google which page of your site the visitor
was on. The IP address still goes once they press the button, because that is unavoidable, but the
page they were reading does not have to.

**Give the iframe a `title`.** Screen readers announce iframes by title, and an untitled one is
announced as nothing useful.

**Move focus into the map after loading it.** Someone navigating by keyboard pressed a button and the
button then vanished. Without `frame.focus()` their place on the page is gone.

**Buuut,**

the version running on our own site does neither of those last two yet. This file is the corrected
version, not a transcript of ours. We are fixing ours to match.

**The same pattern works for anything embedded.** Video, calendars, donation widgets, fundraising
thermometers, social feeds. Anything that loads from someone else's server on page load is telling
that server who your visitors are. The data attribute trick is identical.

## How to check it worked

Open the page and look at the network panel in your browser's developer tools, or just view source.
Before you press the button there should be **zero** requests to the map host and **zero** iframes in
the document. Ours shows zero of both.

If you want the harsher version of the test: load the page, press nothing, and confirm the only
hostname your page contacts is your own.

## If your site runs WordPress

This has to live in a **Custom HTML block**. If you let the editor "convert to blocks", the script is
stripped and you are left with a dead button and a map that never loads. Nothing warns you.

Also see [`wordpress-privacy-checklist.md`](wordpress-privacy-checklist.md). Fixing the map while
Gravatar is still on is not much of a win.
