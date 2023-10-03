// **********************************************************************

import {csvParse, csvParseRows} from "https://cdn.skypack.dev/d3-dsv@3";

const fetchData = async (csv_file) => {
  return fetch(csv_file).then(
    d => {return d.text()}
  )
};

const getData = (data) => {
  const temp = csvParse(data);
  let struct = {
    first_name: [],
    last_name: [],
    age: [],
    country: [],
    occupation: []
  }; 
  for (let t in temp) {
		struct["first_name"].push(Object.values(temp[t])[0]);
    	struct["last_name"].push(Object.values(temp[t])[1]);
    	struct["age"].push(Object.values(temp[t])[2]);
    	struct["country"].push(Object.values(temp[t])[3]);
    	struct["occupation"].push(Object.values(temp[t])[4]);
  }
  return struct;
}

const csv_data = await fetchData("https://raw.githubusercontent.com/julien-blanchard/datasets/main/fake_csv.csv");
const parsed = getData(csv_data);
console.log(parsed);

// **********************************************************************

await import("https://cdn.jsdelivr.net/npm/arquero@latest");

const getTable = (data,where) => {
  const dframe = aq.table(data);
  let viz_df = document.getElementById(where);
  viz_df.innerHTML = aq.table(dframe).toHTML({limit: 10})
}

const csv_data = await fetchData("https://raw.githubusercontent.com/julien-blanchard/datasets/main/fake_csv.csv");
const parsed = getData(csv_data);
getTable(parsed,"viz");

// **********************************************************************

import {csvParse, csvParseRows} from "https://cdn.skypack.dev/d3-dsv@3";
await import("https://cdn.jsdelivr.net/npm/apexcharts");

// **********************************************************************

const fetchData = async (csv_file) => {
  return fetch(csv_file).then(
    d => {return d.text()}
  )
};

const getData = (data) => {
  let struct = new Array();
  let parsed = csvParse(data);
  let parsed_values = Object.values(parsed).slice(0,5)
  for (let p of parsed_values) {
    struct.push(
      {
        x: p["First_name"],
        y: p["Age"]
      }
    )
  }
  return struct;
}

const csv_data = await fetchData("https://raw.githubusercontent.com/julien-blanchard/datasets/main/fake_csv.csv");
const plot_data = await getData(csv_data);
console.log(plot_data);

// **********************************************************************

const getChart = (data) => {
  let options = {
    chart: {
      type: "treemap"
    },
    plotOptions: {
      treemap: {
        distributed: true
      }
    },
    series: [
      {
      	data: data
      }
      ]
  }
  let chart = new ApexCharts(document.querySelector("#viz2"), options);
  chart.render();  
}

const csv_data = await fetchData("https://raw.githubusercontent.com/julien-blanchard/datasets/main/fake_csv.csv");
const plot_data = await getData(csv_data);
await getChart(plot_data)

// **********************************************************************

let docs = [
    "Python is a high-level, general-purpose programming language.",
    "JavaScript, often abbreviated as JS, is a programming language that is one of the core technologies of the World Wide Web, alongside HTML and CSS.",
    "Elixir is a functional, concurrent, high-level general-purpose programming language that runs on the BEAM virtual machine, which is also used to implement the Erlang programming language."
  ];

// **********************************************************************

const tinytfidf = await import("https://cdn.skypack.dev/tiny-tfidf");

const corpus = new tinytfidf.Corpus(
  ["doc1", "doc2", "doc3"],
  docs
);

const getTfIfPerDoc = (data,whichdoc) => {
  console.log("\n")
  let results = data.getTopTermsForDocument(whichdoc);
  for (let t in results) {
    console.log(`TERM for ${whichdoc}: ${results[t][0]} | SCORE: ${results[t][1].toFixed(2)}`)
  }
}

["doc1", "doc2", "doc3"].forEach(d => {getTfIfPerDoc(corpus,d)})
