---
name: squad-list
description: Create a Chorley Panthers rugby league squad list graphic for a fixture, in the club's house template. Use when asked for a squad list, team sheet, line-up or team announcement graphic.
---

# Chorley Panthers squad list

Chorley Panthers is an amateur rugby league club. The squad list is a fixed house template. Build it by running `scripts/render.py`. It places the real photos, crests and sponsor logo and sets the text in the house fonts.

**Never use image generation for this graphic.** Image models redraw crests, logos and faces and invent layouts. Do not generate, edit, retouch or "improve" the result with an image model either.

Examples of the finished graphic are in `references/`: [first team home](references/example-first-team-home.jpg), [first team away](references/example-first-team-away.jpg) and [A team](references/example-a-team-home.jpg). Brand details are in [references/brand.md](references/brand.md).

## 1. Gather the inputs

Ask for anything missing. Do not guess any of these or fill them with placeholders.

| Input | Notes |
| --- | --- |
| Team | First team or A team |
| Opponent full name | Hindley Stags |
| Opponent short name | Used in the small top label, such as Hindley or Blackbrook A |
| Home or away | |
| Day and date | Thursday 27th August |
| Kick-off | 19:00 |
| Squad | First team: in shirt number order, 1 to 13, then interchanges from 14. A team: names only |
| Featured player | Full name, which must be in the squad |
| Featured player photo | **Cut-out PNG with a transparent background**, chest up, in home kit. If they only have a normal photo, ask them to cut it out with remove.bg or Canva first |
| Background photo | Real match action photo. It's converted to black and white and darkened automatically |
| Opponent crest | PNG, ideally with a transparent background |

The Chorley Panthers crest and the sponsor logo are bundled in `assets/` as `club-crest.png` and `sponsor.png`.

## 2. Check the text

- Spell every name exactly as given. Keep apostrophes and hyphens.
- First team: names in shirt number order. The script numbers them and adds the INTERCHANGES label after 13.
- A team: sort by surname unless told otherwise.
- Read the squad back to the user and confirm it before rendering if there's any doubt.

## 3. Write the config

Write `squad.json` next to the uploaded files. Relative paths in it resolve from the JSON file's folder.

```json
{
  "team": "first",
  "home": true,
  "opponent": "Hindley Stags",
  "opponent_short": "Hindley",
  "date": "Thursday 27th August",
  "kickoff": "19:00",
  "squad": ["Player One", "Player Two"],
  "featured_player": "Player One",
  "featured_photo": "player.png",
  "background": "action.jpg",
  "opponent_crest": "hindley.png",
  "output": "squad-list.png"
}
```

`team` is `"first"` or `"a"`. For the A team, the script adds " A" to both team names.

## 4. Render

```bash
python scripts/render.py /path/to/squad.json
```

Run it from this skill's folder. It needs Python 3 and Pillow. The output is a 3200 x 4000 PNG (4:5 for Instagram).

If the script exits with an error, fix the input it names and run it again. Don't work around it.

## 5. Check and hand over

Look at the output and confirm:

- The names, numbers, date, kick-off and home or away are all correct
- The player photo isn't badly cut out

Then give the user the PNG.
