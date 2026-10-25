# Chorley Panthers Image Skills

Agent skills for generating club images that look like Chorley Panthers rather than generic AI rugby league. They're built from real club photos, kit details and a house style guide.

The skills use the open `SKILL.md` format, so they work in OpenAI Codex, ChatGPT (where skills are available on your plan) and Claude.

## Skills

| Skill | What it does |
| --- | --- |
| [`squad-list`](skills/squad-list/SKILL.md) | Builds the rugby league squad list graphic from real photos and logos using a template script, not image generation |

## Install

### Quick install (Codex, Claude Code and other agents)

```bash
npx skills add connoraworden/chorley-panthers-image-skills
```

### Manual install

Clone the repo:

```bash
git clone https://github.com/connoraworden/chorley-panthers-image-skills.git
```

Then copy the skill folder into your agent's skills directory.

Codex:

```bash
mkdir -p ~/.codex/skills && cp -R chorley-panthers-image-skills/skills/squad-list ~/.codex/skills/
```

Claude Code:

```bash
mkdir -p ~/.claude/skills && cp -R chorley-panthers-image-skills/skills/squad-list ~/.claude/skills/
```

### ChatGPT

If your plan has skills, zip the `skills/squad-list` folder and upload it in ChatGPT's skills settings.

## Updating

Re-run the install command, or `git pull` and copy the folder again.

## Photos and safeguarding

This repo is public. Anything in a skill's `references/` folder can be seen by anyone.

- Only add photos the club has consent to publish.
- Junior players only where the club already has consent to publish their photos, as with the default background from the club website.
- Follow the club photography policy and RFL safeguarding guidance.

## Contributing

Open a pull request with changes to a skill. Test the skill on a few real requests before you submit it.
