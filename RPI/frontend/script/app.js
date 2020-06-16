"use strict";

let lanIP = `${window.location.hostname}:5000`;

const socket = io(`http://${lanIP}`);

const provider = "https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png";
const copyright =
'&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
let map, layergroup;

//#region ***  DOM references ***
let html_ldr, html_rfid;
let html_timer, html_address, html_coords, html_navigate, html_owner, html_map;
let html_scorebord, html_graph;
let html_info_start, html_info_end, html_info_players, html_stopgame, html_shutdown;
// FORMS
let html_creategame, html_feedback;
//#endregion

//#region ***  Callback-Visualisation - show___ ***
const showGameInfo = function(jsonObject) {
  console.log(jsonObject)
  // HOMEPAGE: TIMER
  if (html_timer) {
    if (!jsonObject.Spel) {
      console.log("Geen spel bezig.");
      showNoGamePage();
      return;
    }

    console.log("Timer instellen");
    let countDownDate = new Date(jsonObject.Spel.Eindtijd);
    let timer = setInterval(function() {
      // Now
      let now = new Date(Date.now());
      let remaining = (countDownDate - now) /1000;
      if (remaining <= 0) {
        clearInterval(timer);
      }
      html_timer.innerHTML = toHHMMSS(remaining);
    }, 1000);
  }
  // INFO PAGE
  if (html_info_start) {
    const begintijd = new Date(jsonObject.Spel.Begintijd);
    const eindtijd = new Date(jsonObject.Spel.Eindtijd);
    html_info_start.innerHTML = customDateFormat(begintijd);
    html_info_end.innerHTML = customDateFormat(eindtijd);
    let table_content = "";
    for (let speler of jsonObject.Spelers) {
      table_content += `<tr><td>${speler.SpelerID}</td><td>${speler.Naam}</td><td>${speler.RFIDUID}</td></tr>`;
    }
    html_info_players.innerHTML = table_content;
  }
}

const showOwner = function(jsonObject) {
  if (jsonObject.Naam)
    html_owner.innerHTML = jsonObject.Naam;
  else
    html_owner.innerHTML = "Onbekend";
}

const showScoreboard = function(jsonObject) {
  if (jsonObject.error == null) {
    // Table
    let table_content = "";
    let rank = 1;
    for (let speler of jsonObject) {
      table_content += `<tr><td>${rank}</td><td>${speler.Naam}</td><td>${toHHMMSS(speler.Score)}</td></tr>`;
      rank++;
    }
    html_scorebord.innerHTML = table_content;

    // Chart
    let converted_labels = [];
    let converted_data = [];
    for (const speler of jsonObject) {
      converted_labels.push(speler.Naam);
      let uren = Math.round(speler.Score / 60 / 60,1);
      converted_data.push(uren);
    }
    drawChart(converted_labels, converted_data);
  }
  else {
    showNoGamePage();
  }
}

const showAddress = function(jsonObject) {
  console.log(jsonObject);
  const addr = jsonObject.address;

  if (addr.place) {
    html_address.innerHTML = `~ ${addr.place}`;
  }
  else {
    let straat = "";
    let nummer = "";
    let gemeente = "";
    if (addr.road)
      straat = addr.road;
    if (addr.house_number)
      nummer = addr.house_number;
    if (addr.city_district)
      gemeente = ", " + addr.city_district;
    else if (addr.city)
      gemeente = ", " + addr.city;
    else if (addr.town)
      gemeente = ", " + addr.town;
    html_address.innerHTML = `~ ${straat} ${nummer}${gemeente}`;
  }
}

const showMarker = function(coords) {
  layergroup.clearLayers();
  var myIcon = L.icon({
    iconUrl: '/img/svg/place-24px.svg',
    iconSize: [40,40]
});
  let marker = L.marker(coords, { icon: myIcon }).addTo(layergroup);
  map.setView(coords, 18);
}

