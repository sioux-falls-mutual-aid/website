# Quick Exit

**Free to copy.**

This is the Quick Exit pattern we built for Sioux Falls Mutual Aid. It is written down here so another mutual aid group, shelter, community organization, or extremely tired website volunteer does not have to solve the same problem from scratch.

It is intentionally boring: a little HTML, a little CSS, and a little JavaScript. No framework. No plugin. No build step.

## What it does

The visible part is a **Quick exit** link.

When JavaScript is available, clicking it uses `location.replace()` instead of ordinary navigation. That replaces the **current** browser-history entry with the exit destination.

So, in the simplest case:

```
search results → your page → weather
```

Pressing Back from the weather page returns to the search results instead of the page that was just replaced.

The same exit also fires when someone presses **Escape twice within 1.5 seconds**, unless they are currently typing in an input, textarea, select, or editable area.

## Please do not oversell what this does

Quick Exit is useful. It is not an invisibility cloak.

It **cannot**:

- erase browsing history;
- erase network/router/provider records;
- remove monitoring software;
- stop history syncing on a shared account;
- remove **earlier pages from your site** if the visitor already navigated through several pages before using Quick Exit.

That last one matters. `location.replace()` replaces the page the visitor is on **right now**. It cannot reach backward into the browser's history and erase other pages.

Say this plainly wherever you use the control. A safety feature that makes somebody believe their tracks are gone can make them less safe.

## The three pieces

### HTML

Put this near the top of the page, before your main heading if possible.

```html
<div class="quick-exit-bar">
  <a class="quick-exit-link" href="https://www.weather.gov/" rel="noreferrer nofollow">Quick exit</a>
</div>
<p class="quick-exit-note">Leaves this page right away, and so does pressing Escape twice on a keyboard. It cannot erase your history, so if someone checks this device, use one they cannot reach.</p>
```

The same snippet is in [quick-exit.html](quick-exit.html).

### CSS

See [quick-exit.css](quick-exit.css).

The button is sticky because a visitor who needs it may need it after scrolling. Keep the bar's background solid so page text does not scroll visibly underneath it.

One CSS gotcha: `position: sticky` only sticks inside its parent. If you put the bar inside a tiny wrapper that ends immediately, it will stop being sticky immediately.

### JavaScript

See [quick-exit.js](quick-exit.js).

The HTML works without JavaScript: it is still a normal link away from the site. Without JavaScript, it just cannot replace the current history entry or provide the double-Escape shortcut.

That fallback is deliberate. The exit should not become a decorative rectangle just because a script failed.

## Why Escape twice?

People use Escape for ordinary interface things: closing menus, dismissing dialogs, getting out of autocomplete, etc.

One press is too easy to trigger by accident.

Two presses within 1.5 seconds is fast enough to use deliberately without making every ordinary Escape keypress an emergency exit.

The script ignores Escape while focus is in an `INPUT`, `TEXTAREA`, `SELECT`, or `contenteditable` area. Losing half of a mutual-aid request because somebody dismissed autocomplete would be a fairly terrible accessibility feature.

## Where should it go?

At or very near the top of the page, and sticky while the visitor scrolls.

Do not make somebody hunt through navigation for the emergency-exit control.

The destination should be boring, fast, and plausible on almost any device. We use the National Weather Service.

A news site may display alarming headlines. A search engine may expose a previous search. Pick something dull on purpose.

## We do not tell people to clear their history

Some safety pages recommend clearing browser history.

We chose not to.

A suddenly empty history may itself be noticeable to somebody monitoring a device. Changing passwords, removing monitoring software, or turning off location sharing can also alert an abusive person or destroy evidence someone may later need.

Our public copy tells people that Quick Exit cannot erase their history and suggests using a device the unsafe person cannot access.

Your organization may make a different decision. Just make it deliberately rather than treating "clear your history" as harmless boilerplate.

## Test it

Before publishing:

1. Click **Quick exit**. You should land on the destination site.
2. Press Back. You should not return to the page you just replaced.
3. Press Escape once, wait longer than 1.5 seconds, then press it again. Nothing should happen.
4. Press Escape twice quickly. You should leave.
5. Focus a text field and press Escape twice. You should stay put.
6. Open the browser console and make sure there are no JavaScript errors.
7. If your site has several internal pages, navigate through several of them and test Back after Quick Exit so you understand exactly what remains in history.

That last test is important because Quick Exit cannot erase earlier history entries.

## WordPress warning

On our WordPress install, `&&` inside a script pasted into a Custom HTML block was mangled when the live page rendered. The stored block looked fine; the browser received broken JavaScript.

The version in [quick-exit.js](quick-exit.js) deliberately contains no ampersand characters. It uses separate `if` statements instead.

If you modify the script and paste it through WordPress, load the **live page** and check the browser console. The admin editor looking correct is not proof that visitors received working code.

## Want the whole thing in one file?

[demo.html](demo.html) is a tiny working page showing the pieces together.

Open it in a browser and test the actual exit behavior.

## Please steal this

Seriously.

Copy it. Change it. Remove our name if you need to. We did not write this so every mutual aid group in the country could independently spend an afternoon discovering `location.replace()`.

**Credit is lovely, but it is not required.** If you want to mention where it came from, “Sioux Falls Mutual Aid” is plenty.

If you improve the safety guidance or find a browser/accessibility problem we missed, though, please tell us. That part is useful to everybody.

## Licensing

The original SFMA write-up says this is free to copy, with no permission or credit required.

We have **not yet added a formal software license** to this repository. If your organization needs a standard license declaration before reusing code, check back or open an issue.
