// **********************************************************************
let corpus = [
  "Mmmh I love pizzas.",
  "I absolutely hate onions.",
  "Mmmh I love pizzas, but I absolutely hate onions."
]

// **********************************************************************
const sentiment = require("sentiment");
sent = new sentiment();
let result = sent.analyze("any text that you want to compute a sentiment score for")

// **********************************************************************
const getSentiment = (data) => {
  let result = sent.analyze(data);
  for (let r in result) {
    console.log(r, result[r])
  }
}

// **********************************************************************
let struct = {
  sentence: [],
  score: [],
  comparative: [],
  positive: [],
  negative: []
}

// **********************************************************************
const parseSentiment = (data) => {
  let result = sent.analyze(data);
  for (let r in result) {
    if (r === "tokens") {
      struct["sentence"].push(result[r].join(" "))
    }
    if (r === "score") {
      struct["score"].push(result[r])
    }
    else if (r === "comparative") {
      struct["comparative"].push(result[r])
    }
    else if (r === "positive") {
      if (result[r].length === 0) {
        struct["positive"].push("N/A")
      }
      else {
        struct["positive"].push(result[r].join())
      }
    }
    else if (r === "negative") {
      if (result[r].length === 0) {
        struct["negative"].push("N/A")
      }
      else {
        struct["negative"].push(result[r].join())
      }
    }
  }
}

// **********************************************************************
corpus.forEach(
  c => parseSentiment(c);
)

for (let s in struct) {
  console.log(s, struct[s]);
}

// **********************************************************************
const d3 = require("d3");

let sent_file = "https://raw.githubusercontent.com/julien-blanchard/dbs/main/sentiment.csv";

const fetchData = (data) => {
        d3.csv(data).then(csv_file => {
        for (let c in csv_file) {
            if (csv_file[c]["Sentence"]) {
                console.log(csv_file[c]["Sentence"]);
             }
        }
     })
    }

fetchData(sent_file)

// **********************************************************************
const fetchData = (data) => {
        return d3.csv(data).then(csv_file => {
        let fetched = [];
        for (let c in csv_file) {
            if (csv_file[c]["Sentence"]) {
                fetched.push(csv_file[c]["Sentence"]);
             }
        }
        return fetched;
     })
  }

const parseData = async (data) => {
     let parsed = await fetchData(data);
         for (let p of parsed) {
             console.log(p);
     }
 }

// **********************************************************************
const sentiment = require("sentiment");
const d3 = require("d3");

// initializing the sentiment package
sent = new sentiment();

// data structures
let csv_file = "https://raw.githubusercontent.com/julien-blanchard/dbs/main/sentiment.csv";

// functions
const fetchData = (data) => {
        return d3.csv(data).then(csv_file => {
        let fetched = [];
        let struct = {
          sentence: [],
          score: [],
          comparative: [],
          positive: [],
          negative: []
        }
        for (let c in csv_file) {
            if (csv_file[c]["Sentence"]) {
                fetched.push(csv_file[c]["Sentence"]);
             }
        }
        for (let f of fetched) {
          getSentiment(f,struct);
        }
        return struct;
     })
    }

const getSentiment = (data,data_structure) => {
  let result = sent.analyze(data);
  for (let r in result) {
    if (r === "tokens") {
      data_structure["sentence"].push(result[r].join(" "))
    }
    if (r === "score") {
      data_structure["score"].push(result[r])
    }
    else if (r === "comparative") {
      data_structure["comparative"].push(result[r])
    }
    else if (r === "positive") {
      if (result[r].length === 0) {
        data_structure["positive"].push("N/A")
      }
      else {
        data_structure["positive"].push(result[r].join())
      }
    }
    else if (r === "negative") {
      if (result[r].length === 0) {
        data_structure["negative"].push("N/A")
      }
      else {
        data_structure["negative"].push(result[r].join())
      }
    }
  }
}

const getParsedData = async (data) => {
  let parsed = await fetchData(data);
  for (let p in parsed) {
      console.log(p, parsed[p]);
  }
}

getParsedData(csv_file);

// **********************************************************************
const aq = require("arquero");

const getDataFrame = async (data) => {
  let parsed = await fetchData(data);
  aq.table(parsed)
    .select("sentence","score","comparative","positive","negative")
    .orderby(aq.desc("score"))
    .print()
}

getDataFrame(csv_file);