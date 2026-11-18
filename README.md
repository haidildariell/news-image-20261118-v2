# The World Today — Wednesday 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/haidildariell/news-image-20261118-v2/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/haidildariell/news-image-20261118-v2/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

Bounty: https://make.fun/bounty/news-image-20261118

This entry sums up the world news of Wednesday 18 November 2026 in a single
image: a classic newspaper front page. The lead story covers Iran and the US
trading drone strikes over the Gulf; four side panels cover Ukraine's second
strike on the Crimean bridge, Trump's Manila summit for Quad talks, Nvidia's
record $116bn quarter, and the Gaza ceasefire warning; a weather band tracks
Cyclone Akvan in the Bay of Bengal, and a navy ticker along the bottom rounds
up four more stories from the day.

The image was made with a deterministic Pillow program, `build_image.py`,
which draws the whole page with real TrueType fonts (DejaVu Serif for the
masthead, Liberation Sans for headlines and text), flat colours, thin rules,
and small hand-drawn flat icons — no photographs, no gradients, no network.
Running `build_image.py` regenerates `entry.png` (1024×1024 PNG) exactly.

The competition entrypoint is `main.py`: it copies the bundled `entry.png`
to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`), so the
submitted program runs offline with the standard library only and produces
byte-identical output on every run.
