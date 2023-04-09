// let start=0
const endpointUrl = "http://localhost:8000/";
const head=document.getElementById("header");
const songList = document.getElementById("song-list");

// .then(response => response.json())
function songDisplay(start){
fetch(endpointUrl+'get-songs/'+start)
        .then(response => response.json())
        .then(data => {
        // const data_new= JSON.parse(data);
        // console.log(data);
        // console.log(response.json());
        data.forEach(song => {
            const li = document.createElement("li");
            li.textContent = `${song[1]} `;
            
            // create a like button for the song
            const likeButton = document.createElement("button");
            likeButton.textContent = "Like";
            likeButton.onclick = function() {
              // call the like-song endpoint with the song ID
              fetch(endpointUrl+'like-song/'+song[0], { method: "POST" });
            };
            li.appendChild(likeButton);

            const simmButton = document.createElement("button");
            simmButton.textContent = "Get Similiar Songs";
            simmButton.onclick = function() {
                start=0;
                songList.innerHTML='';
                head.innerText="Similiar Songs to "+song[1]
                fetch(endpointUrl+'get-simm/'+song[0], { method: "GET" })
                .then(response => response.json())
                .then(data => {
                    data.forEach(song=>{
                        const li = document.createElement("li");
                        li.textContent = `${song[1]} `;
                        songList.appendChild(li);
                    })
                })
            };
            li.appendChild(simmButton);

            songList.appendChild(li);
          });
        })
        .catch(error => console.error(error));
    }

songDisplay(0);

const textBox = document.getElementById('start');
const submit = document.getElementById('submit');


submit.addEventListener('click', async () => {
    start=textBox.value;
    console.log(textBox)
    songList.innerHTML='';
    songDisplay(start);
});