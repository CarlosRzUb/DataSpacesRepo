# Recording Script — Labs 10-12: Federated EO Data Space for Flood Monitoring

Screen capture + voice only. Run everything from `flood-monitoring-space/`.

---

## Capture 1 — Folder structure in VS Code

**Show:** `flood-monitoring-space/` folder tree expanded — providers/, catalog/, scripts/, reports/ all visible.

**Say:**
This is the Federated EO Data Space I built for the National Flood Monitoring project. It follows the same federated architecture from the previous labs — each EO resource is an independent provider with its own metadata, and a federation layer builds a unified catalog across all of them. There are eight providers, four scripts, and a generated catalog and reports directory.

---

## Capture 2 — `providers/sentinel_1/metadata.json`

**Show:** File open in VS Code. Scroll slowly so the `operational_requirements` block is visible.

**Say:**
Each provider folder contains a metadata file that describes the resource. Sentinel-1 is a C-band SAR satellite — its active radar sensor transmits its own microwave pulses, which means it works through cloud cover and at night. You can see here it maps directly against the five operational requirements defined for the flood monitoring service. It supports all five: flood detection, flood extent assessment, cloudy conditions, night operations, and emergency response.

---

## Capture 3 — `providers/sentinel_2/metadata.json`

**Show:** File open in VS Code. Scroll to `operational_requirements`.

**Say:**
Sentinel-2 is a multispectral optical sensor at 10-metre resolution. It supports flood extent mapping through water spectral indices — NDWI and MNDWI — and is highly complementary to Sentinel-1 in clear-sky windows. However, it does not support cloudy conditions or night operations, because it is a passive optical sensor. This is an important distinction when choosing sensors during an active flood event.

---

## Capture 4 — `providers/copernicus_ems/metadata.json`

**Show:** File open in VS Code. Scroll to `description` and `products`.

**Say:**
The Copernicus Emergency Management Service is not raw satellite data — it is an operational service. Its Rapid Mapping component fuses Sentinel-1 SAR with commercial very-high-resolution imagery to produce standardised flood delineation and damage assessment maps within hours of activation. It also includes the European Flood Awareness System, EFAS, which provides 15-day flood forecasts. This service supports all five operational requirements.

---

## Capture 5 — `providers/eumetsat/metadata.json`

**Show:** File open in VS Code. Show `description` and `operational_requirements`.

**Say:**
EUMETSAT operates Europe's meteorological satellites. Through the Hydrology Satellite Application Facility it delivers 15-minute precipitation estimates from geostationary Meteosat MSG. This is critical for upstream rainfall monitoring before and during a flood event — it feeds directly into EFAS for early warning. It does not detect surface flooding directly, but it covers cloudy conditions, night operations, and emergency response.

---

## Capture 6 — Remaining four providers (file tree)

**Show:** Click through `sentinel_3/`, `sentinel_5p/`, `copernicus_clms/`, `cdse/` in the sidebar — just enough to show each folder exists and contains a metadata.json.

**Say:**
The remaining four providers are: Sentinel-3, which monitors large-scale water bodies at 300-metre resolution with near-daily global coverage; Sentinel-5P TROPOMI, an atmospheric sensor relevant for detecting secondary hazards like methane releases from flooded wetlands; the Copernicus Land Monitoring Service, which provides the EU Digital Elevation Model and the Global Surface Water archive for baseline flood risk assessment; and the Copernicus Data Space Ecosystem, which is the unified STAC access platform for all Sentinel data — the same API we used in the previous labs.

---

## Capture 7 — `python scripts/build_catalog.py`

**Show:** Terminal output.

**Say:**
The build script reads all eight provider metadata files and federates them into a single catalog. This is the same federation principle from the earlier labs — providers remain independent, metadata is shared through a common layer. Each provider's score shows how many of the five operational requirements it covers.

---

## Capture 8 — `python scripts/discover.py`

**Show:** Terminal output — the full provider list.

**Say:**
The discovery tool gives a unified view of all registered resources. A user can browse the entire data space from a single interface without knowing the individual provider APIs. You can see the eight providers, their organisations, and their requirement coverage at a glance.

---

