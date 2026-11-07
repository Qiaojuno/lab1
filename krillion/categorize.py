import re
# Ordered: first match wins
RULES = [
 ("Language & Words", r"\blanguage|alphabet|palindrome|wordle|\bword (for|that)|english word|nationality|street suffix|spell with|nursery rhyme|si\) prefix|first names"),
 ("Animals", r"animal|\bbirds?\b|penguin|owl|parrot|waterfowl|beetle|lizard|turtle|tortoise|crab|crustacean|mollusk|shellfish"),
 ("Geography", r"gulf|bay\\b|soviet|countr|\bcit(y|ies)\b|capital|\bstates?\b|province|continent|island|river|mountain|ocean|\bsea\b|lake|desert|region|territor|border|landmark|national park|volcano|\bflag"),
 ("Animals", r"animal|\bbirds?\b|\bfish|mammal|insect|reptile|\bdogs?\b|\bcats?\b|pokémon|pokemon|creature|\bbugs?\b|spider|snake|shark|whale|horse|breed|amphibian|primate|rodent|marsupial|predator|\bpets?\b|zoo|sea animal|livestock|dinosaur"),
 ("Food & Drink", r"chili|\\bpie\\b|dumpling|salad|pastry|doughnut|cut of beef|berry|\\bdip\\b|curry|legume|\\bdiet\\b|sausage|\bfoods?\b|fruit|vegetable|drink|\bdish|cheese|sauce|pasta|bread|dessert|cocktail|candy|chocolate|snack|ingredient|spice|herb|\bmeal|cereal|beer|wine|coffee|\btea\b|soup|cake|cookie|pizza|sandwich|restaurant|fast[- ]food|menu|cuisine|\bnuts?\b|\bmilk|juice|soda|breakfast|cook|bake|recipe|\beat\b|edible|potato|egg|meat|seafood|condiment|flavou?r"),
 ("Movies & TV", r"superhero team|^$"),
 ("Sports & Games", r"yoga|gym|exercise|minecraft|playstation|sport|\bnba\b|\bnfl\b|\bmlb\b|nhl|soccer|football|basketball|baseball|tennis|golf|olympic|athlete|\bteam|league|ballon|premier league|cricket|rugby|hockey|boxing|wrestl|chess|board game|card game|video game|\bgames?\b|\bplayer|mvp|f1|formula|stadium|\bball\b|martial art"),
 ("Music", r"girl group|music|\bsong|album|singer|\bband|rapper|spotify|billboard|musical instrument|orchestra|genre of music|musician|concert|festival|grammy|k-pop|\bbeatles|taylor swift|bieber|lyric"),
 ("Movies & TV", r"saturday night live|avengers|hollywood|director|short-form video|movie|film|\btv\b|show|series|pixar|disney|marvel|\bdc\b|netflix|actor|actress|oscar|imdb|anime|cartoon|sitcom|character|superhero|villain|star wars|harry potter|simpsons|attack on titan|one piece|naruto|batman|superman|spider-man|lord of the rings|game of thrones|friends|episode"),
 ("People & Celebrities", r"\bfamous (?!museum)|emperor|astronaut|cosmonaut|ceo\\b|\bsomeone\b|celebrit|president|prime minister|\bking\b|queen|royal|youtuber|streamer|influencer|instagram followers|tiktok|billionaire|scientist|artist\b|author|writer|painter|philosopher|comedian|inventor|leader|politician|historical figure|person|people named|named after"),
 ("Science & Nature", r"constellation|ology|geologic|subatomic|hormone|engineering|environmental|phobia|element|metal|chemical|planet|astronom|space|star\b|galax|\bgas\b|mineral|rock|gem|crystal|tree|flower|plant|weather|cloud|physics|chemistry|biology|scientific|\bunit\b|measure|naturally|nature|mined|disease|virus|bacteri|organ\b|\bbones?\b|vitamin|blood|body produces|cell|energy|shape|math|number|geometr|\b2d\b|\b3d\b|percentage|colou?r|blue|\bred\b|green"),
 ("Human Body & Health", r"body|\bhead\b|face|\bhair\b|skin|medical|medicine|doctor|health|injur|symptom|emotion|feel|muscle|tooth|teeth|eye|hand|foot|feet|scan|surgery|drug"),
 ("Brands & Business", r"brand|compan|chain|store|retailer|\bapp\b|apps|website|amazon|apple|google|microsoft|car brand|logo|\bbank|airline|social media|startup|product|instagram|dating|service|currency|stock|\bjob|career|profession|occupation|\bpay\b|salary"),
 ("Technology", r"browser|font|search engine|email|tech|computer|software|phone|iphone|internet|keyboard|device|electronic|robot|\bai\b|programming|code|gadget|setting|feature"),
 ("History & Culture", r"armor|weapon|\\bgun\\b|military|sacred text|prayer|logical fallacy|university|news organi|histor|ancient|war\b|empire|religio|god|goddess|myth|holiday|tradition|festival|halloween|christmas|wedding|symbol|culture|century|dynasty|revolution|legend"),
 ("Arts & Literature", r"shakespeare|fairy tale|literary|\bbook|novel|poem|poet|painting|sculpture|museum|\bart\b|literature|fiction|comic|manga|dance|theat|opera"),
 ("Transport & Vehicles", r"vehicle|\bcar\b|cars\b|train|plane|aircraft|boat|ship|bike|bicycle|motor|wheel|driving|traffic|road|airport|transport"),
 ("Clothing & Fashion", r"fabric|textile|jeans|pattern or print|\\bbag\\b|cloth|wear|shirt|shoe|hat|dress|fashion|jewel|accessor|underwear|perfume|fragrance|makeup|cosmetic|beauty|salon|deodorant"),
 ("Arts & Literature", r"museum|^$"),
 ("Technology", r"notes|documents|^$"),
 ("Home & Everyday Objects", r"knot|tape|\\bwood\\b|door|building material|powder|\\bcard\\b|balloon|structure|furniture|kitchen|household|home|house|room|tool|\bbed\b|table|chair|bathroom|garden|clean|appliance|container|bottle|tube|\broll\b|sold|stick|brush|filter|blade|paper|pages|office|school|toy|\bitem|object|something|thing"),
]
COMPILED = [(c, re.compile(p, re.I)) for c, p in RULES]
def categorize(text):
    for c, rx in COMPILED:
        if rx.search(text): return c
    return "General Knowledge"
