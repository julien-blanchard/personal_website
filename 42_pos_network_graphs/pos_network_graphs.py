def getContext(term: str,n_tokens: int) -> None:
    tokens: List[str] = [c.lower() for c in corpus.split(" ")]
    for idx, token in enumerate(tokens):
        if token == term.lower():
            context: List[str] = [tokens[i] for i in range(idx - n_tokens, idx + n_tokens)]
            output: str = f"Context for {term.upper()} (line {str(idx)}):\n\t{' | '.join(context)}"
            print(output)

getContext("fraud",3)

################################

with open("baskervilles.txt", "r") as text_file:
    corpus: str = text_file.read()

print(corpus[:90])

################################

import spacy
from typing import List, Dict

nlp = spacy.load("en_core_web_sm")

doc = nlp(corpus)

################################

def getContext(term: str,n_tokens: int) -> None:
    for idx, token in enumerate(doc):
        if token.text == term:
            contextual_verbs: List[str] = [t.text for t in doc[idx-n_tokens : idx+n_tokens] if t.pos_ == "VERB"]
            output: str = f"Context for {term.upper()} (line {str(idx)}):\n\t{' | '.join(contextual_verbs)}"
            print(output)

getContext("Holmes",5)

################################

def getContext(term: str,n_tokens: int) -> None:
    for idx, token in enumerate(doc):
        if token.text == term:
            contextual_verbs: List[str] = [t.lemma_ for t in doc[idx-n_tokens : idx+n_tokens] if t.pos_ == "VERB"]
            if len(contextual_verbs) != 0:
                output: str = f"Context for {term.upper()} (line {str(idx)}):\n\t{' | '.join(contextual_verbs)}"
                print(output)

getContext("Watson",10)

################################

characters: List[str] = [
    "Holmes",
    "Watson",
    "Hugo",
    "Charles",
    "Henry",
    "Mortimer",
    "Selden",
    "John",
    "Elisa",
    "Jack",
    "Beryl",
    "Frankland",
]

data: Dict[str, List[str]] = {
    "Characters": [],
    "Verbs": []
}

def getContext(term: str,n_tokens: int) -> None:
    for idx, token in enumerate(doc):
        if token.text in characters:
            contextual_verbs: List[str] = [t.lemma_ for t in doc[idx-n_tokens : idx+n_tokens] if t.pos_ == "VERB"]
            if len(contextual_verbs) != 0:
                for verb in contextual_verbs:
                    data["Characters"].append(token.text)
                    data["Verbs"].append(verb)

getContext("Watson",10)

################################

def prepareData(data):
    dframe: pd.DataFrame = (
        pd
        .DataFrame(data)
        .groupby(["Characters","Verbs"])[["Verbs"]]
        .count()
        .rename(columns={"Verbs":"Volume"})
        .reset_index(drop=False)
        .query("Volume >= 3")
        .sort_values(["Characters","Volume"], ascending=False)
    )
    return dframe

df: pd.DataFrame = prepareData(data_struct)
df.head(10)

################################

def getNetworkPlot(data,serie1,serie2,serie3,title):
    G = nx.from_pandas_edgelist(data, serie1, serie2, edge_attr=True)
    edgelist = nx.to_edgelist(G)

    colors = [i/len(G.nodes) for i in range(len(G.nodes))]

    plt.figure(figsize=(15,9))
    nx.draw(
        G,
        with_labels = True,
        node_size = [v * 200 for v in dict(G.degree()).values()],
        #width_size = [e[2][serie3] / 500 for e in edgelist],
        font_size = 12,
        node_color = colors,
        cmap = "Pastel1"
    )
    plt.title(title)
    plt.show()

getNetworkPlot(df,"Characters","Verbs","Volume","")

################################
