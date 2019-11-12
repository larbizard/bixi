//TODO: Import Google Maps NPM instead of using script in index.html

var vm = new Vue({
  el: '#search-bar',
  data: {
      markerCoordinates: [],
      selectedDay: 'Sunday',
      days: [
      { text: 'Sunday', value: 'W-SUN' },
      { text: 'Monday', value: 'W-MON' },
      { text: 'Tuesday', value: 'W-TUE' },
      { text: 'Wednesday', value: 'W-WED' },
      { text: 'Thursday', value: 'W-THU' },
      { text: 'Friday', value: 'W-FRI' },
      { text: 'Saturday', value: 'W-SAT' },
      ],
      hour: '14',
      short_name: '6043',
      server_path: 'https://06f98462.ngrok.io/bixiOccupancy/',
      map: '',
      markers: []
  },
  mounted: function () {
  try{
    this.map = new google.maps.Map(document.getElementById('mapName'), {
          center: {lat: 45.509462, lng: -73.613413},
          zoom: 13
        });
        this.getStationMarkers();
  }
  catch(e){
    alert(e);
  }
  },
  methods: {
  hideAllInfoWindows() {
   this.markers.forEach(function(marker) {
     marker.infowindow.close(this.map, marker);
  });
},
  getDayText(value){
    var dayName = '';
    this.days.forEach(function(day){
        if(value == day.value) {dayName = day.text};
    });
    return dayName;
  },
  getTheMostBusyStations(){
  /*Append the result to an area of the screen when ready
    this.markers.forEach(marker){
    };*/
  },
  getBikeIcon(occupancy){
    if(occupancy>80){
        return 'images/green-bike.png';
    }else if(occupancy>50){
       return 'images/yellow-bike.png';
    }else if(occupancy>25){
       return 'images/orange-bike.png';
    }else{
       return 'images/black-bike.png';
    }
  } ,
    formFetchData(){
        var self = this;
        try{
            axios.post(self.server_path,
            {
                data: {
                    "year": 2019,
                    "day": self.selectedDay,
                    "hour": Number(self.hour),
                    "short_name": self.short_name
                    }
            }).then(response => {
              occupancy = response.data.result['occupancy'];
              var $displayed_text =$("<p style='font-size: 3vw'>At station "+ self.short_name +
              " availibility on "+ self.selectedDay + " between " + self.hour.toString()  + ":00 and " +
              (Number(self.hour)+1).toString() + ":00 is "+occupancy.toString()+"%</p>");
              alert($displayed_text.html().toString());
            }).catch(error => {
              alert("This station was not parsed!");
            });
        }
        catch(e){
            alert(e);
        }

    },
    fetchData(infowindow, marker, short_name) {
        var self = this;
        try{
            axios.post(self.server_path,
            {
                data: {
                    "year": 2019,
                    "day": self.selectedDay,
                    "hour": Number(self.hour),
                    "short_name": short_name
                    }
            }).then(response => {
              occupancy = response.data.result['occupancy'];
              infowindow.setContent("<p style='font-size: 1.5vw'><img src='" + this.getBikeIcon(occupancy) + "'/><br/>At station <strong>"+ marker.title    +
              "</strong><br/>on "+ this.getDayText(self.selectedDay) + "'s<br/>between <strong>" + self.hour.toString()  + ":00</strong> and <strong>" +
              (Number(self.hour)+1).toString() + ":00</strong><br/><strong>"+occupancy.toString()+"%</strong> of bikes are available.<br/>An<strong> average of " + Math.floor(occupancy*marker.station_data['capacity']/100) + " out of " + marker.station_data['capacity'] + " bikes.</strong></p>");
              marker.setIcon(self.getBikeIcon(occupancy));
              infowindow.open(this.map, marker);
            }).catch(error => {
              alert("This station was not parsed!");
            });
        }
        catch(e){
            alert(e);
        }

    },
    getStationMarkers() {
        try{
            var self = this;
            axios.get('https://api-core.bixi.com/gbfs/en/station_information.json',
            ).then(response => {
                response.data.data.stations.forEach((coord) => {
                  const position = new google.maps.LatLng(coord.lat, coord.lon);
                  var infowindow = new google.maps.InfoWindow({
                  });

                  const marker = new google.maps.Marker({
                    position : position,
                    map : this.map,
                    title : coord.name,
                    icon : 'images/red-bike-no-back.png'
                  });
                  marker.station_data = coord;
                  marker.addListener('click', function() {
                    self.hideAllInfoWindows();
                    self.fetchData(infowindow, marker, coord.short_name);
                  });
                  marker.infowindow = infowindow;
                  this.markers.push(marker);

                });
            });
        }
        catch(e) {
            alert(e);
        }
    }
  },
});

vm.selectedDay = 'W-SUN';
vm.day = 'W-SUN';