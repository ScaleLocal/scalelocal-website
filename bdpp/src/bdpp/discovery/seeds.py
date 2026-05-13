"""Verified ATS seed tokens — each token confirmed to return a non-empty job list
against the public Greenhouse / Lever endpoints at scaffold time.

To refresh: rerun the seed-harvest agent. Tokens decay over time as companies switch ATS providers.
"""

GREENHOUSE_SEED_TOKENS: list[str] = sorted(set([
    # Verified live (May 2026)
    "markforged", "formlabs", "seurat", "neocybernetica", "piaggiofastforward",
    "factorialenergy", "foundenergy", "thirdpoleinc", "elevatebio",
    "andurilindustries", "flagshippioneeringinc", "lightmatter", "ketryx",
    "queracomputinginc", "cambridgeconsultantslimited", "locusrobotics",
    "manifoldbio", "biosphere", "amylyx", "pathai", "fractylhealthinc",
    "indigo", "tulip", "beaconbiosignals", "rebuildmanufacturing",
    "alarmcom", "betatechnologiesinc", "lexingtonmedical", "freeformfuturecorp",
    "aon3d", "morsecorp", "morsecorpcoop", "lilasciences",
    "horizonsurgicalsystems", "rti", "viamrobotics",
    "systemstechnologyresearch", "iterativehealth", "hark", "linushealth",
    "vicarioussurgical", "biofourmis", "butlr",
    # Legacy seeds (some may have decayed but kept in for low-cost retries)
    "desktopmetal", "irobot", "bostondynamics", "veo", "moderna",
    "alnylam", "vertexpharmaceuticals", "ginkgobioworks", "biogen",
]))

LEVER_SEED_TOKENS: list[str] = sorted(set([
    # Verified live (May 2026)
    "whoop", "boston-materials", "cfsenergy", "voltalabs", "reekon-tools",
    "picklerobot", "merlinlabs", "lumafield", "runlaminar", "tutorintelligence",
    "isee", "rapidmicrobio", "rai", "pattern", "cellares", "Regentcraft",
    # Legacy
    "berkshire-grey", "ambri", "form-energy", "factorial", "indigo", "indigoag",
    "shieldai", "anduril", "saildrone", "joby", "atom-power", "tulip",
]))


