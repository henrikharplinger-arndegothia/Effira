#!/usr/bin/env python3
"""
NIBE partner pipeline: parse sitemap URLs → score → write CSVs.
Run: python3 parse_and_score.py
"""

import csv, re, os

# ── Elzon mapping ──────────────────────────────────────────────────────────────
# Exact city → elzon (lowercase, stripped)
SE1_CITIES = {
    "lulea","umea","skelleftea","kiruna","gallivare","pitea","boden","kalix",
    "haparanda","arvidsjaur","arjeplog","jokkmokk","overkalix","overtornea",
    "pajala","malaa","norsjoe","byske","obbola","robertsfors","nordmaling",
    "vilhelmina","lycksele","blattnicksele","asele","storuman","sorsele",
    "dorotea","stromstrom","bjorn","jorn","stenmansmark","vasterbotten"
}
SE2_CITIES = {
    "gavle","falun","mora","ostersund","sundsvall","borlange","rattvik",
    "leksand","orsa","malung","orsa","avesta","hedemora","ludvika","smedjebacken",
    "kopparberg","ljusnarsberg","fagersta","norberg","sala","sandviken","hofors",
    "ockelbo","soderhamn","ljusne","bollnas","hudiksvall","ornskoldsvik",
    "harnosand","kramfors","solleftea","timra","alnoe","bergvara","stugun",
    "hammerdal","undersaker","bruksvallarna","hede","sveg","gallivare",
    "indal","matfors","stode","stenstavik","helgum","hogsten","nordmaling",
    "hogdalen","alno","bjorkback","norra"
}
SE4_CITIES = {
    "malmo","helsingborg","lund","kristianstad","hassleholm","ystad","karlskrona",
    "ronneby","karlshamn","solvesborg","trelleborg","vellinge","staffanstorp",
    "burlöv","svedala","lomma","kävlinge","kavlinge","eslöv","eslov","höör","hoor",
    "höganäs","hoganas","ängelholm","angelholm","åstorp","astorp","klippan",
    "perstorp","orkelljunga","osby","ösby","simrishamn","tomelilla","sjöbo",
    "sjoebo","skurup","landskrona","bjuv","svalöv","svalov","hyllinge","harslov",
    "vellinge","billinge","limhamn","loddekopinge","hollviken","klagshamn",
    "gualov","almhult","tingsryd","alvesta","ljungby","lagan","vaxjo",
    "asarum","svangsta","jamjo","fagelmara","ronneby","backaryd","soderakra",
    "garsnas","vitemolla","brösarp","brosarp","ronneby"
}

def city_to_elzon(city_raw):
    c = city_raw.lower().strip()
    # exact match first
    if c in SE1_CITIES: return "SE1"
    if c in SE4_CITIES: return "SE4"
    if c in SE2_CITIES: return "SE2"
    # postal-code prefix fallback
    return "SE3"

def postal_to_elzon(postal):
    """Use first 2 digits of postal code as region hint."""
    p = postal.replace(" ", "").replace("-", "")
    if not p or not p[0].isdigit(): return None
    prefix = int(p[:2])
    if prefix >= 96:   return "SE1"   # 960–999 Norrbotten/Västerbotten
    if 90 <= prefix <= 95: return "SE1"  # Umeå area
    if 80 <= prefix <= 89: return "SE2"  # Gävle/Sundsvall/Härnösand/Östersund
    if 77 <= prefix <= 79: return "SE2"  # Dalarna
    if 83 <= prefix <= 84: return "SE2"  # Jämtland
    if 20 <= prefix <= 29: return "SE4"  # Skåne
    if 37 <= prefix <= 38: return "SE4"  # Blekinge/Kronoberg south
    return "SE3"

def slug_to_name(slug):
    """Convert URL slug to company name."""
    # remove trailing type
    s = re.sub(r'-(installator|service)$', '', slug)
    # remove postal+city suffix: --city-12345
    s = re.sub(r'--[a-z][\w-]*-\d{5}$', '', s)
    s = re.sub(r'--[a-z][\w-]*-[a-z][\w-]*-\d{5}$', '', s)
    # replace -- with &
    s = s.replace('--', ' & ')
    # replace - with space
    s = s.replace('-', ' ')
    # title case
    s = s.title()
    return s.strip()

def parse_url(url):
    """Extract (company_name, city, postal, partner_type) from URL slug."""
    url = url.strip()
    m = re.search(r'/sv-se/partner/(.+)$', url)
    if not m: return None
    slug = m.group(1)

    # Extract type
    ptype = "installator"
    if slug.endswith("-service"): ptype = "service"
    elif slug.endswith("-installator"): ptype = "installator"

    # Extract postal code (5 digits) and city from end of slug
    # pattern: ..--city-12345-type OR --city-city2-12345-type
    pm = re.search(r'--([a-z][\w-]*?)-(\d{5})-(installator|service)$', slug)
    if pm:
        city_slug = pm.group(1)
        postal = pm.group(2)
    else:
        city_slug = ""
        postal = ""

    city = city_slug.replace('-', ' ').title()

    # Company name: everything before the -- city part
    company_slug = re.sub(r'--[a-z][\w-]*-\d{5}-(installator|service)$', '', slug)
    company_slug = re.sub(r'-(installator|service)$', '', company_slug)
    # Clean up
    company_name = company_slug.replace('--', ' & ').replace('-', ' ').strip().title()
    # Fix common patterns
    company_name = re.sub(r'\s+', ' ', company_name)

    return {
        "company_name": company_name,
        "city": city,
        "postal_code": postal[:3] + " " + postal[3:] if len(postal) == 5 else postal,
        "partner_type": ptype,
        "source_url": url,
    }

# ── Filtering ──────────────────────────────────────────────────────────────────
EXCLUDE_NAMES = {"comfort", "bad & varme", "bad varme", "rorgroepen", "rörgroepen"}

def should_exclude(company_name):
    name_lower = company_name.lower()
    for excl in EXCLUDE_NAMES:
        if excl in name_lower:
            return True
    return False

# ── Scoring ────────────────────────────────────────────────────────────────────
def score(row):
    elzon = row["elzon"]
    ptype = row["partner_type"]

    elzon_pts = {"SE4": 4, "SE3": 3, "SE2": 2, "SE1": 1}.get(elzon, 2)
    # installator = both sell+install = highest cert; service = service-only = standard
    cert_pts = 2 if ptype == "installator" else 1
    total = elzon_pts + cert_pts

    if total >= 6: tier = "A"
    elif total >= 4: tier = "B"
    else: tier = "C"

    return total, tier

