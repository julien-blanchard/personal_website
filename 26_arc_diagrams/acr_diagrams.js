// **********************************************************************

let text = "Hi I'm Julien and I love pizzas, and I also love burgers. I'm also a lot into programming.";

const getTerms = (data) => {
  let result = new Array();
  let d = data.split(" ");
  for (let i = 0; i < d.length; i++) {
    result.push(`${d[i]} | ${d[i+1]}`);
  }
  return result;
}

const countOccurrences = (data) => {
  let result = new Object();
  for (let d of data) {
    if (result[d]) {
      result[d] += 1;
    }
    else {
      result[d] = 1;
    }
  }
  console.log(result);
}

let terms = getTerms(text)
countOccurrences(terms)

// **********************************************************************

let text = "Hi I'm Julien and I love pizzas, and I also love burgers. I'm also a lot into programming.";

const getCleanedTerms = (data) => {
  let punctuation = '!"#$%&\()*+,./:;<=>?@[\\]^_`{|}~';
  let regex = new RegExp("[" + punctuation + "]", "g");
  let result = data
    .split(" ")
    .map(
      d => d
      .replace(regex, "")
      .toLowerCase()
     );
  return result.join(" ");
}

let cleaned = cleanTerms(text);
console.log(`Original sentence:\n\t${text}\n\nCleaned sentence:\n\t${cleaned}`)

// **********************************************************************

const winkNLP = require("wink-nlp");
const model = require("wink-eng-lite-web-model");
const nlp = winkNLP(model);
const its = nlp.its;
const as = nlp.as;

// **********************************************************************

const getTags = (data) => {
  const doc = nlp.readDoc(data);
  const result = doc.tokens().out(its.pos);
  return result;
}

let cleaned = cleanTerms(text);
let tags = getTags(cleaned);
console.log(tags)

// **********************************************************************

let cleaned = cleanTerms(text);
let tags = getTags(cleaned);
let occurrences = getTerms(tags.join(" "));
let c = countOccurrences(occurrences)
console.log(c)

// **********************************************************************

const countOccurrences = (data) => {
    let temp = new Object();
    let result = new Array();
    for (let d of data) {
        if (temp[d]) {
            temp[d] += 1;
        }
        else {
            temp[d] = 1;
        } 
    }
    for (let t in temp) {
        result.push( [t.split(" ")[0], t.split(" ")[1],temp[t]] );
    }
    return result;
}

// **********************************************************************

<head>

    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/sankey.js"></script>
    <script src="https://code.highcharts.com/modules/arc-diagram.js"></script>
    <script src="https://code.highcharts.com/modules/accessibility.js"></script>

</head>
<body>

    <div id="viz" style="height: 400px; max-width: 800px; margin: 0 auto;"></div>
    
    <script type="module">

        import winkNlp from "https://cdn.skypack.dev/wink-nlp";
        import winkEngLiteWebModel from "https://cdn.skypack.dev/wink-eng-lite-web-model";

    </script>

</body>

// **********************************************************************

const getChart = (data,chart_title) => {
    Highcharts.chart(
        "viz",
        {
            colors: ["#003f5c","#58508d","#58508d","#ff6361","#ffa600"],
            title: {
                text: chart_title
             },
             series: [{
                 keys: ["from", "to", "weight"],
                 type: "arcdiagram",
                 name: "Ngrams",
                 linkWeight: 1,
                 centeredLinks: true,
                 dataLabels: {
                     rotation: 90,
                     y: 80,
                     align: "left",
                     color: "black"
                 },
                 offset: "65%",
                 data: data
             }]
         }
     )
}

let sentence = "Hi I'm Julien and I love pizzas, and I also love burgers. I'm also a lot into programming.";
let cleaned = getCleanedTerms(sentence);
let tokens = getTags(cleaned);
let occurrence = getCoOccurrence(tokens,1);
let c = getCount(occurrence);
getChart(c,"Semantic proximity between terms");

// **********************************************************************

let cleaned = getCleanedTerms(sentence); let occurrence = getCoOccurrence(cleaned.split(" "),1);
let c = getCount(occurrence);
getChart(c,"Semantic proximity between terms");

// **********************************************************************

let text = "Hi I'm Julien and I love pizzas, and I also love burgers. I'm also a lot into programming.";