# Known New England manufacturers (independent of ATS — used by the company-first
# discovery layer to crawl careers pages directly).
KNOWN_NE_MANUFACTURERS: list[dict] = [
    {"name": "Axcelis Technologies", "website": "https://www.axcelis.com", "city": "Beverly", "state": "MA", "what": "Ion implantation systems for semiconductor manufacturing"},
    {"name": "MKS Instruments", "website": "https://www.mks.com", "city": "Andover", "state": "MA", "what": "Process control instruments for semiconductor and industrial applications"},
    {"name": "Brooks Automation", "website": "https://www.brooks.com", "city": "Chelmsford", "state": "MA", "what": "Precision robotics for semiconductor fabs"},
    {"name": "Symbotic", "website": "https://www.symbotic.com", "city": "Wilmington", "state": "MA", "what": "AI-powered robotic warehouse automation systems"},
    {"name": "Boston Conveyor & Automation", "website": "https://bostonconveyor.com", "city": "Newburyport", "state": "MA", "what": "Robotic conveyor and automation systems"},
    {"name": "Reiser", "website": "https://www.reiser.com", "city": "Canton", "state": "MA", "what": "Food processing and packaging equipment"},
    {"name": "Symmons Industries", "website": "https://www.symmons.com", "city": "Braintree", "state": "MA", "what": "Commercial showers, faucets and plumbing products"},
    {"name": "Watts Water Technologies", "website": "https://www.watts.com", "city": "North Andover", "state": "MA", "what": "Plumbing, heating and water-quality valves"},
    {"name": "Haartz Corporation", "website": "https://www.haartz.com", "city": "Acton", "state": "MA", "what": "Automotive convertible toppings and laminates"},
    {"name": "Kollmorgen", "website": "https://www.kollmorgen.com", "city": "Northampton", "state": "MA", "what": "Motion control systems and electro-optical equipment"},
    {"name": "Tegra Medical", "website": "https://www.tegramedical.com", "city": "Franklin", "state": "MA", "what": "Contract medical device manufacturing"},
    {"name": "Primo Medical Group", "website": "https://www.primomedicalgroup.com", "city": "Dedham", "state": "MA", "what": "Medical / aerospace / defense contract manufacturing"},
    {"name": "Boyd Coatings Research", "website": "https://www.boydcoatings.com", "city": "Hudson", "state": "MA", "what": "High-performance coatings"},
    {"name": "Tecomet", "website": "https://www.tecomet.com", "city": "Wilmington", "state": "MA", "what": "Precision medical and aerospace components"},
    {"name": "ARCH Medical Solutions Woburn", "website": "https://arch-medical.com", "city": "Woburn", "state": "MA", "what": "Precision medical / aerospace contract manufacturing"},
    {"name": "Machine Inc.", "website": "https://machineinc.com", "city": "Hopedale", "state": "MA", "what": "AS9100 precision aerospace machined components"},
    {"name": "B & E Group", "website": "https://www.begroupllc.com", "city": "Southwick", "state": "MA", "what": "Complex precision-machined airframe parts"},
    {"name": "Hitchiner Manufacturing", "website": "https://www.hitchiner.com", "city": "Milford", "state": "NH", "what": "Ferrous investment castings for aerospace/automotive"},
    {"name": "Hypertherm Associates", "website": "https://www.hypertherm.com", "city": "Hanover", "state": "NH", "what": "Industrial plasma, laser and waterjet cutting systems"},
    {"name": "Cirtronics", "website": "https://www.cirtronics.com", "city": "Milford", "state": "NH", "what": "Contract electronics manufacturing"},
    {"name": "EPTAM Precision", "website": "https://eptam.com", "city": "Northfield", "state": "NH", "what": "Precision CNC machining of plastics"},
    {"name": "ARCH Medical Solutions Seabrook", "website": "https://arch-medical.com", "city": "Seabrook", "state": "NH", "what": "Precision medical device manufacturing"},
    {"name": "Roberson Machine Company", "website": "https://robersontool.com", "city": "Bedford", "state": "NH", "what": "Precision CNC contract manufacturing"},
    {"name": "Vantedge Medical", "website": "https://vantedgemedical.com", "city": "Pelham", "state": "NH", "what": "Precision metal components for medical OEMs"},
    {"name": "W.H. Bagshaw", "website": "https://www.whbagshaw.com", "city": "Nashua", "state": "NH", "what": "Precision turned components"},
    {"name": "Felton Brush", "website": "https://www.feltonbrush.com", "city": "Londonderry", "state": "NH", "what": "Sheet metal, machining, wire harness assembly"},
    {"name": "New England Wire Technologies", "website": "https://newenglandwire.com", "city": "Lisbon", "state": "NH", "what": "Custom cable and wire"},
    {"name": "TURBOCAM International", "website": "https://www.turbocam.com", "city": "Barrington", "state": "NH", "what": "5-axis machined turbomachinery components"},
    {"name": "manroland Goss web systems", "website": "https://manrolandgoss.com", "city": "Durham", "state": "NH", "what": "Web offset printing presses"},
    {"name": "Sturm, Ruger & Co. Newport", "website": "https://www.ruger.com", "city": "Newport", "state": "NH", "what": "Firearms manufacturing"},
    {"name": "Mack Molding", "website": "https://www.mack.com", "city": "Arlington", "state": "VT", "what": "Plastic injection molding contract manufacturing"},
    {"name": "Mack Technologies", "website": "https://www.macktech.com", "city": "Westford", "state": "MA", "what": "PCBA and electronic contract manufacturing"},
    {"name": "GW Plastics", "website": "https://www.gwplastics.com", "city": "Bethel", "state": "VT", "what": "Injection-molded thermoplastics"},
    {"name": "OnLogic", "website": "https://www.onlogic.com", "city": "South Burlington", "state": "VT", "what": "Industrial and embedded rugged computers"},
    {"name": "Beta Technologies", "website": "https://www.beta.team", "city": "South Burlington", "state": "VT", "what": "Electric vertical-takeoff aircraft"},
    {"name": "Edlund Company", "website": "https://www.edlundco.com", "city": "Burlington", "state": "VT", "what": "Stainless-steel foodservice equipment"},
    {"name": "Revision Military", "website": "https://revisionmilitary.com", "city": "Essex Junction", "state": "VT", "what": "Protective eyewear and helmet systems"},
    {"name": "Burton Snowboards", "website": "https://www.burton.com", "city": "Burlington", "state": "VT", "what": "Snowboards and snowboarding equipment"},
    {"name": "Vermont Composites", "website": "https://vermontcomposites.com", "city": "Bennington", "state": "VT", "what": "Aerospace and medical composite structures"},
    {"name": "GS Precision", "website": "https://www.gsprecision.com", "city": "Brattleboro", "state": "VT", "what": "CNC-machined aerospace turbine components"},
    {"name": "Toray Plastics America", "website": "https://www.toraytpa.com", "city": "North Kingstown", "state": "RI", "what": "Polypropylene/polyester films"},
    {"name": "VIBCO Vibrators", "website": "https://www.vibco.com", "city": "Wyoming", "state": "RI", "what": "Industrial and construction vibrators"},
    {"name": "AstroNova", "website": "https://www.astronovainc.com", "city": "West Warwick", "state": "RI", "what": "Specialty printers and aerospace test systems"},
    {"name": "Coto Technology", "website": "https://www.cotorelay.com", "city": "North Kingstown", "state": "RI", "what": "Reed relays, switches and sensors"},
    {"name": "Advanced Interconnections Corp.", "website": "https://www.advanced.com", "city": "West Warwick", "state": "RI", "what": "Semiconductor sockets and interconnects"},
    {"name": "Swissline Precision", "website": "https://www.swisslineprecision.com", "city": "Cumberland", "state": "RI", "what": "Swiss-turned precision components"},
    {"name": "Lavigne Manufacturing", "website": "https://www.lavignemfg.com", "city": "Cranston", "state": "RI", "what": "ISO 9001 precision CNC machining"},
    {"name": "Ward's Manufacturing", "website": "https://www.wardsmanufacturing.com", "city": "Pawtucket", "state": "RI", "what": "Sheet metal fabrication and CNC services"},
    {"name": "FarSounder", "website": "https://www.farsounder.com", "city": "Warwick", "state": "RI", "what": "3D forward-looking sonar systems"},
    {"name": "Fiber Materials Inc.", "website": "https://www.fibermaterialsinc.com", "city": "Biddeford", "state": "ME", "what": "Advanced composite materials"},
    {"name": "Howe & Howe Technologies", "website": "https://www.howeandhowe.com", "city": "Waterboro", "state": "ME", "what": "Robotic and tracked defense vehicles"},
    {"name": "Lanco Assembly Systems", "website": "https://www.lancoassembly.com", "city": "Westbrook", "state": "ME", "what": "Automated assembly and packaging machinery"},
    {"name": "Auburn Manufacturing", "website": "https://www.auburnmfg.com", "city": "Mechanic Falls", "state": "ME", "what": "High-temperature textiles"},
    {"name": "Ocean Renewable Power Company", "website": "https://orpc.co", "city": "Portland", "state": "ME", "what": "Marine and river current power generation"},
    {"name": "IDEXX Laboratories", "website": "https://www.idexx.com", "city": "Westbrook", "state": "ME", "what": "Veterinary and clinical diagnostic equipment"},
]
