const url: string = "https://raw.githubusercontent.com/julien-blanchard/datasets/main/fact_check_articles.json";

const fetchData = async (file: string) => {
  const request = new Request(file);
  return fetch(request)
  .then(req => { return req.json() })
  .then(results => {
    let result: any = results;
    let num_articles: number = Object.keys(result).length;
    let random_article: number = Math.floor(Math.random() * num_articles)
    console.log(result[random_article])
    }
  )
}

await fetchData(url);

// **********************************************************************

const url: string = "https://raw.githubusercontent.com/julien-blanchard/datasets/main/fact_check_articles.json";

type Corpus = { [key: string]: string }

const fetchData = async (file: string) => {
  const request = new Request(file);
  return fetch(request)
  .then(req => { return req.json() })
  .then(results => {
    let result: any = results;
    let num_articles: number = Object.keys(result).length;
    let random_article: number = Math.floor(Math.random() * num_articles);
    let corpus: Corpus = {
      Article: result[random_article]["text"],
      Excerpt: result[random_article]["excerpt"]
    }
    return corpus;
    }
  )
}

const text: Corpus = await fetchData(url);
console.log(text);

// **********************************************************************

import * as tr from "textrank";

const text: Corpus = await fetchData(url);
let textRank: any = new tr.TextRank(text["Article"]);
let summary: string = textRank.summarizedArticle
console.log(`TextRank summary:\n\n${summary}\n\nOfficial excerpt:\n\n${text["Excerpt"]}`);

// **********************************************************************

type params = {
  [key: string]: number | string
};

const getSummary = (text: string, n_sentences: number): string => {
  let settings: params = {
    extractAmount: n_sentences,
    d: 0.95,
    summaryType: "string"
  }

  let textRank: any = new tr.TextRank(text, settings);
  let result: string = textRank.summarizedArticle;
  return result;
}

const text: Corpus = await fetchData(url);
let summary: string = getSummary(text["Article"],3);
console.log(f,`TextRank summary:\n\n${summary}\n\nOfficial excerpt:\n\n${text["Excerpt"]}`,f);

// **********************************************************************

import { HfInference } from "@huggingface/inference";

const getSummary = async (text: string, max_output: number): Promise<{[key: string]: string}> => {
    let HF_ACCESS_TOKEN: string = "********";
    const inference: any = new HfInference(HF_ACCESS_TOKEN);
    const result: {[key: string]: string} = await inference.summarization({
        model: "sshleifer/distilbart-cnn-12-6",
        inputs: text,
        parameters: {
          max_length: max_output
        }
      })
    return result;
}

const text: Corpus = await fetchData(url);
let summary: {[key: string]: string} = await getSummary(text["Article"], 80);
console.log(`Transformers.js summary:\n\n${summary["summary_text"]}\n\nOfficial excerpt:\n\n${text["Excerpt"]}`);