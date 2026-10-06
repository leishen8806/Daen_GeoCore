# Cleanup Manifest

| Source File | Section | Action | Destination | Reason |
|---|---|---|---|---|
| `DAEN_GeoCore_项目战略与产品总纲_V1.1.docx` | Brand direction and Cambodia Location Infrastructure | KEEP | `01_STRATEGY/`, `04_BRAND/` | Directly supports the current location-infrastructure baseline |
| `DAEN_GeoCore_项目战略与产品总纲_V1.1.docx` | DAEN ID, Places, Access, Route, Mobility, Logistics, API / Cloud | KEEP | `01_STRATEGY/`, `04_BRAND/` | Capability candidates are directly related to Geo Core |
| `DAEN_GeoCore_项目战略与产品总纲_V1.1.docx` | M1 place-data validation principle | REWRITE_FOR_CLARITY | `01_STRATEGY/DAEN_GEO_CORE_STRATEGY.md` | Kept as a validation principle without inventing M1 scope |
| `DAEN_GeoCore_项目战略与产品总纲_V1.1.docx` | Virtual office, Agent and office interaction sections | REMOVE_FROM_ACTIVE_BASELINE | `archive/` | Unrelated to the Geo Core location-infrastructure baseline |
| `DAEN_GeoCore_项目战略与产品总纲_V1.1.docx` | Historical model-routing discussion | REMOVE_FROM_ACTIVE_BASELINE | `archive/` | Tool/model routing is not a Geo Core decision |
| `DAEN产品需求边界技术与品牌方案_V1.0.docx` | Geo Core is infrastructure, not a map app | EXTRACT | `01_STRATEGY/DAEN_GEO_CORE_STRATEGY.md` | Directly supports product boundary |
| `DAEN产品需求边界技术与品牌方案_V1.0.docx` | Provider Adapter, PostgreSQL, modular monolith, no Kubernetes, no nationwide basemap | EXTRACT | `01_STRATEGY/DAEN_GEO_CORE_STRATEGY.md` | Retained as historical recommendations, not final architecture |
| `DAEN产品需求边界技术与品牌方案_V1.0.docx` | Place, address, coordinates, source and precision | EXTRACT | `01_STRATEGY/DAEN_GEO_CORE_STRATEGY.md` | Directly relevant location-infrastructure context |
| `DAEN产品需求边界技术与品牌方案_V1.0.docx` | Organization, Member, Membership, Agent, Runtime and workflow object model | REMOVE_FROM_ACTIVE_BASELINE | `archive/` | Belongs to a different product context |
| `DAEN产品需求边界技术与品牌方案_V1.0.docx` | Virtual office and AI organization positioning | REMOVE_FROM_ACTIVE_BASELINE | `archive/` | Conflicts with the current Geo Core baseline |
| `DAEN产品需求边界技术与品牌方案_V1.0.docx` | DAEN / ដែន / 域联 brand and mission line | EXTRACT | `04_BRAND/DAEN_BRAND_STRATEGY.md` | Directly relevant brand material; status preserved |
| `BRAND_STRATEGY.md` | DAEN, ដែន, 域联, positioning and candidate products | KEEP | `04_BRAND/DAEN_BRAND_STRATEGY.md` | Brand baseline |
| `BRAND_STRATEGY.md` | Trademark, Khmer usage and availability claims | REWRITE_FOR_CLARITY | `04_BRAND/DAEN_BRAND_STRATEGY.md` | Preserved as pending verification, not confirmed facts |
| `ENGINEERING_WORKFLOW.md` | Scope, Non-scope, acceptance, build, test, review and human acceptance | EXTRACT | `01_STRATEGY/DAEN_GEO_CORE_STRATEGY.md` | General method retained only at the M1 principle level |
| `ENGINEERING_WORKFLOW.md` | Tool/model routing discussion | REMOVE_FROM_ACTIVE_BASELINE | `archive/` | Not a Geo Core technical decision |
| `PRODUCT_DIRECTION.md` | Virtual office and Agent product direction | ARCHIVE | `archive/` | Unrelated project context; source remains unchanged |
| `README.md` | Historical cross-project links and status | ARCHIVE | `archive/` | Root README is a project history index, not the cleaned active baseline |

## Decision status after cleanup

- `CONFIRMED`: only source-supported current boundary statements and the working terms explicitly allowed by the cleanup brief.
- `RECOMMENDED`: retained historical direction such as Provider Adapter, PostgreSQL, modular monolith and source recording.
- `CANDIDATE`: brand positioning and capability names not formally frozen.
- `TBD`: missing customer, M1, data, quality, API and operating details.
- `ARCHIVED`: unrelated historical project context.