const drawChart = function(labels, data) {
  let ctx = html_graph.getContext("2d");

  let config = {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Score (uur)",
          borderColor: "#990808",
          backgroundColor: "#990808",
          data: data
        }
      ]
    },
    options: { // Opties om de stijl en het gedrag vd grafiek aan te passen
      responsive: true,
      title: {
          display: false,
          text: 'Score per speler'
      },
      tooltips: {
          mode: 'index',
          intersect: true
      },
      hover: {
          mode: 'interact',
          intersect: true
      },
      scales: {
          xAxes: [
              {
                  display: true,
                  scaleLabel: {
                      display: false,
                      labelString: 'Speler'
                  }
              }
          ],
          yAxes: [
              {
                  display: true,
                  scaleLabel: {
                      display: false,
                      labelString: 'Score (uur)'
                  },
                  ticks: {
                    suggestedMin: 0
                  }
              }
          ]
      }
  }
  };

  let myChart = new Chart(ctx, config);
}

const showNoGamePage = function() {
  window.location.href = `geenspel.html`;
}

const showFeedback = function(type, msg) {
  html_feedback.classList.remove("c-feedback--success");
  html_feedback.classList.remove("c-feedback--error");
  if (type == "success")
    html_feedback.classList.add("c-feedback--success"); 
  else
    html_feedback.classList.add("c-feedback--error");
  html_feedback.innerHTML = msg;
}
//#endregion

//#region ***  Callback-No Visualisation - callback___  ***
const callbackCreateGame = function() {
  showFeedback("success", "De game is aangemaakt.");
}

const callbackErrorCreateGame = function() {
  showFeedback("error", "Er gings iets fout bij het aanmaken.");
}

const callbackStopGame = function() {
  alert("Stopped");
}
//#endregion

//#region ***  Data Access - get___ ***
const getGameInfo = function() {
  handleData(`http://${lanIP}/CTB/Spel`, showGameInfo);
}

const getBezit = function() {
  handleData(`http://${lanIP}/CTB/Bezit`, showOwner);
}

const getScoreboard = function() {
  handleData(`http://${lanIP}/CTB/Scorebord`, showScoreboard);
}

const getEstimateLocation = function(lat, long) {
  handleData(`https://nominatim.openstreetmap.org/reverse?lat=${lat}0&lon=${long}&format=json`, showAddress)
}
//#endregion

//#region ***  Event Listeners - listenTo___ ***

const listenToSocket = function () {
  socket.on('connect', function() {
    console.log("Connected");
  });

  socket.on('B2F_MVP1_LDR', function(payload) {
    console.log(`LDR: ${payload.Waarde}`);
  });

  if (html_coords) {
    socket.on('B2F_GPS_locatie', function(payload) {
      let GPS_data = payload.Waarde.split(";")
      html_coords.innerHTML = GPS_data[0] + ", " + GPS_data[1];
  
      showMarker(GPS_data);
      getEstimateLocation(GPS_data[0], GPS_data[1]);

      html_navigate.href = `https://www.google.com/maps/place/${GPS_data[0]}+${GPS_data[1]}`;
    });
  }
};

const listenToClickCreateGame = function () {
  html_creategame.addEventListener("click", function() {
    let bdatum = document.querySelector("#startdate").value;
    let btijd = document.querySelector("#starttime").value;
    let edatum = document.querySelector("#enddate").value;
    let etijd = document.querySelector("#endtime").value;
    let raw_spelers = document.querySelector("#players").value;

    let errors = new Array;
    if (bdatum == "" && btijd == "") {
      errors.push("Geen begintijd ingevuld.")
    }
    if (edatum == "" && etijd == "") {
      errors.push("Geen eindtijd ingevuld.")
    }
    if (raw_spelers == "") {
      errors.push("Geen spelers ingevuld.")
    }

    if (errors.length > 0) {
      let errorMsg = "";
      for (let e of errors) {
        errorMsg += e + "<br>";
      }
      showFeedback("error", errorMsg);
    }
    else {
      console.log(bdatum + " " + btijd + " " + edatum + " " + etijd + " " + raw_spelers)
      let begintijd = bdatum + " " + btijd;
      let eindtijd = edatum + " " + etijd;
      let spelers = raw_spelers.split(",").map(item => item.trim());
      const jsonObject = {
        begintijd:  begintijd,
        eindtijd:   eindtijd,
        spelers:    spelers
      }
      console.log(jsonObject);
      handleData(`http://${lanIP}/CTB/Spel`, callbackCreateGame, callbackErrorCreateGame, "POST", JSON.stringify(jsonObject));
    }
  });
}

