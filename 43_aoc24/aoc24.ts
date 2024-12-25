const input_data: number[][] = [
  [3,4,2,1,3,3],
  [4,3,5,3,9,3]
];

//////////////////

const sorted_array_left : number[] = input_data[0].sort();
const sorted_array_right : number[] = input_data[1].sort();
console.log(sorted_array_left);
console.log(sorted_array_right);

//////////////////

const getDistance = (data: number[][]): number => {
  let result: number = 0;
  const sorted_array_left : number[] = data[0].sort();
  const sorted_array_right : number[] = data[1].sort();

  for (let i = 0; i < data[0].length; i++) {
    let dist: number = Math.abs(sorted_array_left[i] - sorted_array_right[i]);
    result += dist;
  }
  return result;
};

const distance: number = getDistance(input_data);
console.log(`The result is:\n\n\t${distance}`);

//////////////////

const input_data: string[] = [
  "7 6 4 2 1",
  "1 2 7 8 9",
  "9 7 6 2 1",
  "1 3 2 4 5",
  "8 6 4 4 1",
  "1 3 6 7 9"
];

//////////////////

const textToMatrix = (data: string[]): number[][] => {
let result: number[][] = [];
for (let d of data) {
  let string_to_array: string[] = d.split(" ");
  let temp_array: number[] = [];
  for (let s of string_to_array) {
    temp_array.push(parseInt(s));
  };
  result.push(temp_array);
};
return result;
};

const text_to_matrix: number[][] = textToMatrix(input_data);
console.log(text_to_matrix);

//////////////////

const firstFilter = (data: number[][]): boolean[][] => {
let result: boolean[][] = [];
for (let d of data) {
  let current_row: boolean[] = [];
  for (let i = 1; i < d.length; i++) {
    if ((Math.abs(d[i] - d[i-1]) <= 3) && (d[i] != d[i-1])) {
      current_row.push(true);
    }
    else {
      current_row.push(false);
    };
  };
  result.push(current_row);
};
return result;
};

const first_filter: boolean[][] = firstFilter(text_to_matrix);
console.log(first_filter);

//////////////////

const input_data_filtered: number[][] = [
  [7,6,4,2,1],
  [1,3,2,4,5],
  [1,3,6,7,9]
];

//////////////////

const secondFilter = (data: number[][]): number[][] => {
  let result: number[][] = [];
  for (let d of data) {
    let new_row: number[] = [];
    for (let i = 1; i < d.length; i++) {
      if (d[i] > d[i-1]) {
        new_row.push(1);
      }
      else {
        new_row.push(0);
      }
    };
    result.push(new_row);
  };
  return result;
};

const second_filter: number[][] = secondFilter(input_data_filtered)
console.log(second_filter);

//////////////////

const input_data: string = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";

//////////////////

const pattern_functions: RegExp = /mul\(\d+,\d+\)/g;
const pattern_integers: RegExp = /\d+,\d+/g;

//////////////////

const extractFunctions = (data: string): string[] => {
  let result: string[] = [];
  let match: any;
  while ((match = pattern_functions.exec(data)) != null) {
    result.push(match[0]);
  };
  return result;
};

const extracted_functions: string[] = extractFunctions(input_data);
console.log(extracted_functions);

//////////////////

const extractIntegers = (data: string[]): number[][] => {
  let result: number[][] = [];
  let match: any;
  for (let d of data) {
    let integers_to_multiply: number[] = [];
    while ((match = pattern_integers.exec(d)) != null) {
      let split_integers: string[] = match[0].split(",");
      split_integers.forEach(i => integers_to_multiply.push(parseInt(i)));
      result.push(integers_to_multiply);
    };
  };
  return result;
};

const extracted_integers: number[][] = extractIntegers(extracted_functions);
console.log(extracted_integers);

//////////////////

const getSum = (data: number[][]): void => {
  let result: number = 0;
  for (let d of data) {
    let multiplied: number = d[0] * d[1];
    result += multiplied
  };
  console.log(`The result is:\n\n\t${result}`)
};

getSum(extracted_integers);

//////////////////