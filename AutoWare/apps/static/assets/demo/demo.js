demo = {
  initPickColor: function() {
    $('.pick-class-label').click(function() {
      var new_class = $(this).attr('new-class');
      var old_class = $('#display-buttons').attr('data-class');
      var display_div = $('#display-buttons');
      if (display_div.length) {
        var display_buttons = display_div.find('.btn');
        display_buttons.removeClass(old_class);
        display_buttons.addClass(new_class);
        display_div.attr('data-class', new_class);
      }
    });
  },

  initDocChart: function() {
    chartColor = "#FFFFFF";

    // General configuration for the charts with Line gradientStroke
    gradientChartOptionsConfiguration = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      tooltips: {
        bodySpacing: 4,
        mode: "nearest",
        intersect: 0,
        position: "nearest",
        xPadding: 10,
        yPadding: 10,
        caretPadding: 10
      },
      responsive: true,
      scales: {
        yAxes: [{
          display: 0,
          gridLines: 0,
          ticks: {
            display: false
          },
          gridLines: {
            zeroLineColor: "transparent",
            drawTicks: false,
            display: false,
            drawBorder: false
          }
        }],
        xAxes: [{
          display: 0,
          gridLines: 0,
          ticks: {
            display: false
          },
          gridLines: {
            zeroLineColor: "transparent",
            drawTicks: false,
            display: false,
            drawBorder: false
          }
        }]
      },
      layout: {
        padding: {
          left: 0,
          right: 0,
          top: 15,
          bottom: 15
        }
      }
    };

    ctx = document.getElementById('lineChartExample').getContext("2d");

    gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
    gradientStroke.addColorStop(0, '#80b6f4');
    gradientStroke.addColorStop(1, chartColor);

    gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
    gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
    gradientFill.addColorStop(1, "rgba(249, 99, 59, 0.40)");

    myChart = new Chart(ctx, {
      type: 'line',
      responsive: true,
      data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
          label: "Active Users",
          borderColor: "#f96332",
          pointBorderColor: "#FFF",
          pointBackgroundColor: "#f96332",
          pointBorderWidth: 2,
          pointHoverRadius: 4,
          pointHoverBorderWidth: 1,
          pointRadius: 4,
          fill: true,
          backgroundColor: gradientFill,
          borderWidth: 2,
          data: [542, 480, 430, 550, 530, 453, 380, 434, 568, 610, 700, 630]
        }]
      },
      options: gradientChartOptionsConfiguration
    });
  },

  initDashboardPageCharts: function() {

    chartColor = "#FFFFFF";

    // General configuration for the charts with Line gradientStroke
    gradientChartOptionsConfiguration = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      tooltips: {
        bodySpacing: 4,
        mode: "nearest",
        intersect: 0,
        position: "nearest",
        xPadding: 10,
        yPadding: 10,
        caretPadding: 10
      },
      responsive: 1,
      scales: {
        yAxes: [{
          display: 0,
          gridLines: 0,
          ticks: {
            display: false
          },
          gridLines: {
            zeroLineColor: "transparent",
            drawTicks: false,
            display: false,
            drawBorder: false
          }
        }],
        xAxes: [{
          display: 0,
          gridLines: 0,
          ticks: {
            display: false
          },
          gridLines: {
            zeroLineColor: "transparent",
            drawTicks: false,
            display: false,
            drawBorder: false
          }
        }]
      },
      layout: {
        padding: {
          left: 0,
          right: 0,
          top: 15,
          bottom: 15
        }
      }
    };

    gradientChartOptionsConfigurationWithNumbersAndGrid = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      tooltips: {
        bodySpacing: 4,
        mode: "nearest",
        intersect: 0,
        position: "nearest",
        xPadding: 10,
        yPadding: 10,
        caretPadding: 10
      },
      responsive: true,
      scales: {
        yAxes: [{
          gridLines: 0,
          gridLines: {
            zeroLineColor: "transparent",
            drawBorder: false
          }
        }],
        xAxes: [{
          display: 0,
          gridLines: 0,
          ticks: {
            display: false
          },
          gridLines: {
            zeroLineColor: "transparent",
            drawTicks: false,
            display: false,
            drawBorder: false
          }
        }]
      },
      layout: {
        padding: {
          left: 0,
          right: 0,
          top: 15,
          bottom: 15
        }
      }
    };

