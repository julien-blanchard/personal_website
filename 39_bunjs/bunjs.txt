const server = Bun.serve(
    {
        port: 3000,
        fetch(req,server) {
            return new Response(`This article about Bun.js is live on ${req.url}`)
        }
    }
)
console.log(`Listening on port: ${server.port}`)

// **********************************************************************

let userClick = document.getElementById("processButton");
let userClear = document.getElementById("clearButton");

const parseText = () => {
    let userInput = document.getElementById("inputBox");
    let userOutput = document.getElementById("outputBox");
    userOutput.innerHTML = userInput.value;
  }

const clearText = () => {
    let userInput = document.getElementById("inputBox");
    let userOutput = document.getElementById("outputBox");
    userInput.value = "";
    userOutput.innerHTML = "";
  }

userClick.addEventListener("click", parseText);
userClear.addEventListener("click",clearText);

// **********************************************************************

const homePage = await Bun.file("./home.html").text();

const server = Bun.serve(
    {
        port: 3000,
        fetch(req,server) {
            return new Response(
                homePage,
                {
		            headers: {
		                "Content-type": "text/html"
		                }
		        }
            )
        } 
    }
)
console.log(`Listening on port: ${server.port}`)

// **********************************************************************

import { $ } from "bun";

await $`ls > files.txt`;

// **********************************************************************

import { $ } from "bun";

await $`column -s "," -t fake_csv.csv | grep engineer | head`;

// **********************************************************************

await $`cat fake_csv.csv | awk -F, '{print $4","$5}' | sort | uniq | head`;

// **********************************************************************

import {Database} from "bun:sqlite";

const db = new Database("weather.db");

// **********************************************************************

const query = db.query("SELECT * FROM forecast LIMIT 10");

console.log(query.all());

// **********************************************************************

import {Database} from "bun:sqlite";
import * as aq from "arquero";

const db = new Database("weather.db");

type ParsedQuery = {[key: string]: string[]};

const parseQuery = (data: string): ParsedQuery => {
    const query = db.query(data).values();
    let queryContainer: ParsedQuery = {
        "County": [],
        "Day": [],
        "Min_temp": [],
        "Max_temp": [],
        "Forecast_day": [],
        "Forecast_night": [],
        "Wind_speed_day": [],
        "Wind_dir_day": [],
        "Wind_speed_night": [],
        "Wind_dir_night": [],
    }

    for (let q of query) {
        queryContainer["County"].push(q[0]);
        queryContainer["Day"].push(q[1]);
        queryContainer["Min_temp"].push(q[2]);
        queryContainer["Max_temp"].push(q[3]);
        queryContainer["Forecast_day"].push(q[4]);
        queryContainer["Forecast_night"].push(q[5]);
        queryContainer["Wind_speed_day"].push(q[6]);
        queryContainer["Wind_dir_day"].push(q[7]);
        queryContainer["Wind_speed_night"].push(q[8]);
        queryContainer["Wind_dir_night"].push(q[9]);
    }
    return queryContainer;
}

const getDataFrame = (data: ParsedQuery): any => {
    const dframe = aq.table(data);
    dframe.print();
}


const parsed_query: ParsedQuery = parseQuery("SELECT * FROM forecast LIMIT 10");
getDataFrame(parsed_query);

// **********************************************************************

import {Database} from "bun:sqlite";
import * as aq from "arquero";

const db = new Database("weather.sqlite");

type ParsedQuery = {[key: string]: string[]};

const parseQuery = (data: string): ParsedQuery => {
    const query = db.query(data).values();
    let queryContainer: ParsedQuery = {
        "County": [],
        "Day": [],
        "Min_temp": [],
        "Max_temp": [],
        "Forecast_day": [],
        "Forecast_night": [],
        "Wind_speed_day": [],
        "Wind_dir_day": [],
        "Wind_speed_night": [],
        "Wind_dir_night": [],
    }

    for (let q of query) {
        queryContainer["County"].push(q[0]);
        queryContainer["Day"].push(q[1]);
        queryContainer["Min_temp"].push(q[2]);
        queryContainer["Max_temp"].push(q[3]);
        queryContainer["Forecast_day"].push(q[4]);
        queryContainer["Forecast_night"].push(q[5]);
        queryContainer["Wind_speed_day"].push(q[6]);
        queryContainer["Wind_dir_day"].push(q[7]);
        queryContainer["Wind_speed_night"].push(q[8]);
        queryContainer["Wind_dir_night"].push(q[9]);
    }
    return queryContainer;
}

const server = Bun.serve({
    fetch(req) {
        const parsed_query: ParsedQuery = parseQuery("SELECT * FROM forecast LIMIT 40");
        const df = aq.table(parsed_query).toHTML();
        return new Response(`<h1>Weather data</h1><br><div>${df}</div>`, {
            headers: {
                "Content-Type": "text/html",
            },
        });
    },
  });
