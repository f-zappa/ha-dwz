# DWZ (German Chess Federation) Rating — Home Assistant integration ♟️

This integration exposes DWZ data (Deutscher Schachbund) as Home Assistant sensors.

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square)](https://www.hacs.xyz/docs/faq/custom_repositories/)
[![MIT License](https://img.shields.io/github/license/f-zappa/ha-dwz?style=flat-square)](LICENSE)
[![Release](https://img.shields.io/github/v/release/f-zappa/ha-dwz?style=flat-square)](https://github.com/f-zappa/ha-dwz/releases/latest)
[![Issues](https://img.shields.io/github/issues/f-zappa/ha-dwz?style=flat-square)](https://github.com/f-zappa/ha-dwz/issues)
![GitHub Repo stars](https://img.shields.io/github/stars/f-zappa/ha-dwz?style=flat-square)
[![hassfest](https://img.shields.io/github/actions/workflow/status/f-zappa/ha-dwz/validate.yml?style=flat-square&label=hassfest)](https://github.com/f-zappa/ha-dwz/actions/workflows/validate.yml)

## Quick overview
![alt text](image.png)
- One sensor per configuration entry (per player / `nuLiga` ID).
- Sensor state: the player's current DWZ rating (`rating`).
- Additional information is exposed as entity attributes (see Attributes).

## Attributes

- `rating` — current DWZ rating (also entity state)
- `rating_week` — evaluation week (e.g. "202617")
- `rating_date` — ISO date (YYYY‑MM‑DD) of the Sunday's end of the evaluation week
- `index` — sequential index of the DWZ evaluation
- `active_club` — club holding the player's active licence
- `firstname`, `lastname`, `full_name` — player's names
- `gender` — `MALE` / `FEMALE`
- `birth_year`, `fide_id`, `nuliga_id`

## Installation

### Via HACS (recommended) 🧩

#### Use this link to add "DWZ (Schachbund)" to your Home Assistant instance:
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=f-zappa&repository=ha-dwz&category=Integration)

#### Alternatively follow this steps:

1. Open HACS → Integrations.
2. Click the three dots → "Custom repositories".
3. Add repository `f-zappa/ha-dwz` (Category: Integration).
4. Search HACS for "DWZ (Schachbund)" and install.
5. Restart Home Assistant and add the integration via Settings → Integrations.

### Manual (without HACS)) 🧰

1. Copy the `custom_components/dwz` directory into your Home Assistant `custom_components` folder.
2. Restart Home Assistant or reload integrations.


## Configuration

1. Find the player on the DSB search page https://www.schachbund.de/dwz-spieler.html.
   The search result is a link. This link contains the nuLiga-ID.
2. In HA: Settings → Add integration → `DWZ (Schachbund)`.
3. Enter the player's nuLiga-ID (e.g. `NU4168433`).


## More details

- 📦 This integration uses the `dwzclient` Python package (PyPI: https://pypi.org/project/dwzclient/)  `dwzclient` fetches data from the Deutsche Schachbund's public API (new API published July 2026).
- 🤖+👨🏼‍💻 This integration as well as `dwzclient` were developed with assistance from an AI coding assistant. All code, documentation and repository structure were created with AI support and have since been reviewed and manually refined — the result is not purely auto‑generated but contains hand‑crafted improvements and human review. ✍️

- 🙏 Thanks to @ludeeus for the very helpful integration blueprint (https://github.com/ludeeus/integration_blueprint)!
