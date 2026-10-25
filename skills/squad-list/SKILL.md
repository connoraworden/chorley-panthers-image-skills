---
name: squad-list
description: Create a Chorley Panthers rugby league squad list graphic for a fixture, in the club's house style. Use when asked for a squad list, team sheet, line-up or team announcement graphic.
---

# Chorley Panthers squad list

Chorley Panthers is an amateur rugby league club. Squad lists are a fixed house template, not a fresh design each week. Match the template exactly. Read [references/brand.md](references/brand.md) before generating.

## 1. Gather the inputs

Ask for anything missing. Do not guess any of these.

| Input | Example |
| --- | --- |
| Team | First team or A team |
| Opponent full name | Hindley Stags |
| Home or away | H |
| Day and date | Thursday 27th August |
| Kick-off | 19:00 |
| Squad | First team: numbered 1 to 13, then interchanges 14 upwards. A team: names only |
| Featured player | Full name |
| Featured player photo | Real photo, chest up, in home kit |
| Background photo | Real match action photo of the club |
| Opponent crest | Image file |

If there is no real photo of the featured player, stop and ask for one. Never generate or invent a player.

## 2. Check the text

- Spell every name exactly as given. Keep apostrophes and hyphens, such as O'Regan or Riley-Parry.
- First team: keep the numbers as given. Put the italic label INTERCHANGES between 13 and 14. If there are more than four interchanges, leave a small gap before 18.
- A team: no numbers. Sort the names alphabetically by surname unless you're told otherwise.
- Home fixture: Chorley Panthers first, then "vs" and the opponent. Away fixture: the opponent first, then "vs Chorley Panthers".
- A team fixtures add "A" to both teams, such as "Chorley Panthers A vs Blackbrook A".

## 3. Build the prompt

Fill in this template. Do not add style words to it.

```
Rugby league squad list graphic, portrait 4:5, matching the attached reference layout exactly.

Background: solid black with the attached match action photo converted to black and white, darkened heavily so it is barely visible, fading to pure black towards the bottom.

Top: two thin white horizontal lines at the top edge, with "{OPPONENT SHORT} ({H/A})" in small white italic condensed capitals centred between them.

Top left: "SQUAD" and "LIST" on two lines, huge white heavy condensed italic capitals.

Top right, right aligned:
{HOME LINE}
{AWAY LINE}
"{DAY} {DATE}" with the ordinal ("th", "st", "nd", "rd") as small superscript
"KO {TIME}"
Chorley Panthers' line is large bold heavy condensed italic capitals. The opponent's line is smaller and lighter weight condensed capitals. The date and kick-off are bold condensed italic capitals.

Left column, white condensed sans serif with wide letter spacing, one name per line:
{SQUAD LIST}

Right side: the attached photo of {PLAYER NAME}, cut out, in full colour, chest up, facing camera, standing in the club's black and white chevron home shirt. He is the only full colour element apart from the logos. Do not change his face, hair, build or kit.

Over the lower right of the player: "{FIRST NAME}" smaller and "{SURNAME}" larger below it, in a thin white handwritten signature script, overlapping each other.

Bottom centre: the attached FI Real Estate Management sponsor logo, unchanged.

Bottom edge: thin white horizontal lines with the home team crest on the left and the away team crest on the right, both from the attached files, unchanged.

No other text, colours, effects or graphics.
```

## 4. Generate

Attach these input images to the image generation:

1. The closest example from `references/` as the layout reference:
   - [example-first-team-home.jpg](references/example-first-team-home.jpg) for a first team home fixture
   - [example-first-team-away.jpg](references/example-first-team-away.jpg) for a first team away fixture
   - [example-a-team-home.jpg](references/example-a-team-home.jpg) for the A team
   Copy the layout only. Never copy the names, dates, player or opponent from an example.
2. The featured player photo
3. The background action photo
4. The Chorley Panthers crest, the opponent crest and the sponsor logo

## 5. Verify before handing over

Read the generated image back and check:

- Every name matches the input letter for letter, with the right numbers and order
- Date, ordinal, kick-off and home or away are all correct
- The player's face and kit match the photo
- The crests and sponsor logo are undistorted, with no invented logos
- Nothing extra has been added

Fix any error with an edit pass, or regenerate. If a problem is still there, tell the user exactly what is wrong. Don't hand over a graphic with a misspelt name without saying so.

## Never

- Invent a player, face, crest, sponsor or kit
- Use colour anywhere apart from the player photo and the logos
- Add glows, lens flare, smoke, fire, sparks, neon, gold, gradients or textures
- Add panther illustrations, rugby union imagery, stadium crowds or hashtags
- Add extra text such as "MATCHDAY", "GAME DAY" or a slogan
- Change the layout, swap sides or restyle the typography