# ── All URLs ───────────────────────────────────────────────────────────────────
ALL_URLS = """
https://www.nibe.eu/sv-se/partner/elan-el--vvs-ab--ystad-27139-installator
https://www.nibe.eu/sv-se/partner/vvs-cirkeln-i-lund-ab--staffanstorp-24593-installator
https://www.nibe.eu/sv-se/partner/elan-el--vvs-ab--simrishamn-27236-installator
https://www.nibe.eu/sv-se/partner/4t-energy-consulting-ab--hollviken-23632-installator
https://www.nibe.eu/sv-se/partner/a.j.ws-lift--rorteknik-ab--sundsvall-85231-installator
https://www.nibe.eu/sv-se/partner/a.-wiklund-vvs--stugun-84451-installator
https://www.nibe.eu/sv-se/partner/aa-kyl--energiteknik-ab--savsjo-57633-installator
https://www.nibe.eu/sv-se/partner/ab-boras-rorinstallationer--boras-50446-installator
https://www.nibe.eu/sv-se/partner/abk-vvs-installation--kungsbacka-43437-installator
https://www.nibe.eu/sv-se/partner/adtec-vvs-i-kalmar-ab--kalmar-39351-installator
https://www.nibe.eu/sv-se/partner/agge--oskars-ror-ab--aneby-57892-installator
https://www.nibe.eu/sv-se/partner/ag-rorteknik-ab--gislaved-33236-installator
https://www.nibe.eu/sv-se/partner/aircontrol-i-boras-ab--boras-50467-service
https://www.nibe.eu/sv-se/partner/a-j-thermopump-ab--bankeryd-56491-installator
https://www.nibe.eu/sv-se/partner/almgren-karlsam-vvs-ab--trollhattan-46138-installator
https://www.nibe.eu/sv-se/partner/alno-vvs-ab--alno-86592-installator
https://www.nibe.eu/sv-se/partner/alstermo-vvs-ab--alstermo-36443-installator
https://www.nibe.eu/sv-se/partner/am-villabutiken-ab--limhamn-21616-installator
https://www.nibe.eu/sv-se/partner/anders-johanssons-energiteknik-vvs--ab--ankarsrum-59370-service
https://www.nibe.eu/sv-se/partner/anders-johanssons-vvs--energiteknik-ab--ankarsrum-59370-installator
https://www.nibe.eu/sv-se/partner/andersson-jan-olof-peter--gallo-84394-installator
https://www.nibe.eu/sv-se/partner/backaryds-vvs-ab--backaryd-37296-installator
https://www.nibe.eu/sv-se/partner/bad--varme-stromstad--stromstad-45233-installator
https://www.nibe.eu/sv-se/partner/beckmanns-vvs--energiteknik--jonkoping-55302-service
https://www.nibe.eu/sv-se/partner/benor-solar-ab--vastra-frolunda-42166-installator
https://www.nibe.eu/sv-se/partner/benor-solar-ab--vaxjo-35244-installator
https://www.nibe.eu/sv-se/partner/beo-vvs-en-del-av-sandbackens-ror--varberg-43232-installator
https://www.nibe.eu/sv-se/partner/bergstrands-vvs-ab--kungsor-73632-installator
https://www.nibe.eu/sv-se/partner/bergvarme--ventilation-i-stockholm-ab--jarfalla-17562-installator
https://www.nibe.eu/sv-se/partner/bergvarme-ab--timra-86136-installator
https://www.nibe.eu/sv-se/partner/bgs-kyl--varmeservice-ab--matfors-86431-installator
https://www.nibe.eu/sv-se/partner/bgs-kyl--varmeservice-ab--matfors-86431-service
https://www.nibe.eu/sv-se/partner/bj-varmemontage-ab--kvicksund-63531-installator
https://www.nibe.eu/sv-se/partner/bj-varmemontage-ab--kvicksund-63531-service
https://www.nibe.eu/sv-se/partner/blekinge-rortjanst-ab--ronneby-37237-installator
https://www.nibe.eu/sv-se/partner/blekinge-varmeservice-ab--asarum-37492-installator
https://www.nibe.eu/sv-se/partner/blekinge-varmeservice-ab--asarum-37492-service
https://www.nibe.eu/sv-se/partner/anderssons-vvs-ab--anderstorp-33431-installator
https://www.nibe.eu/sv-se/partner/anton-o-simons-vvs-ab--falkenberg-31132-installator
https://www.nibe.eu/sv-se/partner/aqua-support-i-vilhelmina-ab--vilhelmina-91299-installator
https://www.nibe.eu/sv-se/partner/arboga-rorservice-ab--arboga-73231-installator
https://www.nibe.eu/sv-se/partner/arons-vvs-ab--veddige-43266-installator
https://www.nibe.eu/sv-se/partner/ascy-ror--industri-ab--hagfors-68333-installator
https://www.nibe.eu/sv-se/partner/ascy-ror--industri-ab--hagfors-68333-service
https://www.nibe.eu/sv-se/partner/askersunds-brunnsborrning-ab--askersund-69691-installator
https://www.nibe.eu/sv-se/partner/assemblin-ventilation-ab-gallivare--gallivare-98238-service
https://www.nibe.eu/sv-se/partner/assemblin-ventilation-ab-norrland-kyla--skelleftea-93137-service
https://www.nibe.eu/sv-se/partner/assemblin-vs-ab--kristianstad-29159-installator
https://www.nibe.eu/sv-se/partner/assemblin-vs-ab--ronneby-37222-installator
https://www.nibe.eu/sv-se/partner/assemblin-vs-ab--trelleborg-23162-installator
https://www.nibe.eu/sv-se/partner/anderssons-rorinstallationer-ab-sture--ystad-27139-installator
https://www.nibe.eu/sv-se/partner/axelssons-rorservice--ydre-57060-installator
https://www.nibe.eu/sv-se/partner/b.-berghs-olje--pannservice-hb--vendelso-13668-installator
https://www.nibe.eu/sv-se/partner/agesta-vvs-service--huddinge-14137-installator
https://www.nibe.eu/sv-se/partner/ake-lindkvist-ror-ab--mora-79233-installator
https://www.nibe.eu/sv-se/partner/ake-lindkvist-ror-ab--mora-79233-service
https://www.nibe.eu/sv-se/partner/akerbo-vvs-ab--lottorp-38772-installator
https://www.nibe.eu/sv-se/partner/akessons-rorteknik-ab--vislanda-34250-installator
https://www.nibe.eu/sv-se/partner/are-rorteam-ab--undersaker-83796-installator
https://www.nibe.eu/sv-se/partner/alvsborgs-vvs-hindas-lerum-ab--hindas-43853-installator
https://www.nibe.eu/sv-se/partner/angby-ror-ab--saltsjo-boo-13238-installator
https://www.nibe.eu/sv-se/partner/odsmals-rorlaggeri-ab--odsmal-44495-installator
https://www.nibe.eu/sv-se/partner/orebro-vvs-ab--orebro-70595-installator
https://www.nibe.eu/sv-se/partner/oregrunds-el--vvs-ab--oregrund-74242-installator
https://www.nibe.eu/sv-se/partner/oringe-ror-ab--tyreso-13549-installator
https://www.nibe.eu/sv-se/partner/ostgota-varmepumpsteknik--atvidaberg-59791-installator
https://www.nibe.eu/sv-se/partner/steffes-kyl--varmepumpar-ternstedt-invent-ab--atvidaberg-59724-service
https://www.nibe.eu/sv-se/partner/stenmans-vvs-ab--jorn-93651-installator
https://www.nibe.eu/sv-se/partner/stensborg-vvs-ab--fagelmara-37378-installator
https://www.nibe.eu/sv-se/partner/stenstans-varme--sanitet--sundsvall-85633-installator
https://www.nibe.eu/sv-se/partner/stenso-varme--sanitet-ab--kalmar-39246-installator
https://www.nibe.eu/sv-se/partner/stetab-vvs--brunnsborrning--stjarnhov-64651-installator
https://www.nibe.eu/sv-se/partner/stigs-rorlaggeri-ab--lindome-43722-installator
https://www.nibe.eu/sv-se/partner/stockholm-pool--varme-ab--huddinge-14143-installator
https://www.nibe.eu/sv-se/partner/stockholm-pool--varme-ab--huddinge-14143-service
https://www.nibe.eu/sv-se/partner/stockholms-ror--vvs-ab--------------lidingo-18132-installator
https://www.nibe.eu/sv-se/partner/stora-skedvi-ror-ab--stora-skedvi-78393-installator
https://www.nibe.eu/sv-se/partner/strangnas-rortjanst-ab--strangnas-64540-installator
https://www.nibe.eu/sv-se/partner/strombergs-ror-och-allservice-ab--asele-91932-installator
https://www.nibe.eu/sv-se/partner/stromlunds-ror-ab--trollhattan-46104-installator
https://www.nibe.eu/sv-se/partner/stromstad-rorservice-ab--stromstad-45292-installator
https://www.nibe.eu/sv-se/partner/stures-rorinstallationer-ab--borensberg-59031-installator
https://www.nibe.eu/sv-se/partner/sturko-jamjo-ror-och-varmeinstallationer-ab--jamjo-37372-installator
https://www.nibe.eu/sv-se/partner/stallets-rorlaggeri-ab--ytterby-44254-installator
https://www.nibe.eu/sv-se/partner/sundbyholms-vvs-ab--eskilstuna-63347-installator
https://www.nibe.eu/sv-se/partner/svenljunga-el-ab--svenljunga-51253-installator
https://www.nibe.eu/sv-se/partner/sven-olovs-el--vvs--upplands-vasby-19444-installator
https://www.nibe.eu/sv-se/partner/svenska-vpg-ab--umea-90321-installator
https://www.nibe.eu/sv-se/partner/svensk-installation-vast-ab--arjang-67231-installator
https://www.nibe.eu/sv-se/partner/svensk-kylservice-i-goteborg-ab--goteborg-41707-installator
https://www.nibe.eu/sv-se/partner/svensk-villavarme-ab--hisings-backa-42246-installator
https://www.nibe.eu/sv-se/partner/svenssons-ror-ab--bor-33174-installator
https://www.nibe.eu/sv-se/partner/sweror-ab--eskilstuna--------------------------63346-installator
https://www.nibe.eu/sv-se/partner/s-varme-ab--hallsberg-69435-installator
https://www.nibe.eu/sv-se/partner/s-varme-ab--hallsberg-69435-service
https://www.nibe.eu/sv-se/partner/soberg--soderstrom-ror-ab--gnesta-64634-installator
https://www.nibe.eu/sv-se/partner/soderbloms-ror-ab--gavle-80309-installator
https://www.nibe.eu/sv-se/partner/soderakra-vvs-ab--soderakra-38597-installator
https://www.nibe.eu/sv-se/partner/sodra-vi-varmepumpservice-ab--kisa-59040-installator
https://www.nibe.eu/sv-se/partner/sodregards-ror--maskin-ab--vaxjo-35593-installator
https://www.nibe.eu/sv-se/partner/sone-el-ab--lidkoping-53157-installator
https://www.nibe.eu/sv-se/partner/sone-el-ab--lidkoping-53157-service
https://www.nibe.eu/sv-se/partner/sorens-ror--stode-86496-installator
https://www.nibe.eu/sv-se/partner/taussons-ror-ab--uddevalla-45134-installator
https://www.nibe.eu/sv-se/partner/tbb-ror--vvs-service-ab--taby-18766-installator
https://www.nibe.eu/sv-se/partner/teknisk-fastighetsservice-ab--lycksele-92193-service
https://www.nibe.eu/sv-se/partner/teknisk-fastighetsservice-ab--skelleftea-93137-service
https://www.nibe.eu/sv-se/partner/termoklimat-i-skane-ab--ystad-27139-service
https://www.nibe.eu/sv-se/partner/termoklimat-skane-ab--svedala-23351-installator
https://www.nibe.eu/sv-se/partner/termoklimat-skane-ab--svedala-23351-service
https://www.nibe.eu/sv-se/partner/tf-service-ab--skelleftea-93137-installator
https://www.nibe.eu/sv-se/partner/themptander-vvs-ab--skogas-14250-installator
https://www.nibe.eu/sv-se/partner/thimsfors-vvs-ab--bastad-26942-installator
https://www.nibe.eu/sv-se/partner/thimsfors-vvs-ab--bastad-26942-service
https://www.nibe.eu/sv-se/partner/thimsfors-vvs-ab--markaryd-28540-service
https://www.nibe.eu/sv-se/partner/thimsfors-vvs-ab--skummeslovstrand-31272-installator
https://www.nibe.eu/sv-se/partner/thimsfors-vvs-ab--almhult-34334-installator
https://www.nibe.eu/sv-se/partner/thimsfors-vvs-ab--almhult-34334-service
https://www.nibe.eu/sv-se/partner/tim-svenssons-ror-ab--alvesta-34232-installator
https://www.nibe.eu/sv-se/partner/tinbak-ab--hammerdal-83349-installator
https://www.nibe.eu/sv-se/partner/tjallmo-vatten--varme-ab--tjallmo-59034-installator
https://www.nibe.eu/sv-se/partner/tomas-enoksson-rormokeri--fast.service--ostervala-74046-installator
https://www.nibe.eu/sv-se/partner/torbjornsgardens-vvs-ab--vara-53490-installator
https://www.nibe.eu/sv-se/partner/tps-ror-ab--kiruna-98143-installator
https://www.nibe.eu/sv-se/partner/trelleborgs-rorservice-ab--trelleborg-23163-installator
https://www.nibe.eu/sv-se/partner/trs---tingdahls-rorservice-ab--tingsryd-36230-installator
https://www.nibe.eu/sv-se/partner/ts-ror-ab--heby-74431-installator
https://www.nibe.eu/sv-se/partner/tullinge-ror-ab--tullinge-14638-installator
https://www.nibe.eu/sv-se/partner/tunabergs-vvs-ab--nykoping-61192-installator
https://www.nibe.eu/sv-se/partner/turex-ror-ab--saltsjo-boo-13235-installator
https://www.nibe.eu/sv-se/partner/wiklunds-kylteknik-ab--kungsbacka-43437-installator
https://www.nibe.eu/sv-se/partner/wikmans-vvs-ab--ekero-17961-installator
https://www.nibe.eu/sv-se/partner/vikstroms-vvs--grav-ab--skelleftea-93142-installator
https://www.nibe.eu/sv-se/partner/villavarme-i-ostergotland-ab--motala-59192-installator
https://www.nibe.eu/sv-se/partner/villavarme-i-ostergotland-ab--motala-59192-service
https://www.nibe.eu/sv-se/partner/villavarme-i-ostergotlandab--norrkoping-60238-installator
https://www.nibe.eu/sv-se/partner/vi-varmer-sverige-ab--huddinge-14140-installator
https://www.nibe.eu/sv-se/partner/vi-varmer-sverige-ab--hagersten-12630-installator
https://www.nibe.eu/sv-se/partner/vi-varmer-sverige-ab--hagersten-12630-service
https://www.nibe.eu/sv-se/partner/vi-varmer-sverige-ab--sollentuna-19278-installator
https://www.nibe.eu/sv-se/partner/vi-varmer-sverige-ab--taby-18766-installator
https://www.nibe.eu/sv-se/partner/votab-vvs--varmeinstallation-ab--varberg-43232-installator
https://www.nibe.eu/sv-se/partner/wrandings-rormokeri-ab--balsta-74631-installator
https://www.nibe.eu/sv-se/partner/vs-installation-i-kalmar-ab--kalmar-39356-installator
https://www.nibe.eu/sv-se/partner/vvs-akuten-i-sodertorn-ab--segersang-14840-installator
https://www.nibe.eu/sv-se/partner/vvsarn-i-blekinge-ab--svangsta-37692-installator
https://www.nibe.eu/sv-se/partner/vvs-installatoren-i-gavle-ab--gavle-80309-installator
https://www.nibe.eu/sv-se/partner/vvs-kompaniet-ab--saffle-66140-installator
https://www.nibe.eu/sv-se/partner/vvs-svepet-ab--loddekopinge-24631-installator
https://www.nibe.eu/sv-se/partner/vvs-teknik-i-jamtland-ab--stenstavik-84531-installator
https://www.nibe.eu/sv-se/partner/vvs-teknik-kristianstad-ab--kristianstad-29194-installator
https://www.nibe.eu/sv-se/partner/vvs-tjanst-i-falun-ab--falun-79143-installator
https://www.nibe.eu/sv-se/partner/vvs-tjanst-i-gualov-ab--gualov-29572-installator
https://www.nibe.eu/sv-se/partner/vvs-tjanst-i-solvesborg-ab--solvesborg-29471-installator
https://www.nibe.eu/sv-se/partner/vargarda-vvs-ab--vargarda-44735-installator
https://www.nibe.eu/sv-se/partner/vallsater-ror-ab--alunda-74792-installator
https://www.nibe.eu/sv-se/partner/vanersnas-rorservice-ab--vanersnas-46890-installator
https://www.nibe.eu/sv-se/partner/varme--konstruktionskansla-i-trosa-ab--trosa-61934-installator
https://www.nibe.eu/sv-se/partner/varme--sanitet-a.-palmer-ab--vimmerby-59840-installator
https://www.nibe.eu/sv-se/partner/varme--sanitet-i-huskvarna-ab--huskvarna-56132-installator
https://www.nibe.eu/sv-se/partner/varme-och-kylteknik-i-harjedalen-ab--hede-84093-service
https://www.nibe.eu/sv-se/partner/varmepumpsbolaget-i-kristianstad-ab--kristianstad-29194-installator
https://www.nibe.eu/sv-se/partner/varmepumpsgruppen-mitt-ab--eskilstuna-63346-installator
https://www.nibe.eu/sv-se/partner/varmeservice-i-veddige-ab--veddige-43266-installator
https://www.nibe.eu/sv-se/partner/varmeservice-i-veddige-ab--veddige-43266-service
https://www.nibe.eu/sv-se/partner/varmeservice-uddevalla-ab--uddevalla-45170-installator
https://www.nibe.eu/sv-se/partner/varmespecialisten-ab--kungsbacka-43442-installator
https://www.nibe.eu/sv-se/partner/varmia-syd-ab--harslov-26192-installator
https://www.nibe.eu/sv-se/partner/varnamo-forsheda-ror-ab--varnamo-33134-installator
https://www.nibe.eu/sv-se/partner/varnamo-forsheda-ror-ab--varnamo-33134-service
https://www.nibe.eu/sv-se/partner/vasterbotten-vvs-ab--byske-93451-installator
https://www.nibe.eu/sv-se/partner/vastkustkyl--varme-ab--alvangen-44632-installator
https://www.nibe.eu/sv-se/partner/vastsvenska-varme--sanitet-ab--ed-66832-installator
https://www.nibe.eu/sv-se/partner/yttergrens-ror-ab--visby-62154-installator
https://www.nibe.eu/sv-se/partner/taby-vvs--service-ab--taby-18746-installator
https://www.nibe.eu/sv-se/partner/talje-vvs-ab--sodertalje-15242-installator
https://www.nibe.eu/sv-se/partner/umeas-raka-rorinstallationer-ab--umea-90426-installator
https://www.nibe.eu/sv-se/partner/umia-ab--umea-90304-installator
https://www.nibe.eu/sv-se/partner/unnaryds-varme--sanitet-ab--unnaryd-31451-installator
https://www.nibe.eu/sv-se/partner/upplands-energi-produkt--miljo-ab--bjorklinge-74363-service
https://www.nibe.eu/sv-se/partner/upplands-energi-produkt--miljo-ab--uppsala-75450-installator
https://www.nibe.eu/sv-se/partner/upplands-kyl--varme-ab--uppsala-75323-installator
https://www.nibe.eu/sv-se/partner/upplands-kyl--varme-ab--uppsala-75323-service
https://www.nibe.eu/sv-se/partner/vadsbo-kylteknik-ab--moholm-54594-installator
https://www.nibe.eu/sv-se/partner/wahlgren-ror-ab--norrtalje-76172-installator
https://www.nibe.eu/sv-se/partner/walfridssons-ror-ab--lessebo-36531-installator
https://www.nibe.eu/sv-se/partner/walthers-kyl--varmepumpservice--nykoping-61145-installator
https://www.nibe.eu/sv-se/partner/walthers-kyl--varmepumpservice-ab--norrkoping-60223-service
https://www.nibe.eu/sv-se/partner/walthers-kyl--varmepumpservice-ab--nykoping-61145-service
https://www.nibe.eu/sv-se/partner/varmitek-energisystem-ab--helsingborg-25467-installator
https://www.nibe.eu/sv-se/partner/wastvinds-vvs-ab--koping-73136-installator
https://www.nibe.eu/sv-se/partner/vatten--varme-ab--gallivare-98238-installator
https://www.nibe.eu/sv-se/partner/vatten--varme-i-norberg--norberg-73835-installator
https://www.nibe.eu/sv-se/partner/vatten--varmeteknik-ab--hogsater-45870-installator
https://www.nibe.eu/sv-se/partner/vattenhuset-ab--borlange-78170-installator
https://www.nibe.eu/sv-se/partner/westheat-ab--hisings-backa-42246-service
https://www.nibe.eu/sv-se/partner/westman-vvs--kalix-95231-installator
https://www.nibe.eu/sv-se/partner/wfix-vvs--energi-ab--lulea-97341-installator
https://www.nibe.eu/sv-se/partner/vfs-varberg-ab--varberg-43232-installator
https://www.nibe.eu/sv-se/partner/wickmans-ror--vellinge-23532-installator
https://www.nibe.eu/sv-se/partner/steffes-kyl--varmepumpar-ternstedt-invent-ab--linkoping-58273-installator
https://www.nibe.eu/sv-se/partner/steffes-kyl--varmepumpar-ternstedt-invent-ab--linkoping-58273-service
https://www.nibe.eu/sv-se/partner/steffes-kyl--varmepumpar-ternstedt-invent-ab--rimforsa-59044-service
https://www.nibe.eu/sv-se/partner/zero-energi-ab--lund-22478-service
https://www.nibe.eu/sv-se/partner/tuvessons-vvs-ab--billinge-24195-installator
https://www.nibe.eu/sv-se/partner/tvaratrask-rorservice-ab--blattnicksele-92492-installator
https://www.nibe.eu/sv-se/partner/sp-rorservice--svenljunga-51293-installator
https://www.nibe.eu/sv-se/partner/widerbergs-ror--garsnas-27261-installator
https://www.nibe.eu/sv-se/partner/borlange-vvs-ab--borlange-78131-installator
https://www.nibe.eu/sv-se/partner/bo-gustavssons-ror-ab--ljungbyhed-26877-installator
https://www.nibe.eu/sv-se/partner/bohuslans-bergvarmepumpar-ab--kungshamn-45632-installator
https://www.nibe.eu/sv-se/partner/boken-vvs-ab--stromsholm-72581-installator
https://www.nibe.eu/sv-se/partner/boras-varme-ab--boras-50370-installator
https://www.nibe.eu/sv-se/partner/boras-vvs-ab--boras-50460-installator
https://www.nibe.eu/sv-se/partner/branninge-rorservice-ab--norrtalje-76140-installator
https://www.nibe.eu/sv-se/partner/bredvikens-ror-ab--varby-14251-installator
https://www.nibe.eu/sv-se/partner/brinnen-ror-ab--lindas-43491-installator
https://www.nibe.eu/sv-se/partner/brotorps-vvs--kil-66530-installator
https://www.nibe.eu/sv-se/partner/bruksvallens-ror-ab--bruksvallarna-84098-installator
https://www.nibe.eu/sv-se/partner/bunkeflo-ror-ab--vellinge-23532-installator
https://www.nibe.eu/sv-se/partner/carlssons-vvs--brottby-18494-installator
https://www.nibe.eu/sv-se/partner/celsius-energi-ab--umea-90330-installator
https://www.nibe.eu/sv-se/partner/celsius-energi-ab--umea-90330-service
https://www.nibe.eu/sv-se/partner/christer-lindbloms-ror-ab--skanninge-59570-installator
https://www.nibe.eu/sv-se/partner/comfort-zone-i-sverige-ab--halmstad-30261-installator
https://www.nibe.eu/sv-se/partner/d-j-rorsystem--kungshamn-45636-installator
https://www.nibe.eu/sv-se/partner/dala-ror-ab--falun-79132-installator
https://www.nibe.eu/sv-se/partner/dalaro-rorservice-ab--dalarso-13956-installator
https://www.nibe.eu/sv-se/partner/dale-ror-ab--dals-ed-66630-installator
https://www.nibe.eu/sv-se/partner/dalarnas-ror-ab--avesta-77431-installator
https://www.nibe.eu/sv-se/partner/daldala-ab--ljusnarsberg-71191-installator
https://www.nibe.eu/sv-se/partner/dalmarken-ror-ab--rattvik-79591-installator
https://www.nibe.eu/sv-se/partner/djupa-ror-ab--djuras-79195-installator
https://www.nibe.eu/sv-se/partner/dk-ror-ab--falkenberg-31195-installator
https://www.nibe.eu/sv-se/partner/dk-ror-ab--halmstad-30279-installator
https://www.nibe.eu/sv-se/partner/dr-ror-ab--gunnebo-57892-installator
https://www.nibe.eu/sv-se/partner/e.-m.-vvs-ab--nacka-13172-installator
https://www.nibe.eu/sv-se/partner/ea-energi-ab--upplands-vasby-19467-installator
https://www.nibe.eu/sv-se/partner/ea-vvs-installationer-ab--enkoping-74991-installator
https://www.nibe.eu/sv-se/partner/ekerums-ror-ab--borgholm-38795-installator
https://www.nibe.eu/sv-se/partner/eklunds-vvs-ab--oskarshamn-57237-installator
https://www.nibe.eu/sv-se/partner/ekbloms-rorinstallation-ab--nassjo-57173-installator
https://www.nibe.eu/sv-se/partner/el--vvs-vast-ab--kungsbacka-43441-installator
https://www.nibe.eu/sv-se/partner/el-partner-ab--skelleftea-93140-installator
https://www.nibe.eu/sv-se/partner/elcon-energi-ab--katrineholm-64140-installator
https://www.nibe.eu/sv-se/partner/elektrus-ab--goteborg-41467-installator
https://www.nibe.eu/sv-se/partner/elite-energi-ab--sundsvall-85454-installator
https://www.nibe.eu/sv-se/partner/emab-energi-ab--mariestad-54263-installator
https://www.nibe.eu/sv-se/partner/emab-energi-ab--lidkoping-53163-installator
https://www.nibe.eu/sv-se/partner/energi-akuten-i-stockholm-ab--stockholm-11534-installator
https://www.nibe.eu/sv-se/partner/energieffektiv-ab--vasteras-72231-installator
https://www.nibe.eu/sv-se/partner/energikompaniet-ab--gothenburg-41871-installator
https://www.nibe.eu/sv-se/partner/energipartner-i-norden-ab--solna-16934-installator
https://www.nibe.eu/sv-se/partner/energipartner-i-norden-ab--solna-16934-service
https://www.nibe.eu/sv-se/partner/enova-ab--boras-50445-installator
https://www.nibe.eu/sv-se/partner/enova-ab--gothenburg-41871-installator
https://www.nibe.eu/sv-se/partner/eorb-ab--ljungby-34132-installator
https://www.nibe.eu/sv-se/partner/espinge-el--vvs-ab--osby-28330-installator
https://www.nibe.eu/sv-se/partner/expert-rad-vvs-ab--gavle-80392-installator
https://www.nibe.eu/sv-se/partner/f-j-teknik-ab--vetlanda-57491-installator
https://www.nibe.eu/sv-se/partner/fagerlids-vvs-ab--leksand-79330-installator
https://www.nibe.eu/sv-se/partner/falks-ror-vvs-ab--eskilstuna-63360-installator
https://www.nibe.eu/sv-se/partner/falkenberg-ror-ab--falkenberg-31132-installator
https://www.nibe.eu/sv-se/partner/falkvarme-ab--falkenberg-31191-installator
https://www.nibe.eu/sv-se/partner/falun-varme-ab--falun-79173-installator
https://www.nibe.eu/sv-se/partner/faluns-rorservice-ab--falun-79138-installator
https://www.nibe.eu/sv-se/partner/farstas-rorinstallatorer-ab--stockholm-12362-installator
https://www.nibe.eu/sv-se/partner/filipstads-ror-ab--filipstad-68230-installator
https://www.nibe.eu/sv-se/partner/fjordans-ror-ab--lysekil-45381-installator
https://www.nibe.eu/sv-se/partner/fjordans-ror-ab--munkedal-45530-installator
https://www.nibe.eu/sv-se/partner/fjaras-rorinstallationer-ab--fjaras-43991-installator
https://www.nibe.eu/sv-se/partner/flen-rorservice-ab--flen-64233-installator
https://www.nibe.eu/sv-se/partner/forsvaret-ab--osthammar-74281-installator
https://www.nibe.eu/sv-se/partner/framtidens-uppvarmning-ab--stockholm-16879-installator
https://www.nibe.eu/sv-se/partner/frisens-ror-ab--linkoping-58275-installator
https://www.nibe.eu/sv-se/partner/frost-kyl-vvs-ab--boden-96137-installator
https://www.nibe.eu/sv-se/partner/frost-kyl-vvs-ab--boden-96137-service
https://www.nibe.eu/sv-se/partner/frostrings-ror-ab--gimo-74020-installator
https://www.nibe.eu/sv-se/partner/frosunda-ror-ab--harnosand-87137-installator
https://www.nibe.eu/sv-se/partner/gardsby-ror-ab--lenhovda-36194-installator
https://www.nibe.eu/sv-se/partner/gavle-ror-ab--gavle-80354-installator
https://www.nibe.eu/sv-se/partner/gisslarbo-ror-ab--gisslarbo-73591-installator
https://www.nibe.eu/sv-se/partner/gislavedsbygdens-ror-ab--gislaved-33221-installator
https://www.nibe.eu/sv-se/partner/gotlands-ror-ab--visby-62157-installator
https://www.nibe.eu/sv-se/partner/godings-vvs--kungsholmen-11228-installator
https://www.nibe.eu/sv-se/partner/grabo-ror--el-ab--grebbestad-45773-installator
https://www.nibe.eu/sv-se/partner/grabo-ror--el-ab--tanumshede-45730-installator
https://www.nibe.eu/sv-se/partner/gronkulla-ror-ab--nassjo-57131-installator
https://www.nibe.eu/sv-se/partner/gustafs-vvs--ab--torslanda-42365-installator
https://www.nibe.eu/sv-se/partner/hallbo-vvs-ab--hallsberg-69432-installator
https://www.nibe.eu/sv-se/partner/hallands-bergvarme-ab--kungsbacka-43491-installator
https://www.nibe.eu/sv-se/partner/hallands-bergvarme-ab--kungsbacka-43491-service
https://www.nibe.eu/sv-se/partner/hallands-el--vvs-ab--laholm-31233-installator
https://www.nibe.eu/sv-se/partner/hallstahammars-ror-ab--hallstahammar-73430-installator
https://www.nibe.eu/sv-se/partner/hammerbys-ror-ab--stockholm-12060-installator
https://www.nibe.eu/sv-se/partner/hardemo-ror-ab--hardemo-69493-installator
https://www.nibe.eu/sv-se/partner/hassleholms-rorservice-ab--hassleholm-28133-installator
https://www.nibe.eu/sv-se/partner/hedemoras-ror-ab--hedemora-77631-installator
https://www.nibe.eu/sv-se/partner/heimdall-byggtjanst-ab--akersberga-18430-installator
https://www.nibe.eu/sv-se/partner/helgums-ror--ventilation-ab--helgum-88291-installator
https://www.nibe.eu/sv-se/partner/hemvarmekonsulten-ab--akersberga-18432-installator
https://www.nibe.eu/sv-se/partner/hohanssons-ror-ab--fagersta-73740-installator
https://www.nibe.eu/sv-se/partner/hogbergs-ror--ventilation-ab--leksand-79332-installator
https://www.nibe.eu/sv-se/partner/hogdalens-ror-ab--stockholm-12454-installator
https://www.nibe.eu/sv-se/partner/hogstens-rorservice-ab--hogsten-87696-installator
https://www.nibe.eu/sv-se/partner/hosjo-ror-ab--ostersund-83152-installator
https://www.nibe.eu/sv-se/partner/hudiksvalls-rorservice-ab--hudiksvall-82431-installator
https://www.nibe.eu/sv-se/partner/humlevikens-ror--ab--kungsbacka-43494-installator
https://www.nibe.eu/sv-se/partner/husells-el--vvs-ab--heby-74476-installator
https://www.nibe.eu/sv-se/partner/hylte-rorservice-ab--torup-31460-installator
https://www.nibe.eu/sv-se/partner/indals-vvs-ab--indal-86497-installator
https://www.nibe.eu/sv-se/partner/j-e-rorinstallationer-ab--soderhamn-82671-installator
https://www.nibe.eu/sv-se/partner/j-j-rorservice-ab--ockelbo-81690-installator
https://www.nibe.eu/sv-se/partner/j-l-vvs-ab--sundbyberg-17273-installator
https://www.nibe.eu/sv-se/partner/jan-karlssons-ror-ab--munkedal-45526-installator
https://www.nibe.eu/sv-se/partner/jannes-vvs-ab--hoor-24333-installator
https://www.nibe.eu/sv-se/partner/janssons-ror-ab--obbola-90591-installator
https://www.nibe.eu/sv-se/partner/jkp-energi--ab--kopparberg-71494-installator
https://www.nibe.eu/sv-se/partner/johanneberg-ror-ab--fjaras-43991-installator
https://www.nibe.eu/sv-se/partner/jonkoping-installationstjanst-ab--jonkoping-55389-installator
https://www.nibe.eu/sv-se/partner/johanssons-vvs-ab--strangnas-64540-installator
https://www.nibe.eu/sv-se/partner/jordens-basta-vvs-ab--tranas-57390-installator
https://www.nibe.eu/sv-se/partner/js-vvs-i-norrtalje-ab--norrtalje-76130-installator
https://www.nibe.eu/sv-se/partner/j-thompsons-vvs-ab--tingsryd-36242-installator
https://www.nibe.eu/sv-se/partner/j-thompsons-vvs-ab--tingsryd-36242-service
https://www.nibe.eu/sv-se/partner/k-g-johanssons-ror-ab--nyhro-38975-installator
https://www.nibe.eu/sv-se/partner/kalmar-ror-ab--kalmar-39254-installator
https://www.nibe.eu/sv-se/partner/kalmarsunds-ror-ab--kalmar-39371-installator
https://www.nibe.eu/sv-se/partner/kalix-ror--ventilation-ab--kalix-95231-installator
https://www.nibe.eu/sv-se/partner/kangers-vvs-ab--hyssna-51163-installator
https://www.nibe.eu/sv-se/partner/karlshamns-vvs-ab--karlshamn-37432-installator
https://www.nibe.eu/sv-se/partner/karlskoga-rorservice-ab--karlskoga-69145-installator
https://www.nibe.eu/sv-se/partner/karlstads-vvs--lantbrukstjanst-ab--karlstad-65272-installator
https://www.nibe.eu/sv-se/partner/kungsors-ror-vvs-ab--kungsor-73632-installator
https://www.nibe.eu/sv-se/partner/kyle-vvs-ab--skara-53231-installator
https://www.nibe.eu/sv-se/partner/lakerols-ror-ab--kolboda-37040-installator
https://www.nibe.eu/sv-se/partner/landora-ror-ab--enkoping-74994-installator
https://www.nibe.eu/sv-se/partner/larssons-vvs-ab--nusnas-79295-installator
https://www.nibe.eu/sv-se/partner/lejonet-ror-ab--nassjo-57192-installator
https://www.nibe.eu/sv-se/partner/lena-vvs-ab--lena-74992-installator
https://www.nibe.eu/sv-se/partner/lerums-rorservice-ab--lerum-44335-installator
https://www.nibe.eu/sv-se/partner/leys-vvs-ab--lulea-97441-installator
https://www.nibe.eu/sv-se/partner/lf-energi-och-kyla-ab--orebro-70225-installator
https://www.nibe.eu/sv-se/partner/lindesberg-rostorp-ror-ab--lindesberg-71131-installator
https://www.nibe.eu/sv-se/partner/lindkvists-vvs-ab--nassjo-57136-installator
https://www.nibe.eu/sv-se/partner/lindqvists-ror-ab--boras-50449-installator
https://www.nibe.eu/sv-se/partner/linero-ror-ab--lund-22367-installator
https://www.nibe.eu/sv-se/partner/linkopings-vvs-ab--linkoping-58295-installator
https://www.nibe.eu/sv-se/partner/ljusne-ror-ab--ljusne-82691-installator
https://www.nibe.eu/sv-se/partner/lostagards-ror-ab--boras-50453-installator
https://www.nibe.eu/sv-se/partner/lovikka-ror-ab--pajala-98491-installator
https://www.nibe.eu/sv-se/partner/lulea-ror-ab--lulea-97266-installator
https://www.nibe.eu/sv-se/partner/lulea-vvs--energi-ab--lulea-97434-installator
https://www.nibe.eu/sv-se/partner/m-a-bergstrom-vvs-ab--ljungby-34132-installator
https://www.nibe.eu/sv-se/partner/magle-ror-ab--kavlinge-24362-installator
https://www.nibe.eu/sv-se/partner/magnus-peterssons-vvs-ab--kungsbacka-43431-installator
https://www.nibe.eu/sv-se/partner/maglehems-ror-ab--kristianstad-29194-installator
https://www.nibe.eu/sv-se/partner/malungs-ror-ab--malung-78270-installator
https://www.nibe.eu/sv-se/partner/marsta-vvs-ab--marsta-19551-installator
https://www.nibe.eu/sv-se/partner/masen-ror-ab--ornskoldsvik-89133-installator
https://www.nibe.eu/sv-se/partner/melander-ror-ab--borlange-78170-installator
https://www.nibe.eu/sv-se/partner/mellbyns-rorservice-ab--mellbystrand-31277-installator
https://www.nibe.eu/sv-se/partner/mellstrom-ror-ab--skene-51160-installator
https://www.nibe.eu/sv-se/partner/mellstroms-ror-ab--hoganas-26391-installator
https://www.nibe.eu/sv-se/partner/mercurius-energi-ab--nykoping-61145-installator
https://www.nibe.eu/sv-se/partner/mil-el-o-vvs-i-ostergotland-ab--linkoping-58275-installator
https://www.nibe.eu/sv-se/partner/mil-el-o-vvs-i-ostergotland-ab--linkoping-58275-service
https://www.nibe.eu/sv-se/partner/mill-energi-ab--nassjo-57134-installator
https://www.nibe.eu/sv-se/partner/mns-ror--energi-ab--sodra-sandby-24792-installator
https://www.nibe.eu/sv-se/partner/molndals-varme-ab--molndal-43139-installator
https://www.nibe.eu/sv-se/partner/morgonstjarnan-ror-ab--sunne-68694-installator
https://www.nibe.eu/sv-se/partner/morkoms-vvs-ab--sveg-84231-installator
https://www.nibe.eu/sv-se/partner/mossboda-vvs-ab--haby-44495-installator
https://www.nibe.eu/sv-se/partner/motala-kylen-ab--motala-59194-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-aborred-ror--ab--munkedal-45582-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-aborred-ror--ab--munkedal-45582-service
https://www.nibe.eu/sv-se/partner/nibe-partner-bjork--lind-ror-ab--tanumshede-45730-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-bjork--lind-ror-ab--tanumshede-45730-service
https://www.nibe.eu/sv-se/partner/nibe-partner-fruktan-ab--orust-47390-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-fruktan-ab--orust-47390-service
https://www.nibe.eu/sv-se/partner/nibe-partner-granens-ror-ab--ornskoldsvik-89131-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-granens-ror-ab--ornskoldsvik-89131-service
https://www.nibe.eu/sv-se/partner/nibe-partner-installation-i-brottby-ab--brottby-18494-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-john-eklund-borrning-ab--ornskoldsvik-89150-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-john-eklund-borrning-ab--ornskoldsvik-89150-service
https://www.nibe.eu/sv-se/partner/nibe-partner-kungsholmen-vvs-ab--stockholm-10452-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-lindgrens-ror-ab--kramfors-87231-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-lindgrens-ror-ab--kramfors-87231-service
https://www.nibe.eu/sv-se/partner/nibe-partner-malaxhuse-ror-ab--lysekil-45355-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-malaxhuse-ror-ab--lysekil-45355-service
https://www.nibe.eu/sv-se/partner/nibe-partner-masab-ror-ab--alingsas-44152-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-masab-ror-ab--alingsas-44152-service
https://www.nibe.eu/sv-se/partner/nibe-partner-nordkust-ror-och-vvs-ab--sundsvall-85471-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-nordkust-ror-och-vvs-ab--sundsvall-85471-service
https://www.nibe.eu/sv-se/partner/nibe-partner-rorstrom-i-karlstad-ab--karlstad-65351-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-rorstrom-i-karlstad-ab--karlstad-65351-service
https://www.nibe.eu/sv-se/partner/nibe-partner-sandsvikens-ror-ab--sandviken-81132-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-sandsvikens-ror-ab--sandviken-81132-service
https://www.nibe.eu/sv-se/partner/nibe-partner-vasternorrlands-bergvarmepumpar-ab--harnosand-87130-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-vasternorrlands-bergvarmepumpar-ab--harnosand-87130-service
https://www.nibe.eu/sv-se/partner/nibe-partner-vattenfall-heat-pump-service-ab--borlange-78153-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-vattenfall-heat-pump-service-ab--borlange-78153-service
https://www.nibe.eu/sv-se/partner/nibe-partner-vattenfall-heat-pump-service-ab--falun-79132-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-vattenfall-heat-pump-service-ab--falun-79132-service
https://www.nibe.eu/sv-se/partner/nibe-partner-vattenfall-heat-pump-service-ab--hagfors-68333-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-vattenfall-heat-pump-service-ab--karlstad-65340-installator
https://www.nibe.eu/sv-se/partner/nibe-partner-vattenfall-heat-pump-service-ab--vasteras-72232-installator
https://www.nibe.eu/sv-se/partner/nordbergs-ror-ab--falkenberg-31197-installator
https://www.nibe.eu/sv-se/partner/nordens-bergvarmepumpar-ab--halmstad-30264-installator
https://www.nibe.eu/sv-se/partner/nordens-bergvarmepumpar-ab--halmstad-30264-service
https://www.nibe.eu/sv-se/partner/nordisk-kyl--service-ab--gothenburg-41258-service
https://www.nibe.eu/sv-se/partner/nordisk-kyl--service-ab--gothenburg-41258-installator
https://www.nibe.eu/sv-se/partner/nordmalings-rorservice-ab--nordmaling-91491-installator
https://www.nibe.eu/sv-se/partner/nordvik-vvs-ab--harnosand-87143-installator
https://www.nibe.eu/sv-se/partner/norra-dalarnas-ror-ab--orsa-79431-installator
https://www.nibe.eu/sv-se/partner/norr-energi-ab--umea-90344-installator
https://www.nibe.eu/sv-se/partner/norr-energi-ab--umea-90344-service
https://www.nibe.eu/sv-se/partner/norrkopings-kylen-ab--norrkoping-60221-installator
https://www.nibe.eu/sv-se/partner/norskogs-ror-ab--karlstad-65225-installator
https://www.nibe.eu/sv-se/partner/nossebro-el--vvs-ab--nossebro-46590-installator
https://www.nibe.eu/sv-se/partner/ny-rorservice-ab--ekeby-24232-installator
https://www.nibe.eu/sv-se/partner/nybro-vvs-ab--nybro-38231-installator
https://www.nibe.eu/sv-se/partner/o-lindqvists-ror-ab--hassleholm-28133-installator
https://www.nibe.eu/sv-se/partner/ola-westman-ror--goteborg-41272-installator
https://www.nibe.eu/sv-se/partner/orsa-ror-ab--orsa-79431-installator
https://www.nibe.eu/sv-se/partner/osby-rorservice-ab--osby-28322-installator
https://www.nibe.eu/sv-se/partner/osterlens-rorinstallationer-ab--simrishamn-27233-installator
https://www.nibe.eu/sv-se/partner/osterlens-rorinstallationer-ab--simrishamn-27233-service
https://www.nibe.eu/sv-se/partner/pagelmans-ror-ab--stenungsund-44446-installator
https://www.nibe.eu/sv-se/partner/pagelmans-ror-ab--gothenburg-41258-installator
https://www.nibe.eu/sv-se/partner/pelle-petter-ab--huskvarna-56173-installator
https://www.nibe.eu/sv-se/partner/per-johanssons-vvs--eslov-24131-installator
https://www.nibe.eu/sv-se/partner/per-ols-ror--kyla-ab--nacka-13137-installator
https://www.nibe.eu/sv-se/partner/per-persons-vvs--rottne-36394-installator
https://www.nibe.eu/sv-se/partner/perssons-ror-ab--lessebo-36531-installator
https://www.nibe.eu/sv-se/partner/piteors-vvs-ab--pitea-94138-installator
https://www.nibe.eu/sv-se/partner/pitea-ror-ab--pitea-94133-installator
https://www.nibe.eu/sv-se/partner/plc-miljo-ab--norrkoping-60224-installator
https://www.nibe.eu/sv-se/partner/pmab-ror-ab--gothenburg-41104-installator
https://www.nibe.eu/sv-se/partner/polhems-ror-ab--horby-24237-installator
https://www.nibe.eu/sv-se/partner/precis-energi-ab--linkoping-58330-installator
https://www.nibe.eu/sv-se/partner/prima-rorinstallationer-i-visby-ab--visby-62157-installator
https://www.nibe.eu/sv-se/partner/pro-ror--varme-ab--herrljunga-52492-installator
https://www.nibe.eu/sv-se/partner/pro-ror--varme-ab--lidkoping-53167-installator
https://www.nibe.eu/sv-se/partner/pronordic-ab--sollentuna-19154-installator
https://www.nibe.eu/sv-se/partner/provag-energi-ab--vasteras-72249-installator
https://www.nibe.eu/sv-se/partner/pumpterminalen-i-jonkoping-ab--jonkoping-55311-installator
https://www.nibe.eu/sv-se/partner/r-h-vvs-ab--malmo-21137-installator
https://www.nibe.eu/sv-se/partner/rafael-fernandez-rorinstallationer-ab--uppsala-75432-installator
https://www.nibe.eu/sv-se/partner/ragnar-graffman-vvs-ab--vasteras-72241-installator
https://www.nibe.eu/sv-se/partner/rakt-ror-ab--motala-59132-installator
https://www.nibe.eu/sv-se/partner/rakt-ror-ab--mjolby-59537-installator
https://www.nibe.eu/sv-se/partner/rattviks-ror-ab--rattvik-79595-installator
https://www.nibe.eu/sv-se/partner/rbd-ror-ab--nacka-13175-installator
https://www.nibe.eu/sv-se/partner/rein-ror-ab--haparanda-95332-installator
https://www.nibe.eu/sv-se/partner/rein-ror-ab--haparanda-95332-service
https://www.nibe.eu/sv-se/partner/restaurang-ror-ab--gothenburg-40023-installator
https://www.nibe.eu/sv-se/partner/ro-installationer-ab--gothenburg-41502-installator
https://www.nibe.eu/sv-se/partner/robertsfors-ror-ab--robertsfors-91570-installator
https://www.nibe.eu/sv-se/partner/rokestads-ror--kyla-ab--eslov-24131-installator
https://www.nibe.eu/sv-se/partner/ronnebyortens-el--vvs-ab--ronneby-37232-installator
https://www.nibe.eu/sv-se/partner/rorbolaget-i-malmo-ab--malmo-21137-installator
https://www.nibe.eu/sv-se/partner/ror-gruppen-gotland-ab--visby-62151-installator
https://www.nibe.eu/sv-se/partner/ror-halland-ab--kungsbacka-43432-installator
https://www.nibe.eu/sv-se/partner/ror-service-dala-ab--sala-73343-installator
https://www.nibe.eu/sv-se/partner/ror-tjansen-i-norrtelje-ab--norrtalje-76196-installator
https://www.nibe.eu/sv-se/partner/rors-rorstudio-ab--vimmerby-59840-installator
https://www.nibe.eu/sv-se/partner/rorsmorpan-ab--norrahammar-56163-installator
https://www.nibe.eu/sv-se/partner/rorstrom-ab--borlange-78153-installator
https://www.nibe.eu/sv-se/partner/rorstrom-ab--borlange-78153-service
https://www.nibe.eu/sv-se/partner/rortekniken-ab--halmstad-30255-installator
https://www.nibe.eu/sv-se/partner/sa-rorinstallation-ab--hoganas-26391-installator
https://www.nibe.eu/sv-se/partner/sala-rorservice-ab--sala-73342-installator
https://www.nibe.eu/sv-se/partner/sandvikens-ror-ab--sandviken-81135-installator
https://www.nibe.eu/sv-se/partner/serneke-installation-ab--gothenburg-41877-installator
https://www.nibe.eu/sv-se/partner/service-kyla-ab--linkoping-58273-installator
https://www.nibe.eu/sv-se/partner/service-kyla-ab--linkoping-58273-service
https://www.nibe.eu/sv-se/partner/simrishamns-ror-ab--simrishamn-27233-installator
https://www.nibe.eu/sv-se/partner/sjobergs-ror-ab--linkoping-58273-installator
https://www.nibe.eu/sv-se/partner/skelleftea-rorservice-ab--skelleftea-93140-installator
https://www.nibe.eu/sv-se/partner/skovde-rorservice-ab--skovde-54135-installator
https://www.nibe.eu/sv-se/partner/skovde-rorservice-ab--skovde-54135-service
https://www.nibe.eu/sv-se/partner/smalands-rorservice-ab--eksjo-57527-installator
https://www.nibe.eu/sv-se/partner/smalands-rorservice-ab--nassjo-57131-installator
https://www.nibe.eu/sv-se/partner/soback-rorinstallation-ab--svalov-26874-installator
https://www.nibe.eu/sv-se/partner/soback-rorinstallation-ab--svalov-26874-service
https://www.nibe.eu/sv-se/partner/son-o-faders-bygg--ror-ab--jokkmokk-96232-installator
""".strip()

