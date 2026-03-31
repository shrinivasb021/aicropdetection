function uploadImage() {

let fileInput =
document.getElementById(
"imageInput"
);

let file =
fileInput.files[0];

let formData =
new FormData();

formData.append(
"file",
file
);

fetch("/predict", {

method: "POST",

body: formData

})

.then(
response =>
response.json()
)

.then(data => {

document.getElementById(
"result"
).innerHTML =

`
Disease:
<b>${data.disease}</b>

<br>

Confidence:
<b>${data.confidence}%</b>

<br>

Treatment:
<b>${data.treatment}</b>
`;

});

}
