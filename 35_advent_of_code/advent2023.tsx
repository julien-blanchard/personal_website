const text: string[] = [
  "1abc2",
  "pqr3stu8vwx",
  "a1b2c3d4e5f",
  "treb7uchet"
];

type Result = {
  [key: number]: number[];
};

const getAllIntegers = (data: string[]): Result => {
  let result: Result = {};
  for (let i = 0; i < data.length; i++) {
    result[i] = [];
    for (let char of data[i]) {
      let temp_char: any = new RegExp(/^[0-9]/);
      if (temp_char.test(char)) {
        result[i].push(parseInt(char));
      }
    }
  }
  return result;
}

const getSelectedIntegers = (data: Result): number[] => {
  let result: number[] = [];
  for (let d in data) {
    let first_integer: number = data[d][0];
    let last_integer: number = data[d].slice(-1)[0]; 
    result.push(first_integer);
    result.push(last_integer);
  }
  return result;
};

const getFinalResults = (data: number[]): number => {
  let result: number = 0;
  data.forEach(nums => {result += nums});
  console.log(`The answer for puzzle 1 is:\n\n\t${result}\n`);
  return result;
};

const first: Result = getAllIntegers(text);
const second: number[] = getSelectedIntegers(first)
getFinalResults(second);

// **********************************************************************

const puzzle: string[] = [
  "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
  "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
  "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
  "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
  "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
];

type All_Games = {
  [key: string]: {[key: string]: number[]}
;}

type Possible_Games = {
[key: number]: boolean[]
};

const getAllGames = (data: string[]): All_Games => {
  
  let result: All_Games = {};

  for (let d of data) {
    let game: string = d.split(":")[0].split(" ")[1];
    let cubes: string = d.split(":")[1];
    let cube: string[] = cubes.split(" ");

    result[game] = {};
    result[game]["red"] = [];
    result[game]["green"] = [];
    result[game]["blue"] = [];
    
    for (let i = 0; i < cube.length; i++) {
      if (cube[i].includes("red")) {
        result[game]["red"].push(parseInt(cube[i-1]));
      }
      else if (cube[i].includes("green")) {
        result[game]["green"].push(parseInt(cube[i-1]));
      }
      else if (cube[i].includes("blue")) {
        result[game]["blue"].push(parseInt(cube[i-1]));
      }
    }
  }
  return result;
};

const getPossibleGames = (data: All_Games): Possible_Games => {
  let possible_games: Possible_Games = {};
  const thresholds: number[] = [12,13,14];
  for (let game in data) {
    possible_games[parseInt(game)] = [];
    for (let g in data[game]) {
      let cubes: number[] = data[game][g];
      if (g == "red") {
        possible_games[parseInt(game)].push(cubes.some(c => c > thresholds[0]));
      }
      else if (g == "green") {
        possible_games[parseInt(game)].push(cubes.some(c => c > thresholds[1]));
      }
      else if (g == "blue") {
        possible_games[parseInt(game)].push(cubes.some(c => c > thresholds[2]));
      }
    }
  }
  return possible_games;
};

const getWinningGames = (data: Possible_Games): number[] => {
  let result: number[] = [];
  for (let game in data) {
    //console.log(data[game]);
    if (!data[game].includes(true)) {
      result.push(parseInt(game));
    }
  }
  return result;
};

const getFinalResults = (data: number[]): number => {
  let result: number = 0;
  data.forEach(nums => {result += nums});
  console.log(`The answer for puzzle 2 is:\n\n\t${result}\n`);
  return result;
};

const all_games: All_Games = getAllGames(puzzle);
const all_possible_games: Possible_Games = getPossibleGames(all_games);
const winning_games: number[] = getWinningGames(all_possible_games);
getFinalResults(winning_games);