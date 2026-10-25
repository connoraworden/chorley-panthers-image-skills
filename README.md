# Chorley Panthers Image Skills

Agent skills for generating club images that look like Chorley Panthers rather than generic AI rugby. They're built from real club photos, kit details and a house style guide.

The skills use the open `SKILL.md` format, so they work in OpenAI Codex, ChatGPT (where skills are available on your plan) and Claude.

## Skills

| Skill | What it does |
| --- | --- |
| [`club-images`](skills/club-images/SKILL.md) | Turns a request into an on-brand image prompt and generates it |

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
mkdir -p ~/.codex/skills && cp -R chorley-panthers-image-skills/skills/club-images ~/.codex/skills/
```

Claude Code:

```bash
mkdir -p ~/.claude/skills && cp -R chorley-panthers-image-skills/skills/club-images ~/.claude/skills/
```

### ChatGPT

If your plan has skills, zip the `skills/club-images` folder and upload it in ChatGPT's skills settings.

## Updating

Re-run the install command, or `git pull` and copy the folder again.

## Photos and safeguarding

This repo is public. Anything in `references/` can be seen by anyone.

- Only add photos the club has consent to publish.
- No identifiable junior players.
- Follow the club photography policy and RFU safeguarding guidance.

## Contributing

Open a pull request with changes to a skill. Test the skill on a few real requests before you submit it.