const listenToClickStopGame = function() {
  html_stopgame.addEventListener("click", function() {
    handleData(`http://${lanIP}/CTB/Spel/Stop`, callbackStopGame, null, "POST");
  });
}

const listenToClickShutdown = function() {
  html_shutdown.addEventListener("click", function() {
    socket.emit("F2B_shutdown", "Shutdown")
  });
}
//#endregion

//#region ***  INIT / DOMContentLoaded  ***
const init = function () {
  // Home
  html_timer = document.querySelector(".js-timer");
  html_map = document.querySelector(".js-map");
  html_coords = document.querySelector(".js-coords");
  html_navigate = document.querySelector(".js-navigate");
  html_address = document.querySelector(".js-est-address");
  html_owner = document.querySelector(".js-owner");
  // Scoreboard
  html_scorebord = document.querySelector(".js-scoreboard");
  html_graph = document.querySelector(".js-graph");
  // Game info
  html_info_start = document.querySelector(".js-info_start");
  html_info_end = document.querySelector(".js-info_end");
  html_info_players = document.querySelector(".js-info_players"); 
  html_stopgame = document.querySelector(".js-stopgame");
  html_shutdown = document.querySelector(".js-shutdown");
  // Form (create game)
  html_creategame = document.querySelector(".js-creategame");
  html_feedback = document.querySelector(".js-feedback");

  console.log("DOM is geladen");

  if (html_timer || html_info_start) {
    getGameInfo();
  }
  if (html_map) {
    map = L.map('js-map', { zoomControl: false }).setView([50.849210, 4.352386], 9);
    L.tileLayer(provider, { attribution: copyright }).addTo(map);
    layergroup = L.layerGroup().addTo(map);
  }
  if (html_owner) {
    getBezit();
  }
  if (html_scorebord) {
    getScoreboard();
  }
  if (html_creategame) {
    listenToClickCreateGame();
  }
  if (html_stopgame) {
    listenToClickStopGame();
  }
  if (html_shutdown) {
    listenToClickShutdown();
  }

  listenToSocket();
};
//#endregion

document.addEventListener("DOMContentLoaded", init);

const toHHMMSS = function (sec) {
  if (sec == null) {
    return "00:00:00"
  }
  let sec_num = parseInt(sec, 10);
  let hours   = Math.floor(sec_num / 3600);
  let minutes = Math.floor((sec_num - (hours * 3600)) / 60);
  let seconds = sec_num - (hours * 3600) - (minutes * 60);

  if (hours   < 10) {hours   = "0"+hours;}
  if (minutes < 10) {minutes = "0"+minutes;}
  if (seconds < 10) {seconds = "0"+seconds;}
  return hours+':'+minutes+':'+seconds;
}

const customDateFormat = function(datum) {
  const months = [ "?", "januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december" ]
  let customDate = "";
  customDate += datum.getDate() + " " + months[datum.getMonth()]; // dd/mm
  customDate += " om " + addLeadingZeros(datum.getHours()) + ":" + addLeadingZeros(datum.getMinutes()); // om hh:mm
  return customDate;
}

const addLeadingZeros = function(nummer) {
  if (nummer < 10)
    return "0" + nummer;
  else
    return nummer
}