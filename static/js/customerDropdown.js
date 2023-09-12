fetch('/get_customers.json')
.then(response => response.json())
.then((data) => {
    let text = "";
    let len = data.length;
    let i = 0;

    for (; i < len; i++ ) {
        text += "<option value='" + data[i] + "'>" + data[i] + "</option>\n"
    }

    document.querySelector('#email-dropdown').innerHTML = text 
});