const getNLP = () => {
  let tokens = getText();
  let choice = getChoice();
  let doc = nlp(tokens);
  if (choice == "To plural form") {
    doc.nouns().toPlural();
    document.getElementById("text_output").value = doc.text();
  }
  else if (choice == "To negative form") {
    doc.verbs().toNegative();
    document.getElementById("text_output").value = doc.text();
  }
  else if (choice == "To future tense") {
    doc.verbs().toFutureTense();
    document.getElementById("text_output").value = doc.text();
  }
  else if (choice == "To past tense") {
    doc.verbs().toPastTense();
    document.getElementById("text_output").value = doc.text();
  }
  else if (choice == "To POS tags") {
    doc.compute("penn");
    let tokens = doc.json()[0].terms;
    tags = tokens.map(term => [ term.text, term.penn]);
    let result = ""
    for (let tag of tags) {
        result += (tag.join(": ") + " / ");
    }
    document.getElementById("text_output").value = result.slice(0,-2);
  }
};

const getText = () => {
  let user_input = document.getElementById("text_input").value;
  return user_input;
};

const getChoice = () => {
  let user_choice = document.getElementById("choice").value;
  return user_choice;
}

// Clearing the text input area
const clearText = () => {
  document.getElementById("text_input").value = "";
  document.getElementById("text_output").value = "";
};

// **********************************************************************

let doc = nlp("I'm playing with JavaScript and that's cool.")
doc.contractions().expand()
console.log(doc.text())

// **********************************************************************

const getText = () => {
  let user_input = document.getElementById("text_input").value;
  return user_input;
}

// **********************************************************************

const getChoice = () => {
  let user_choice = document.getElementById("choice").value;
  return user_choice;
}

// **********************************************************************

const clearText = () => {
  document.getElementById("text_input").value = "";
  document.getElementById("text_output").value = "";
};

// **********************************************************************

const getNLP = () => {
  let tokens = getText();
  let choice = getChoice();
  let doc = nlp(tokens);
  if (choice == "To plural form") {
    doc.nouns().toPlural();
    document.getElementById("text_output").value = doc.text();
  }
  else if (choice == "To negative form") {
    doc.verbs().toNegative();
    document.getElementById("text_output").value = doc.text();
  }
  else if (choice == "To future tense") {
    doc.verbs().toFutureTense();
    document.getElementById("text_output").value = doc.text();
  }
  else if (choice == "To past tense") {
    doc.verbs().toPastTense();
    document.getElementById("text_output").value = doc.text();
  }
  else if (choice == "To POS tags") {
    doc.compute("penn");
    let tokens = doc.json()[0].terms;
    tags = tokens.map(term => [ term.text, term.penn]);
    let result = ""
    for (let tag of tags) {
        result += (tag.join(": ") + " / ");
    }
    document.getElementById("text_output").value = result.slice(0,-2);
  }
};

// **********************************************************************

let text = "Hi my name is Julien."
let doc = nlp(text);
doc.compute("penn");
let tokens = doc.json()[0].terms;
console.log(tokens);

// **********************************************************************

tags = tokens.map(term => [ term.text, term.penn]);
let result = "";
for (let tag of tags) {
        result += (tag.join(": ") + " / ");
    }
console.log(result);