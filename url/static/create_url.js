document.addEventListener("DOMContentLoaded", ()=>{
    document.querySelector("ol").append(create_list_element(1, 1, ""));

    document.getElementById("add-button").onclick = () => {
      document.querySelector("ol").append(create_list_element(get_n(), 1, ""));

      calculate_percent_change();
    };

    document.getElementById("create-url").onclick = () => {
        let data = get_data();

        let h = {
            'destinations': data['destinations'],
            'probs': data['probs'],
            'X-CSRFToken': window.CSRF_TOKEN
        };

        let req = new Request("", {
            method: 'POST',
            headers: h,
            mode: 'same-origin'
        });

        fetch(req).then((response) => {
            window.location = "account";
        });
    };
});


// Basic Wannabe React Functionality
function create_list_element(n, percent, dest){
    // This is just such as long function, I could shorten it, but I have no desire to
    let button = document.createElement("button");
    button.onclick = delete_element;
    button.className = "btn btn-primary";
    button.innerText = "Remove Destination";
    button.id = `btn-${n}`;

    let bottom_col_2 = document.createElement("div");
    bottom_col_2.className = "col";
    bottom_col_2.append(button);

    let text_input = document.createElement("input");
    text_input.type = "url";
    text_input.placeholder = "Put your URL here";
    text_input.id = `text-${n}`;

    let bottom_col_1 = document.createElement("div");
    bottom_col_1.className = "col";
    bottom_col_1.append(text_input);
    // Appended to the text input should be a link which you could click to test your url

    let bottom_row = document.createElement("div");
    bottom_row.className = "row";
    bottom_row.append(bottom_col_1);
    bottom_row.append(bottom_col_2);

    let slider = document.createElement("input");
    slider.type = "range";
    slider.min = "1";
    slider.max = "100";
    slider.value = `${(percent * 100).toFixed(0)}`;
    slider.onchange = calculate_percent_change;

    let top_col_1 = document.createElement("div");
    top_col_1.className = "col";
    top_col_1.append(slider);

    let percent_indicator = document.createElement("h5");
    percent_indicator.innerText = `${(percent * 100).toFixed(0)}%`

    let top_col_2 = document.createElement("div");
    top_col_2.className = "col";
    top_col_2.append(percent_indicator);

    let top_row = document.createElement("div");
    top_row.className = "row";
    top_row.append(top_col_1);
    top_row.append(top_col_2);

    let container = document.createElement("div");
    container.className = "container";
    container.append(top_row);
    container.append(bottom_row);

    let list_group = document.createElement("div");
    list_group.className = "list-group-item";
    list_group.id = `url-${n}`;
    list_group.append(container);

    return list_group;
}

function delete_element(event){
    event.path[4].remove(); // Deletes the list group, container, etc
}

function calculate_percent_change(){ // Called on the update of each slider
    // Sums the value of all of the sliders
    let sliders = document.querySelectorAll("div.col input[type='range']");
    let sum = 0;

    for(let i = 0; i < sliders.length; i++){
        sum += parseInt(sliders[i].value);
    }

    // Iterates through the sliders and uses their parents to do stuff
    for(let i = 0; i < sliders.length; i++){
        let percent = sliders[i].value / sum * 100;
        let percent_string = `${percent.toFixed(0)} %`;
        // Gets the heading and updates it
        let heading = sliders[i].parentNode.parentNode.children[1].children[0]; // Moves two up to the row, then moves back down the second column and to the heading

        heading.innerText = percent_string;
    }
}

function get_n(){
    return document.querySelector("ol").children.length;
}

function get_data(){
    // Gets the list group
    let lg = document.querySelector("ol"); // There is only one of these

    // Iterates through the list group and builds a destination - value model (these are based on slider values != percentages)
    let destinations = [];
    let probs = [];

    let sum = 0;
    for(let i = 0; i < lg.children.length; i++){
        let div = lg.children[i].children[0]; // Gets to the inner div

        let value = parseInt(div.children[0].children[0].children[0].value); // div > first row > first col > input > value
        sum += value; // creates a running sum which is used to formulate the percentages

        let destination = div.children[1].children[0].children[0].value; // div > second row > first col > input > value

        destination = destination.replace(" ", ""); // The bare minimum url processing

        destinations.push(destination);
        probs.push(value);
    }

    for(let i = 0; i < probs.length; i++){
        probs[i] = probs[i] / sum;
    }

    let return_object = {
        "destinations": destinations,
        "probs": probs
    }
    return return_object;
}