## Capture 9 — `python scripts/discover.py --requirement cloudy_conditions`

**Show:** Terminal output.

**Say:**
Filtering by operational requirement immediately shows which resources are usable under cloudy conditions — which is the most common situation during an active flood event. Six of eight providers are suitable. Crucially, Sentinel-2 and Sentinel-3 are not, because they are optical sensors. An operator responding to a flood under cloud cover should go straight to Sentinel-1 or the Copernicus Emergency Management Service.

---

## Capture 10 — `python scripts/discover.py --provider sentinel_1`

**Show:** Terminal output — full provider detail. Scroll slowly.

**Say:**
The full provider view gives everything needed to assess and access a resource: sensor type, spatial resolution, revisit time, the API endpoint, and for each operational requirement, the specific technical reasoning behind whether it is supported. This is how a user selects a resource for a specific operational situation.

---

## Capture 11 — `python scripts/compare.py sentinel_1 sentinel_2`

**Show:** Terminal output. Scroll to show the requirements table and strengths and limitations.

**Say:**
The comparison tool places two resources side by side. Here Sentinel-1 versus Sentinel-2 — both support flood detection and extent assessment, but only Sentinel-1 supports cloudy conditions and night operations. Sentinel-2 offers 10-metre resolution in the visible bands and dedicated water detection channels, but it is completely blocked by cloud cover. During an active flood event, Sentinel-1 is the primary choice; Sentinel-2 becomes valuable in post-event clear-sky windows.

---

## Capture 12 — `python scripts/compare.py --matrix`

**Show:** Terminal output — the full coverage matrix.

**Say:**
The coverage matrix gives the complete picture across all eight providers and all five requirements. The only requirement with 100% provider coverage is emergency response — every resource in the data space contributes something to emergency coordination. Flood detection is supported by five of eight providers, with the gaps coming from EUMETSAT, CLMS, and Sentinel-5P — none of which directly detect surface flooding, but all of which play supporting roles.

---

## Capture 13 — `python scripts/live_query.py --start 2024-09-01T00:00:00Z --end 2024-09-15T23:59:59Z --limit 5`

**Show:** Terminal — let it run, then scroll through the full output.

**Say:**
The live query script connects directly to the Copernicus Data Space Ecosystem STAC API — the same API from Labs 7 and 8. It queries Sentinel-1 GRD and Sentinel-2 L2A over Central Europe for a two-week window. Sentinel-1 returns five available products with real acquisition IDs — all-weather, confirmed accessible. Sentinel-2 also returns five products, but with an average cloud cover of 64%, which directly demonstrates why it cannot be relied on during active flood events. The scenario section translates this into operational guidance: for a cloudy active flood event, Sentinel-1 is available. For post-event assessment in clear sky, both are available. The metadata-only providers — EUMETSAT, Copernicus EMS, CLMS — are documented with their external access points.

---

## Capture 14 — `python scripts/report.py` (scroll to FEDERATION SUMMARY)

**Show:** Let the full output scroll, then pause on the FEDERATION SUMMARY section at the bottom.

**Say:**
The final report consolidates everything: the provider registry, requirement coverage per resource, the full coverage matrix, and per-provider technical detail. The federation summary shows eight EO resources from six independent organisations, spanning five different resource types — satellite missions, an emergency service, a land monitoring service, a meteorological agency, and a platform. This is the complete Federated EO Data Space for the National Flood Monitoring service.

---

## Capture 15 — `scripts/live_query.py` source in VS Code

**Show:** Scroll through the script — enough to show the STAC query logic and provider loop.

**Say:**
The implementation builds directly on the patterns from the previous labs — JSON-based provider metadata, a federation script that aggregates across providers, discovery and comparison tools, and a live STAC API query using the Copernicus Data Space Ecosystem endpoint. All source code and reports are available in the repository.

---

## Capture 16 — GitHub repository in browser

**Show:** `github.com/CarlosRzUb/DataSpacesRepo` with the `flood-monitoring-space/` folder visible.

**Say:**
The full implementation is available in the repository. The flood-monitoring-space directory contains all provider metadata, federation scripts, the generated catalog, and all reports. Thank you.
