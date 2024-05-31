const fetchData = (csv_file) => {
        const request = new Request(csv_file);
        return fetch(request)
            .then(req => {return req.text()})
            .then(result => {console.log(result)});
    }

const getData = async (csv_file) => {
        const data = await fetchData(csv_file);
        return data;
    }

getData("https://opendata-geohive.hub.arcgis.com/datasets/d9be85b30d7748b5b7c09450b8aede63_0.csv");

// **********************************************************************

const getDataFrame = (csv_file) => {
        let viz_df = document.getElementById("viz");
        let struct = {
            county: [],
            population: [],
            confirmed_cases: [],
            timestamp: [],
        };

const request = new Request(csv_file);
        fetch(request)
            .then(req => {return req.text()})
            .then(data => {
                let rows = data.split("\n").slice(1);
                for (let r of rows) {
                    struct["county"].push(r.split(",")[2]);
                    struct["population"].push(r.split(",")[3]);
                    struct["confirmed_cases"].push(r.split(",")[10]);
                    struct["timestamp"].push(r.split(",")[4]);
                    }
                viz_df.innerHTML = aq.table(struct).toHTML({limit: 10})
                }
            );
        return struct;
    }

getDataFrame("https://opendata-geohive.hub.arcgis.com/datasets/d9be85b30d7748b5b7c09450b8aede63_0.csv")

// **********************************************************************

const getDataFrame = async (csv_file) => {
        let viz_df = document.getElementById("viz");
        const dt = await aq.loadCSV(csv_file);
        viz_df.innerHTML = aq
            .table(dt)
            .toHTML({limit: 10})
        }
getDataFrame("https://opendata-geohive.hub.arcgis.com/datasets/d9be85b30d7748b5b7c09450b8aede63_0.csv")

// **********************************************************************

const getDataFrame = (csv_file) => {
        let cols = ["CountyName","PopulationCensus16","TimeStamp","ConfirmedCovidCases"]
        dfd.readCSV(csv_file)
            .then(df => {
                df
                .loc( {columns: cols} )
                .head(20)
                .plot("viz")
                .table();
            }
        )
    }; 

getDataFrame("https://opendata-geohive.hub.arcgis.com/datasets/d9be85b30d7748b5b7c09450b8aede63_0.csv")