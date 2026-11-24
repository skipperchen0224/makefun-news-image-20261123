# makefun-news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/skipperchen0224/makefun-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/skipperchen0224/makefun-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A newspaper front page that sums up the world's news of Monday,
23 November 2026, in one 1024×1024 image (`entry.png`).

Made for the [news-image-20261123 bounty](https://make.fun/bounty/news-image-20261123)
on [make.fun](https://make.fun) — one image, the whole day.

![The World Today — 23 November 2026](entry.png)

## The day's stories

- **Lead — Santa Clara:** Nvidia brings back Jensen Huang as CEO after
  an 11-day crisis, backed by Trump and Musk (AP, Reuters).
- **Washington:** Trump leans to new Iran strikes in the New Year if
  talks fail to produce a deal (AP).
- **Benghazi:** Zelenskyy says Ukrainian sea drones hit two Russian
  ships in the Libyan port of Benghazi (AP).
- **Seoul:** Asian chip stocks slide on AI-spending doubts; South
  Korea's Kospi falls as much as 5.8% (Al Jazeera).
- **Kyiv:** Russian strikes kill at least 15 people in the Kyiv region
  (AP).
- **Dhaka:** Bangladesh vows to arrest and jail ex-PM Sheikh Hasina if
  she returns from India in December (Reuters).
- **Jakarta:** 24 killed in an Indonesia factory blaze as rescuers
  search for dozens missing (AFP).
- Also: Medvedev warns on nuclear arms; Eisenkot calls settler arson
  "Jewish terrorism"; Libya files a UN complaint over the Benghazi
  ship attacks.

## Run it

```sh
python3 render_front_page.py   # redraw the front page (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png (1024x1024 PNG, deterministic bytes)
```

`main.ts` (Node 22, standard library only) copies the pre-drawn
`entry.png` to the output directory. The image itself is drawn by
`render_front_page.py` (Pillow, in this repo). Every fact was checked against
live reporting on 23 November 2026. The script is deterministic — same
input, same bytes.

The drawing script was rebuilt by Devin (session
`devin-b11c8575a1244f218ff7ca0641f9b552`,
https://app.devin.ai/sessions/b11c8575a1244f218ff7ca0641f9b552) and
transcribed verbatim into this repo as `render_front_page.py`.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
