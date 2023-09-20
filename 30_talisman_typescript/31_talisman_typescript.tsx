// **********************************************************************

import jaroWinkler from "talisman/metrics/jaro-winkler";

// **********************************************************************

const x: string = "raspberry";
const y: string = "strawberry";
const distance: number = jaroWinkler(x,y);

console.log(distance);

// **********************************************************************

const x: string = "I love fruits";
const y: string = "I adore raspberries";
const distance: number = jaroWinkler(x,y);

console.log(distance);

// **********************************************************************

const x: string = "raspberry";
const y: string = "byerarsrb";
const distance: number = jaroWinkler(x,y);

console.log(distance);

// **********************************************************************

const corpus: string[] = [
  "I love fruits",
  "I adore raspberries",
  "TypeScript is cool",
  "Programming is fun",
  "Julien loves pizzas"
  ];

// **********************************************************************

type distances = {
  [key: string]: number[];
};

// **********************************************************************

const getMatrix = (data: string[]): distances => {
  
  let inc: number = 1;
  let sent: string = "Sentence_";
  let struct: distances = {};
  
  for (let da of data) {
    for (let d of data) {
      let key: string = `${sent}${inc}`;
      if (!struct[key]) {
        struct[key] = [];
      }
        let jaro: number = jaroWinkler(da,d).toFixed(2)
        struct[`${sent}${inc}`].push(inc)
    }
    inc ++;  
  }
  return struct;
}

const matrix: distances = getMatrix(corpus);
console.log(matrix)

// **********************************************************************

import { all, desc, op, table } from 'arquero';

const d = {
  Name: ["Tomato", "Apple", "Lemon"],
  Price: [3,4,2],
  Color: ["Red","Green","Yellow"]
}

const getTable = (data) => {
  const dframe = table(data)
  console.log(dframe.print())
}
getTable(d);

// **********************************************************************

type distances = {
  [key:string]: number[] | string[];
};

const getMatrix = (data: string[]): distances => {
  
  let inc: number = 1;
  let sent: string = "Sentence_";
  let struct: distances = {};

  const sentences: string[] = data.map(x => sent + inc++);
  struct["Index"] = sentences;
  inc = 1;
  
  for (let da of data) {
    for (let d of data) {
      let key: string = `${sent}${inc}`;
      if (!struct[key]) {
        struct[key] = [];
      }
        let jaro: number = jaroWinkler(da,d).toFixed(2)
        struct[`${sent}${inc}`].push(jaro)
    }
    inc ++;  
  }
  return struct;
}

// **********************************************************************

const getTable = (data: distances) => {
  const dframe = table(data)
  console.log(dframe.print())
}

const matrix: distances = getMatrix(corpus);
getTable(matrix);