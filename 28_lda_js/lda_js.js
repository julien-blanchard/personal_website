// **********************************************************************

const docs = [
  "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a 'batteries included' language due to its comprehensive standard library. Python was conceived in the late 1980s by Guido van Rossum at Centrum Wiskunde & Informatica (CWI) in the Netherlands as a successor to the ABC programming language, which was inspired by SETL, capable of exception handling and interfacing with the Amoeba operating system.",
  "JavaScript, often abbreviated as JS, is a programming language that is one of the core technologies of the World Wide Web, alongside HTML and CSS. As of 2022, 98% of websites use JavaScript on the client side for webpage behavior, often incorporating third-party libraries. All major web browsers have a dedicated JavaScript engine to execute the code on users' devices. JavaScript is a high-level, often just-in-time compiled language that conforms to the ECMAScript standard. It has dynamic typing, prototype-based object-orientation, and first-class functions. It is multi-paradigm, supporting event-driven, functional, and imperative programming styles. It has application programming interfaces (APIs) for working with text, dates, regular expressions, standard data structures, and the Document Object Model (DOM)",
  "Go is a statically typed, compiled high-level programming language designed at Google by Robert Griesemer, Rob Pike, and Ken Thompson. It is syntactically similar to C, but with memory safety, garbage collection, structural typing, and CSP-style concurrency. It is often referred to as Golang because of its former domain name, golang.org, but its proper name is Go. Go was designed at Google in 2007 to improve programming productivity in an era of multicore, networked machines and large codebases. The designers wanted to address criticism of other languages in use at Google, but keep their useful characteristics: Static typing and run-time efficiency, Readability and usability, High-performance networking and multiprocessing.",
];

import {lda} from "https://cdn.jsdelivr.net/gh/stdlib-js/nlp@esm/index.mjs"

let model = lda(
    docs,
    3
);

model.fit(
    5000,
    100,
    10 
);

// **********************************************************************

const getTerms = (topic,words) => {
  let terms = model.getTerms(topic,words);
  for (let t in terms) {
    console.log(terms[t])
  }
}

getTerms(0,3);

// **********************************************************************

import stopword from "https://cdn.jsdelivr.net/npm/stopword@2.0.6/+esm"

const getCleanedText = (data) => {
  let result = new Array();
  let punctuation = "!\"#$%&'()*+,./:;<=>?@[\\]^_`{|}~";
  let regex = new RegExp("[" + punctuation + "]", "g");
  for (let d of data) {
    result.push(
      stopword
        .removeStopwords(d.split(" "))
        .join(" ")
        .replace(/(\b(\w{1,3})\b(\s|$))/g, "")
        .replace(regex, "")
        .toLowerCase()
    );
  }
  return result;
};

const docs_cleaned = getCleanedText(docs);

// **********************************************************************

const getTerms = (topic,words) => {
	for (let i of Array(topic).keys()) {
    	let terms = model.getTerms(i,words);
      	for (let t in terms) {
          let scores = Object.values(terms[t]);
          console.log(`Topic ${i+1} => Term: ${scores[0]} => Score: ${scores[1]}`);
        }
    }
}

getTerms(3,5);

// **********************************************************************

const getTerms = (n_topics, n_terms) => {
  let struct = new Array();
  for (let i of Array(n_topics).keys()) {
    let children = new Array();
    const terms = model.getTerms(i, n_terms);
    const term = Object.values(terms);
    term.forEach((t) => {
      children.push({ name: t["word"], value: t["prob"] });
    });
    struct.push({ name: `Topic ${i + 1}`, children: children });
  }
  const result = [{ name: " ", children: struct }];
  return result;
};

let t = getTerms(3,5);
console.log(t);

// **********************************************************************

<head>
    <script src="https://cdn.anychart.com/releases/8.11.0/js/anychart-core.min.js"></script>
     <script src="https://cdn.anychart.com/releases/8.11.0/js/anychart-circle-packing.min.js"></script>
     <link rel="stylesheet" href="lda_viz.css">
</head>

<div class="container">
    <div id="viz"></div>
</div>

// **********************************************************************

.container {
    display: flex;
  }
#viz {
    margin: 0px;
    width: 1100px;
    height: 600px;
  }

// **********************************************************************

const getChart = (chart_title) => {
    const data = getTerms(3,5);
    let chart = anychart.circlePacking(data, "as-tree");
    chart.container("viz");
    chart.draw();
    let title = chart.title();
    title.text(chart_title);
    title.enabled(true);
    title.fontSize(35);
}

getChart("LDA visualisation");

// **********************************************************************

const getTerms = (n_topics, n_terms) => {
  let struct = new Array();
  for (let i of Array(n_topics).keys()) {
    let children = new Array();
    const terms = model.getTerms(i, n_terms);
    const term = Object.values(terms);
    for (let t in terms) {
      struct.push({
        from: `Topic ${i + 1}`,
        to: terms[t]["word"],
        weight: terms[t]["prob"],
      });
    }
  }
  return struct;
};

let t = getTerms(3,5);
console.log(t);

// **********************************************************************

const getChart = (chart_title) => {
  const data = getTerms(3, 5);
  let chart = anychart.sankey(data);
  chart.nodeWidth("30%");
  chart.container("viz");
  chart.draw();
  let title = chart.title();
  title.text(chart_title);
  title.enabled(true);
  title.fontSize(35);
};

getChart("LDA visualization");
