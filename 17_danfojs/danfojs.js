let dataset_stocks = "https://github.com/julien-blanchard/dbs/blob/main/Stocks%20-%20Sept%202022.csv";
let dataset_news = "https://raw.githubusercontent.com/julien-blanchard/dbs/main/df_journal.csv";

// **********************************************************************

const getDataframe = (csv_file) => {
      dfd
        .readCSV(csv_file)
        .then(
          df => df)
          .whatever_method_we_want_to_apply_here
        )
      };

getDataframe(either_of_the_aformentioned_two_datasets)

// **********************************************************************

const getDataFrame = (csv_file) => {
   dfd.readCSV(csv_file)
      .then( d => let dataframe = d )
   return dataframe

let df = getDataFrame(either_of_the_aformentioned_two_datasets)

// **********************************************************************

async function getDataFrame(csv_file) {
        let df = await dfd.readCSV(csv_file);
        df.whatever_method_we_want_to_apply_here;
      }

getDataFrame(either_of_the_aformentioned_two_datasets)

// **********************************************************************

const dfd = require("danfojs-node")

async function getAsyncDataFrame(csv_file) {
    let df = await dfd.readCSV(csv_file);
    df.head().print()
}

getAsyncDataFrame(dataset_news);

// **********************************************************************

async function getAsyncDataFrame(csv_file) {
    let df = await dfd.readCSV(csv_file);
    df
        .loc( {columns: ["views","comments"]})
        .print()
}

getAsyncDataFrame(dataset_news);

// **********************************************************************

async function getAsyncDataFrame(csv_file) {
    let df = await dfd.readCSV(csv_file);
    df.loc({ rows: df["Meta"].gt(370) }).print()
}

getAsyncDataFrame(dataset_stocks);

// **********************************************************************

async function getAsyncDataFrame(csv_file) {
    let df = await dfd.readCSV(csv_file);
    df
        .groupby(["tag"])
        .col(["views"]).mean()
        .print()
}

getAsyncDataFrame(dataset_news);

// **********************************************************************

async function getAsyncDataFrame(csv_file) {
    let df = await dfd.readCSV(csv_file);
    df
        .loc({columns: ["tag","views"]})
        .groupby(["tag"])
        .col(["views"]).mean()
        .dropNa({ axis: 0 })
        .sortValues("views_mean", {ascending:false})
        .rename({"views_mean":"volume"})
        .print()
}

getAsyncDataFrame(dataset_news);

// **********************************************************************

df.head().plot("plot_div").table()

// **********************************************************************

let dataset_news = "https://raw.githubusercontent.com/julien-blanchard/dbs/main/df_journal.csv";
    async function getAsyncDataFrame(csv_file) {
      let df = await dfd.readCSV(csv_file);

      const config = {
          x: "tag",
          y: "volume"
      }

      df
          .groupby(["tag"])
          .col(["views"]).mean()
          .sortValues("views_mean", {ascending:false})
          .rename({"views_mean":"volume"})
          .plot("plot_div").bar( {config} )
        }

    getAsyncDataFrame(dataset_news);

// **********************************************************************

let stocks = "https://raw.githubusercontent.com/julien-blanchard/dbs/main/Stocks%20-%20Sept%202022.csv";

async function getDataFrame(csv_file,where) {
    let df = await dfd.readCSV(csv_file);
    df.plot(where).table();
  }

async function getBarPlot(csv_file,where) {
    let df = await dfd.readCSV(csv_file);
    const config = {
      columns: ["Meta","Amazon","Apple","Netflix","Google"],
      displayModeBar: true,
      displaylogo: false,
    };
    df.plot(where).line({ config });
  }

getDataFrame(stocks,"data")
getBarPlot(stocks,"plot");