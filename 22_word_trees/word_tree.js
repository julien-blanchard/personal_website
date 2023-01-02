// **********************************************************************

let corpus = [
    ["Julien is a big fan of pizzas and salted caramel"],
    ["Julien loves pizzas and salted caramel"],
    ["Julien is a big fan of food in general"],
    ["Julien loves pizzas but he hates onions"],
    ["Julien is a big fan of pizzas but he hates onions"],
    ["Julien is a big fan of pizzas but he absolutely hates onions"],
    ["Julien is a big fan of pizzas"],
    ["Julien loves pizzas"]
]

// **********************************************************************

let chart = anychart.wordtree(corpus);
chart.container("viz");
chart.draw()

// **********************************************************************

const getWordTree = (data,chart_title) => {
    let chart = anychart.wordtree(data);
    let title = chart.title();
    title.text(chart_title);
    title.enabled(true);
    title.fontSize(35);
    title.align("left");
    title.fontColor("#e9ecef")
    title.fontFamily("helvetica");
    title.fontStyle("italic");
    chart.container("viz");
    chart.fontFamily("Helvetica");
    chart.fontColor("#e9ecef")
    let connectors = chart.connectors();
    connectors.stroke("4 #FFFFFF");
    chart.background().fill("#6c757d");
    chart.draw();
}

getWordTree(corpus,"Word Tree parser");

// **********************************************************************

const getPOSTags = (text) => {
  let result = new Array();
  let doc = nlp(text);
  doc.compute("penn");
  let data = doc.json()
  for (let d in data) {
      console.log(d, data[d]);
  }
}

getPOSTags("Julien is a big fan of pizzas and salted caramel.");

// **********************************************************************

let corpus_tags = new Array();

const getPOSTags = (text) => {
  let result = new Array();
  let doc = nlp(text);
  doc.compute("penn");
  let data = doc.json()
  for (let d in data) {
    for (let t in data[d].terms) {
      result.push(data[d].terms[t].penn);
    }
  }
  return result.join(" ");
}

corpus.forEach(
  c => corpus_tags.push([getPOSTags(c)])
)

corpus_tags.forEach(
  c => console.log(c)
)