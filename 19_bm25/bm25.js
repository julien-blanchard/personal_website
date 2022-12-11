const winkNLP = require("wink-nlp");
const model = require("wink-eng-lite-web-model");
const its = require("wink-nlp/src/its.js");
const as = require("wink-nlp/src/as.js");

// **********************************************************************

let text = "Oh hello!";
const nlp = winkNLP(model);
const doc = nlp.readDoc(text);
console.log(doc.tokens().out());

// **********************************************************************

const getNLP = (data) => {
  const text = data;
  const nlp = winkNLP(model);
  const doc = nlp.readDoc(text);
  let keywords = doc.tokens().out();
  let result = {
    "Token": [],
    "Tag": [],
    "Lemma": [],
    "Stopword": []
  };
  for (let i = 0; i < keywords.length; i++) {
    result["Token"].push(doc.tokens().out(its.value)[i]);
    result["Tag"].push(doc.tokens().out(its.pos)[i]);
    result["Lemma"].push(doc.tokens().out(its.lemma)[i]);
    result["Stopword"].push(doc.tokens().out(its.stopWordFlag)[i]);
  }
  return result;
};

const getResults = (data) => {
  let processed_text = getNLP(data);
  for (let p in processed_text) {
    console.log(p + "\n\t", processed_text[p].join(" / "));
  }
}

let text_to_process = "Hey, this article is about using JavaScript to extract meaningful information from textual data.";
getResults(text_to_process);

// **********************************************************************

let text = "Julien's website has seen a 60% week on week increase between August and October, but he's not making any $ with it."

const getFreq = (data) => {
  const nlp = winkNLP(model);
  let doc = nlp.readDoc(data);
  doc.tokens()
    .out(its.type, as.freqTable)
	.forEach(e => {console.log(`Type: ${e[0]} => ${e[1]}`)})
}

getFreq(text);

// **********************************************************************

const corpus = [
    "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically-typed and garbage-collected. It supports multiple programming paradigms, including structured, object-oriented and functional programming.",
    "JavaScript, often abbreviated as JS, is a programming language that is one of the core technologies of the World Wide Web, alongside HTML and CSS. As of 2022, 98% of websites use JavaScript on the client side for webpage behavior, often incorporating third-party libraries.",
    "Ruby is an interpreted, high-level, general-purpose programming language which supports multiple programming paradigms. It was designed with an emphasis on programming productivity and simplicity. In Ruby, everything is an object, including primitive data types."
];

// **********************************************************************

const BM25Vectorizer = require('wink-nlp/utilities/bm25-vectorizer');
const bm25 = BM25Vectorizer();

corpus.forEach( (doc) =>  bm25.learn(
        nlp.readDoc(doc)
        .tokens()
        .out(its.normal)
        )
    );

// **********************************************************************

const getUniqueTerms = () => {
    let terms = bm25.out(its.terms);
    for (let term in terms) {
        console.log(term, terms[term])
    }
    console.log(bm25.out(its.terms));
}

// **********************************************************************

const getBowPerDoc = (which) => {
    let terms = bm25.doc(which).out(its.bow)
    for (let term in terms) {
        console.log(term, " => ", terms[term])
    }
}

// **********************************************************************

const getBow = () => {
    let terms = bm25.out(its.docBOWArray)
    for (term in terms) {
        for (t in terms[term]) {
            console.log(`${t}  =>  ${terms[term][t]}`)
        }
    }
}

// **********************************************************************

const getIdfPerTerm = () => {
    let terms = bm25.out(its.idf);
    for (term in terms) {
        console.log(`${terms[term][0]} =>  ${terms[term][1]}`)
    }
}