# Parse all URLs
rows = []
seen_companies = {}  # company_name -> first row (dedup by company+city)

for url in ALL_URLS.split("\n"):
    url = url.strip()
    if not url or "/sv-se/partner/" not in url:
        continue

    parsed = parse_url(url)
    if not parsed:
        continue

    company = parsed["company_name"]
    city = parsed["city"]
    ptype = parsed["partner_type"]

    # Skip excluded companies
    if should_exclude(company):
        continue

    # Determine elzon: try city first, fallback to postal
    postal_clean = parsed["postal_code"].replace(" ", "")
    elzon = city_to_elzon(city)
    if elzon == "SE3":  # double-check with postal
        postal_elzon = postal_to_elzon(postal_clean)
        if postal_elzon and postal_elzon != "SE3":
            elzon = postal_elzon

    total_score, tier = score({**parsed, "elzon": elzon})

    row = {
        "company_name": company,
        "city": city,
        "postal_code": parsed["postal_code"],
        "elzon": elzon,
        "partner_type": ptype,
        "cert_level": "Installatör" if ptype == "installator" else "Service",
        "score": total_score,
        "tier": tier,
        "phone": "",
        "email": "",
        "website": "",
        "source_url": url,
    }
    rows.append(row)

print(f"Total parsed rows: {len(rows)}")

