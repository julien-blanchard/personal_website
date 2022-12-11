d3.csv(data).then(csv_file => {
  for (let c of csv_file) {
    console.log(Object.values(c))
  }
})

// **********************************************************************

let temp_n = new Array();
let n = new Array();
let e = new Array();

// **********************************************************************

for (let i in data) {
    temp_n.push( Object.values(data[i])[0] );
    e.push( {from: Object.values(data[i])[0], to: Object.values(data[i])[1]} );};
    temp_n = temp_n.filter((v, i, a) => a.indexOf(v) === i);

for (t of temp_n) {
    n.push( {id: t} );
};

// **********************************************************************

let network = {nodes: n, edges: e};

// **********************************************************************

const getNetworkPlot = (data,chart_title) => {
    d3.csv(data).then(data => {

        // container arrays
        let temp_n = new Array();
        let n = new Array();
        let e = new Array();

        // looping through the CSV file
        for (let i in data) {
           temp_n.push( Object.values(data[i])[0] );
           e.push( {from: Object.values(data[i])[0], to: Object.values(data[i])[1]} );
           };
         temp_n = temp_n.filter((v, i, a) => a.indexOf(v) === i);
         for (t of temp_n) {
            n.push( {id: t} );
            };

         // data structure that can be read by AnyChart
         let network = {nodes: n, edges: e};

         // creating the chart
         let chart = anychart.graph(network);
         chart.layout().iterationCount(47);
         chart.rotation(40);

         // aesthetics

         // title
         let title = chart.title();
         title.text(chart_title);
         title.enabled(true);
         title.fontSize(25);
         title.fontColor("#616161")
         title.fontFamily("verdana");

         // background colours
         chart.background().fill("#e2e2e2");

         // nodes
         chart.nodes().labels().enabled(true);
         chart.nodes().labels().fontSize(14);
         chart.nodes().labels().fontColor("#616161");
         chart.nodes().normal().height(40);
         chart.nodes().normal().stroke("#d3d3d3", 8);
         chart.nodes().normal().fill("#ffff");
         chart.nodes().hovered().height(50);
         chart.nodes().hovered().shape("star10");
         chart.nodes().hovered().fill("#FFA1CF");
         chart.nodes().hovered().stroke("#ffff", 8);
         chart.nodes().tooltip().useHtml(true);

         // edges
         chart.edges().tooltip().useHtml(true);
         chart.edges().normal().stroke("#ffff", 1, "10 5");

         // ploting
         chart.container("vis");
         chart.draw();
         }
      );
  }

getNetworkPlot(pokemons,"Test");