$.ajax({
      url: '/api/monthly-avg/', // replace with your API endpoint
      method: 'GET',
      
    success: function(response)
    { 
      var apiResponse  = response;
          // console.log(apiResponse)
          var monthNames =["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
            var labels = [];
            var combinedAvgData = [];
            for (var i = 0; i < apiResponse.length; i++) {
              // labels.push(apiResponse[i]['month']);
              // combinedAvgData.push(apiResponse[i]['combined_avg']);
              var monthData = apiResponse[i];
              if (monthData['combined_avg'] !== 0) { 
                var monthName = monthNames[monthData['month'] - 1];
                labels.push(monthName);
                combinedAvgData.push(monthData['combined_avg']);
              }
            }
            labels.sort(function(a, b) {
              return a - b;
            });
combinedAvgData = combinedAvgData.filter((_, i) => labels.includes(labels[i]));
    var ctx = document.getElementById('bigDashboardChart').getContext("2d");

    var gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
    gradientStroke.addColorStop(0, '#80b6f4');
    gradientStroke.addColorStop(1, chartColor);

    var gradientFill = ctx.createLinearGradient(0, 200, 0, 50);
    gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
    gradientFill.addColorStop(1, "rgba(255, 255, 255, 0.24)");

    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        // labels: ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
        labels: labels,
        datasets: [{ 
          label: "Data",
          borderColor: chartColor,
          pointBorderColor: chartColor,
          pointBackgroundColor: "#1e3d60",
          pointHoverBackgroundColor: "#1e3d60",
          pointHoverBorderColor: chartColor,
          pointBorderWidth: 1,
          pointHoverRadius: 7,
          pointHoverBorderWidth: 2,
          pointRadius: 5,
          fill: true,
          backgroundColor: gradientFill,
          borderWidth: 2,
          // data: [50, 150, 100, 190, 130, 90, 150, 160, 120, 140, 190, 95]
          data: combinedAvgData
        }]
      },
      options: {
        layout: {
          padding: {
            left: 20,
            right: 20,
            top: 0,
            bottom: 0
          }
        },
        maintainAspectRatio: false,
        tooltips: {
          backgroundColor: '#fff',
          titleFontColor: '#333',
          bodyFontColor: '#666',
          bodySpacing: 4,
          xPadding: 12,
          mode: "nearest",
          intersect: 0,
          position: "nearest"
        },
        legend: {
          position: "bottom",
          fillStyle: "#FFF",
          display: false
        },
        scales: {
          yAxes: [{
            ticks: {
              fontColor: "rgba(255,255,255,0.4)",
              fontStyle: "bold",
              beginAtZero: true,
              maxTicksLimit: 5,
              padding: 10
            },
            gridLines: {
              drawTicks: true,
              drawBorder: false,
              display: true,
              color: "rgba(255,255,255,0.1)",
              zeroLineColor: "transparent"
            }

          }],
          xAxes: [{
            gridLines: {
              zeroLineColor: "transparent",
              display: false,

            },
            ticks: {
              padding: 10,
              fontColor: "rgba(255,255,255,0.4)",
              fontStyle: "bold"
            }
          }]
        }
      }
    });
  }
  })

    var cardStatsMiniLineColor = "#fff",
      cardStatsMiniDotColor = "#fff";
    $.ajax({
        url: '/api/monthly-dlt/',
        method: 'GET',
      success: function(response)
      { 
        var apiResponse  = response;
            // console.log(apiResponse);
            var monthNames =["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
            var labels = [];
            var dataCounts = [];
            for (var i = 0; i < apiResponse.length; i++) {
              var monthData = apiResponse[i];
              if (monthData['count'] !== 0) { 
                var monthName = monthNames[monthData['month'] - 1];
                labels.push(monthName);
                dataCounts.push(monthData['count']);
              }
            }
            labels.sort(function(a, b) {
              return a - b;
            });
            var combinedData = labels.map(function(label, index) {
              return { label: label, count: dataCounts[index] };
            });
            combinedData.sort(function(a, b) {
              var monthIndexA = monthNames.indexOf(a.label);
              var monthIndexB = monthNames.indexOf(b.label);
              return monthIndexA - monthIndexB;
            });
            labels = combinedData.map(function(data) {
              return data.label;
            });
            dataCounts = combinedData.map(function(data) {
              return data.count;
            });
            // console.log(labels);
            // console.log(dataCounts);
    ctx = document.getElementById('lineChartExample').getContext("2d");

    gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
    gradientStroke.addColorStop(0, '#80b6f4');
    gradientStroke.addColorStop(1, chartColor);

    gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
    gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
    gradientFill.addColorStop(1, "rgba(249, 99, 59, 0.40)");

    myChart = new Chart(ctx, {
      type: 'line',
      responsive: true,
      data: {
        // labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        labels: labels,
        datasets: [{
          label: "Out",
          borderColor: "#f96332",
          pointBorderColor: "#FFF",
          pointBackgroundColor: "#f96332",
          pointBorderWidth: 2,
          pointHoverRadius: 4,
          pointHoverBorderWidth: 1,
          pointRadius: 4,
          fill: true,
          backgroundColor: gradientFill,
          borderWidth: 2,
          // data: [542, 480, 430, 550, 530, 453, 380, 434, 568, 610, 700, 630]
          data: dataCounts
        }]
      },
      options: gradientChartOptionsConfiguration
    })
    }
  });

  $.ajax({
    url: '/api/monthly-daily/',
    method: 'GET',
  success: function(response)
  { 
    var apiResponse  = response;
    var monthNames = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
    var currentMonthIndex = new Date().getMonth();
    // const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

    // const d = new Date();
    // let currentMonthIndex = monthNames[d.getMonth()];
    // console.log(month);
    // console.log(currentMonthIndex);
    var startIndex = (currentMonthIndex + 10) % 12;
    // if (currentMonthIndex !== 2) {
    //   startIndex = currentMonthIndex < 2 ? 12 + currentMonthIndex - 2 : currentMonthIndex - 2;
    // }

        // console.log(apiResponse);
        var labels = [];
        var dataCounts = [];
        for (var i = 0; i < apiResponse.length; i++) {
          var dayData = apiResponse[i];
          var monthIndex = (startIndex + dayData['month'] - 1) % 12; // Calculate the month index based on startIndex
          if (monthIndex === currentMonthIndex && dayData['count'] !== 0) { // Check if the month matches the current month
            var monthName = monthNames[monthIndex];
            var day = dayData['day'];
            labels.push(monthName + ' ' + day); // Concatenate month name and day
            dataCounts.push(dayData['count']);
          }
        }
        labels.sort(function(a, b) {
          var aDate = new Date('2000 ' + a);
          var bDate = new Date('2000 ' + b);
          return aDate - bDate;
        });
      // console.log(labels);
      // console.log(dataCounts);
    ctx = document.getElementById('lineChartExampleWithNumbersAndGrid').getContext("2d");

    gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
    gradientStroke.addColorStop(0, '#18ce0f');
    gradientStroke.addColorStop(1, chartColor);

    gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
    gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
    gradientFill.addColorStop(1, hexToRGB('#18ce0f', 0.4));

    myChart = new Chart(ctx, {
      type: 'line',
      responsive: true,
      data: {
        // labels: ["12pm,", "3pm", "6pm", "9pm", "12am", "3am", "6am", "9am"],
        labels: labels,
        datasets: [{
          label: "Products",
          borderColor: "#18ce0f",
          pointBorderColor: "#FFF",
          pointBackgroundColor: "#18ce0f",
          pointBorderWidth: 2,
          pointHoverRadius: 4,
          pointHoverBorderWidth: 1,
          pointRadius: 4,
          fill: true,
          backgroundColor: gradientFill,
          borderWidth: 2,
        //  data: [40, 500, 650, 700, 1200, 1250, 1300, 1900]
          data: dataCounts
        }]
      },
      options: gradientChartOptionsConfigurationWithNumbersAndGrid
    })
  }
  }
  );

  $.ajax({
      url: '/api/monthly-data/', // replace with your API endpoint
      method: 'GET',
      
    success: function(response)
    { 
      var monthlyData = response;
            
            // Extracting labels (months) and counts from the data
            var labels = [];
            var dataCounts = [];
            for (var i = 0; i < monthlyData.length; i++) {
                labels.push(monthlyData[i]['month']);
               
                dataCounts.push(monthlyData[i]['count']);
            }
            var months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
            for (var i = 0; i < labels.length; i++) {
                labels[i] = months[parseInt(labels[i]) - 1];
            }
            labels.sort(function(a, b) {
              return months.indexOf(a) - months.indexOf(b);
          });
          dataCounts = dataCounts.filter((_, i) => labels.includes(months[i]));
          // console.log(labels);
          // console.log(dataCounts);
      var e = document.getElementById("barChartSimpleGradientsNumbers").getContext("2d");

      gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
      gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
      gradientFill.addColorStop(1, hexToRGB('#2CA8FF', 0.6));

      var a = {
        type: "bar",
        data: {
          // labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
          labels: labels,
          datasets: [{
            label: "Data",
            backgroundColor: gradientFill,
            borderColor: "#2CA8FF",
            pointBorderColor: "#FFF",
            pointBackgroundColor: "#2CA8FF",
            pointBorderWidth: 2,
            pointHoverRadius: 4,
            pointHoverBorderWidth: 1,
            pointRadius: 4,
            fill: true,
            borderWidth: 1,
            // data: [80, 99, 86, 96, 123, 85, 100, 75, 88, 90, 123, 155]
            data: dataCounts
          }]
        },
        options: {
          maintainAspectRatio: false,
          legend: {
            display: false
          },
          tooltips: {
            bodySpacing: 4,
            mode: "nearest",
            intersect: 0,
            position: "nearest",
            xPadding: 10,
            yPadding: 10,
            caretPadding: 10
          },
          responsive: 1,
          scales: {
            yAxes: [{
              gridLines: 0,
              gridLines: {
                zeroLineColor: "transparent",
                drawBorder: false
              },
              ticks: {
                suggestedMin: 5
            }
            }],
            xAxes: [{
              display: 0,
              gridLines: 0,
              ticks: {
                display: false
              },
              gridLines: {
                zeroLineColor: "transparent",
                drawTicks: false,
                display: false,
                drawBorder: false
              }
            }]
          },
          layout: {
            padding: {
              left: 0,
              right: 0,
              top: 15,
              bottom: 15
            }
          }
        }
      }
    

      var viewsChart = new Chart(e, a);
    }
  });
    },

  // initGoogleMaps: function() {
  //   var myLatlng = new google.maps.LatLng(40.748817, -73.985428);
  //   var mapOptions = {
  //     zoom: 13,
  //     center: myLatlng,
  //     scrollwheel: false, //we disable de scroll over the map, it is a really annoing when you scroll through page
  //     styles: [{
  //       "featureType": "water",
  //       "elementType": "geometry",
  //       "stylers": [{
  //         "color": "#e9e9e9"
  //       }, {
  //         "lightness": 17
  //       }]
  //     }, {
  //       "featureType": "landscape",
  //       "elementType": "geometry",
  //       "stylers": [{
  //         "color": "#f5f5f5"
  //       }, {
  //         "lightness": 20
  //       }]
  //     }, {
  //       "featureType": "road.highway",
  //       "elementType": "geometry.fill",
  //       "stylers": [{
  //         "color": "#ffffff"
  //       }, {
  //         "lightness": 17
  //       }]
  //     }, {
  //       "featureType": "road.highway",
  //       "elementType": "geometry.stroke",
  //       "stylers": [{
  //         "color": "#ffffff"
  //       }, {
  //         "lightness": 29
  //       }, {
  //         "weight": 0.2
  //       }]
  //     }, {
  //       "featureType": "road.arterial",
  //       "elementType": "geometry",
  //       "stylers": [{
  //         "color": "#ffffff"
  //       }, {
  //         "lightness": 18
  //       }]
  //     }, {
  //       "featureType": "road.local",
  //       "elementType": "geometry",
  //       "stylers": [{
  //         "color": "#ffffff"
  //       }, {
  //         "lightness": 16
  //       }]
  //     }, {
  //       "featureType": "poi",
  //       "elementType": "geometry",
  //       "stylers": [{
  //         "color": "#f5f5f5"
  //       }, {
  //         "lightness": 21
  //       }]
  //     }, {
  //       "featureType": "poi.park",
  //       "elementType": "geometry",
  //       "stylers": [{
  //         "color": "#dedede"
  //       }, {
  //         "lightness": 21
  //       }]
  //     }, {
  //       "elementType": "labels.text.stroke",
  //       "stylers": [{
  //         "visibility": "on"
  //       }, {
  //         "color": "#ffffff"
  //       }, {
  //         "lightness": 16
  //       }]
  //     }, {
  //       "elementType": "labels.text.fill",
  //       "stylers": [{
  //         "saturation": 36
  //       }, {
  //         "color": "#333333"
  //       }, {
  //         "lightness": 40
  //       }]
  //     }, {
  //       "elementType": "labels.icon",
  //       "stylers": [{
  //         "visibility": "off"
  //       }]
  //     }, {
  //       "featureType": "transit",
  //       "elementType": "geometry",
  //       "stylers": [{
  //         "color": "#f2f2f2"
  //       }, {
  //         "lightness": 19
  //       }]
  //     }, {
  //       "featureType": "administrative",
  //       "elementType": "geometry.fill",
  //       "stylers": [{
  //         "color": "#fefefe"
  //       }, {
  //         "lightness": 20
  //       }]
  //     }, {
  //       "featureType": "administrative",
  //       "elementType": "geometry.stroke",
  //       "stylers": [{
  //         "color": "#fefefe"
  //       }, {
  //         "lightness": 17
  //       }, {
  //         "weight": 1.2
  //       }]
  //     }]
  //   };

  //   var map = new google.maps.Map(document.getElementById("map"), mapOptions);

  //   var marker = new google.maps.Marker({
  //     position: myLatlng,
  //     title: "Hello World!"
  //   });

  //   // To add the marker to the map, call setMap();
  //   marker.setMap(map);
  // }
};