const getTags = (data) => {
  let result = new Array();
  const doc = nlp.readDoc(data);
  const tokens = doc.tokens().out()
  const tags = doc.tokens().out(its.pos);
  if (tokens.length === tags.length) {
    for (let i = 0; i < tokens.length; i++) {
      result.push([tokens[i],tags[i]]);
    }
  }
  else {
    return "Mismatched length"
  }
  return result;
}

const terms = cleanTerms(text);
console.log(getTags(terms))

// **********************************************************************

const getPlot = (data, chart_title) => {
  Highcharts.chart("viz", {
    chart: {
      type: "networkgraph",
      height: "100%",
    },
    title: {
      text: chart_title,
      align: "left",
    },
    plotOptions: {
      networkgraph: {
        keys: ["from", "to"],
        layoutAlgorithm: {
          enableSimulation: false,
        },
      },
    },
    series: [
      {
        accessibility: {
          enabled: false,
        },
        dataLabels: {
          enabled: true,
          linkFormat: "",
        },
        id: "lang-tree",
        data: data,
      },
    ],
  });
};


getPlot(network,"Network graph for H.P. Lovecraft");

// **********************************************************************

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/sankey.js"></script>
    <script src="https://code.highcharts.com/modules/arc-diagram.js"></script>
    <script src="https://code.highcharts.com/modules/accessibility.js"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>

    <div id="viz" style="height: 700px; max-width: 800px; margin: 0 auto;"></div>
    
    <script type="module">

        import winkNlp from 'https://cdn.skypack.dev/wink-nlp';
        import winkEngLiteWebModel from 'https://cdn.skypack.dev/wink-eng-lite-web-model';

        const getTags = (data) => {
            const nlp = winkNlp(winkEngLiteWebModel);
            let its = nlp.its;
            let as = nlp.as;
            const doc = nlp.readDoc(data);
            const result = doc.tokens().out(its.pos);
            return result;
        }

        const getCleanedTerms = (data) => {
            let punctuation = '!"#$%&\()*+,./:;<=>?@[\\]^_`{|}~';
            let regex = new RegExp("[" + punctuation + "]", "g");
            let result = data.split(" ").map(
                d => d
                .replace(regex, "")
                .toLowerCase()
                    );
            return result.join(" ");
        }

        const getCoOccurrence = (data,howmany) => {
            let result = new Array();
            for (let i = 0; i < data.length; i++) {
                if (typeof data[i + howmany] === "string") {
                result.push(`${data[i]} ${data[i+howmany]}`);
                }
            }
            return result;
        }

        const getCount = (data) => {
            let temp = new Object();
            let result = new Array();
            for (let d of data) {
                if (temp[d]) {
                temp[d] += 1;
                }
                else {
                temp[d] = 1;
                } 
            }
            for (let t in temp) {
                result.push( [t.split(" ")[0], t.split(" ")[1],temp[t]] );
            }
            return result;
        }

        const getChart = (data,chart_title) => {
            Highcharts.chart(
                "viz",
                {
                    //colors: ["#003f5c","#58508d","#58508d","#ff6361","#ffa600"],
                    //colors: ["#cdb4db","#ffc8dd","#ffafcc","#bde0fe","#a2d2ff"],
                    colors: ["#3A98B9","#FFF1DC","#E8D5C4","#EEEEEE"],
                    title: {
                        text: chart_title
                    },
                    series: [{
                    keys: ["from", "to", "weight"],
                    type: "arcdiagram",
                    name: "Ngrams",
                    linkWeight: 1,
                    centeredLinks: true,
                    dataLabels: {
                        rotation: 90,
                        y: 110,
                        align: 'left',
                        color: 'black'
                        },
                    offset: '65%',
                    data: data
                }]
                }
            )
        }

        let sentence = "Hi I'm Julien and I love pizzas, and I also love burgers. I'm also a lot into programming.";
        let cleaned = getCleanedTerms(text);
        let tokens = getTags(cleaned);
        let occurrence = getCoOccurrence(tokens,1);
        let c = getCount(occurrence);
        getChart(c,"Semantic proximity between POS tags");
    </script>
</body>
</html>

// **********************************************************************
// **********************************************************************
// **********************************************************************
// **********************************************************************