# Sort: tier A first, then B, then by score desc
tier_order = {"A": 0, "B": 1, "C": 2}
rows.sort(key=lambda r: (tier_order[r["tier"]], -r["score"], r["company_name"]))

# Write leads_raw.csv
fieldnames = ["company_name","city","postal_code","elzon","partner_type","cert_level","score","tier","phone","email","website","source_url"]
with open("/Users/henrikharplinger/dev/effira/crm/nibe/leads_raw.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)
print(f"Wrote leads_raw.csv ({len(rows)} rows)")

# Write outreach_leads.csv (Tier A + B only)
outreach = [r for r in rows if r["tier"] in ("A", "B")]
with open("/Users/henrikharplinger/dev/effira/crm/nibe/outreach_leads.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(outreach)
print(f"Wrote outreach_leads.csv ({len(outreach)} rows)")

# Stats
tier_a = [r for r in rows if r["tier"] == "A"]
tier_b = [r for r in rows if r["tier"] == "B"]
tier_c = [r for r in rows if r["tier"] == "C"]
elzon_counts = {}
for r in rows:
    elzon_counts[r["elzon"]] = elzon_counts.get(r["elzon"], 0) + 1

print(f"\nTier A: {len(tier_a)}, Tier B: {len(tier_b)}, Tier C: {len(tier_c)}")
print(f"Elzon distribution: {elzon_counts}")
print("\nTop 10 Tier A:")
for r in tier_a[:10]:
    print(f"  {r['company_name']} | {r['city']} | {r['elzon']} | {r['score']}p | {r['cert_level']}")
